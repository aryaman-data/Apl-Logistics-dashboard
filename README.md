# APL Logistics — Delivery Performance Dashboard

A data analytics project analyzing delivery performance, delay risk, 
and logistics efficiency across 180,519 global shipments.

## Live Dashboard[
([url](https://apl-logistics-dashboard-ald.streamlit.app/))

## Project Overview
This project provides operational transparency into APL Logistics' 
delivery timelines and delay risks across global markets, regions, 
shipping modes, and customer segments.

## Key Findings
- 54.8% of shipments carry late delivery risk
- First Class shipping has the highest late risk (95%) despite being premium
- Standard Class is the most reliable mode at only 38% late risk
- +1 day is the most common delay affecting 60,000+ shipments
- Risk is systemic across all markets (54–57%) — not geographic

## Tech Stack
- Python — data cleaning and analysis
- Pandas & NumPy — data manipulation
- Matplotlib & Seaborn — static visualizations
- Plotly — interactive charts
- Streamlit — live dashboard

## Project Structure
- app.py — Streamlit dashboard application
- requirements.txt — Python dependencies

## How to Run Locally
pip install -r requirements.txt
streamlit run app.py

## Dataset
180,519 shipments across 40 columns including delivery status, 
shipping mode, regional data, customer segments, and financials.
