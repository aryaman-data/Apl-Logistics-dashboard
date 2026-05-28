import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="APL Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("APL_Logistics.csv", encoding="latin1")
    df["Delay Gap"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
    def classify(gap):
        if gap > 0: return "Delayed"
        elif gap == 0: return "On Time"
        else: return "Early"
    df["Delivery Class"] = df["Delay Gap"].apply(classify)
    df = df[df["Delivery Status"] != "Shipping canceled"].reset_index(drop=True)
    return df

df = load_data()

st.sidebar.title("Filters")
shipping_modes = ["All"] + sorted(df["Shipping Mode"].unique().tolist())
markets        = ["All"] + sorted(df["Market"].unique().tolist())
segments       = ["All"] + sorted(df["Customer Segment"].unique().tolist())

selected_mode    = st.sidebar.selectbox("Shipping Mode",    shipping_modes)
selected_market  = st.sidebar.selectbox("Market",           markets)
selected_segment = st.sidebar.selectbox("Customer Segment", segments)

filtered = df.copy()
if selected_mode    != "All": filtered = filtered[filtered["Shipping Mode"]    == selected_mode]
if selected_market  != "All": filtered = filtered[filtered["Market"]           == selected_market]
if selected_segment != "All": filtered = filtered[filtered["Customer Segment"] == selected_segment]

st.title("APL Logistics — Delivery Performance Dashboard")
st.markdown("**Delivery performance, delay risk, and logistics efficiency analysis**")
st.markdown("---")

total          = len(filtered)
ontime         = (filtered["Delay Gap"] <= 0).sum()
late_risk      = filtered["Late_delivery_risk"].mean() * 100
avg_delay      = filtered["Delay Gap"].mean()
avg_delay_late = filtered[filtered["Delay Gap"] > 0]["Delay Gap"].mean()
ontime_rate    = ontime / total * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="Total Orders",       value=f"{total:,}")
col2.metric(label="On-Time Rate",       value=f"{ontime_rate:.1f}%")
col3.metric(label="Late Delivery Risk", value=f"{late_risk:.1f}%")
col4.metric(label="Avg Delay (All)",    value=f"{avg_delay:.2f} days")
col5.metric(label="Avg Delay (Late)",   value=f"{avg_delay_late:.2f} days")

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Delivery Status Breakdown")
    status_counts = filtered["Delivery Status"].value_counts()
    fig1 = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        color_discrete_sequence=["#E24B4A","#1D9E75","#378ADD","#888780"],
        hole=0.45
    )
    fig1.update_traces(textposition="outside", textinfo="percent+label")
    fig1.update_layout(showlegend=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Delay Gap Distribution")
    delay_dist = filtered["Delay Gap"].value_counts().sort_index().reset_index()
    delay_dist.columns = ["Delay Gap", "Count"]
    delay_dist["Color"] = delay_dist["Delay Gap"].apply(
        lambda x: "On Time / Early" if x <= 0 else "Delayed"
    )
    fig2 = px.bar(
        delay_dist, x="Delay Gap", y="Count", color="Color",
        color_discrete_map={"On Time / Early":"#1D9E75","Delayed":"#E24B4A"},
        labels={"Delay Gap":"Delay Gap (days)","Count":"Number of Orders"}
    )
    fig2.update_layout(margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Shipping Mode Performance")
    mode_data = filtered.groupby("Shipping Mode").agg(
        Late_Risk_Pct=("Late_delivery_risk","mean")
    ).reset_index()
    mode_data["Late_Risk_Pct"] = (mode_data["Late_Risk_Pct"] * 100).round(1)
    mode_data = mode_data.sort_values("Late_Risk_Pct", ascending=False)
    fig3 = px.bar(
        mode_data, x="Shipping Mode", y="Late_Risk_Pct",
        color="Late_Risk_Pct",
        color_continuous_scale=["#1D9E75","#BA7517","#E24B4A"],
        text="Late_Risk_Pct",
        labels={"Late_Risk_Pct":"Late Risk (%)"}
    )
    fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig3.update_layout(coloraxis_showscale=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("Regional Late Delivery Risk")
    region_data = filtered.groupby("Order Region")["Late_delivery_risk"].mean() * 100
    region_data = region_data.reset_index()
    region_data.columns = ["Region","Late Risk %"]
    region_data = region_data.sort_values("Late Risk %", ascending=True)
    fig4 = px.bar(
        region_data, x="Late Risk %", y="Region", orientation="h",
        color="Late Risk %",
        color_continuous_scale=["#1D9E75","#BA7517","#E24B4A"],
        text="Late Risk %"
    )
    fig4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig4.update_layout(coloraxis_showscale=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Market Comparison")
    market_data = filtered.groupby("Market").agg(
        Late_Risk_Pct=("Late_delivery_risk","mean")
    ).reset_index()
    market_data["Late_Risk_Pct"] = (market_data["Late_Risk_Pct"] * 100).round(1)
    market_data = market_data.sort_values("Late_Risk_Pct", ascending=False)
    fig5 = px.bar(
        market_data, x="Market", y="Late_Risk_Pct",
        color="Late_Risk_Pct",
        color_continuous_scale=["#1D9E75","#BA7517","#E24B4A"],
        text="Late_Risk_Pct",
        labels={"Late_Risk_Pct":"Late Risk (%)"}
    )
    fig5.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig5.update_layout(coloraxis_showscale=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    st.subheader("Customer Segment Risk")
    seg_data = filtered.groupby("Customer Segment").agg(
        Late_Risk_Pct=("Late_delivery_risk","mean")
    ).reset_index()
    seg_data["Late_Risk_Pct"] = (seg_data["Late_Risk_Pct"] * 100).round(1)
    fig6 = px.bar(
        seg_data, x="Customer Segment", y="Late_Risk_Pct",
        color="Customer Segment",
        text="Late_Risk_Pct",
        color_discrete_sequence=["#378ADD","#1D9E75","#7F77DD"],
        labels={"Late_Risk_Pct":"Late Risk (%)"}
    )
    fig6.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig6.update_layout(showlegend=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

st.subheader("Correlation Heatmap")
numeric_cols = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Delay Gap","Late_delivery_risk",
    "Benefit per order","Sales per customer","Order Item Quantity"
]
corr = filtered[numeric_cols].corr().round(2)
corr.index   = ["Ship Real","Ship Sched","Delay Gap","Late Risk","Benefit","Sales","Quantity"]
corr.columns = ["Ship Real","Ship Sched","Delay Gap","Late Risk","Benefit","Sales","Quantity"]
fig7, ax = plt.subplots(figsize=(9,5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax)
plt.tight_layout()
st.pyplot(fig7)

st.markdown("---")
st.caption("APL Logistics · Delivery Performance Analysis · Built with Python & Streamlit")
