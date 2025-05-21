# main.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_country_data, get_top_days

# Config - Faster rendering
st.set_page_config(
    page_title="🌞 Solar Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - Simplified
with st.sidebar:
    st.title("Control")
    selected_country = st.selectbox(
        "Country",
        ['Benin', 'Togo', 'Sierra Leone'],
        index=0
    )
    
    # Show loading spinner only in sidebar
    with st.spinner(f"Loading {selected_country} data..."):
        df = load_country_data(selected_country)

# Main content - Progressive rendering
if df.empty:
    st.warning("No data loaded!")
    st.stop()

# 1. First show key metrics immediately
st.title(f"☀️ {selected_country} Solar Performance")
col1, col2, col3 = st.columns(3)
col1.metric("Avg GHI", f"{df['GHI'].mean():.1f} W/m²")
col2.metric("Peak Temp", f"{df['Tamb'].max():.1f}°C")
col3.metric("Avg Humidity", f"{df['RH'].mean():.1f}%")

# 2. Then render visualizations progressively
tab1, tab2 = st.tabs(["📈 Time Series", "📊 Distributions"])

with tab1:
    st.subheader("Daily Trends")
    
    # Weekly resampling for faster plotting
    weekly_df = df.resample('W', on='Timestamp').mean().reset_index()
    
    fig = px.line(
        weekly_df,
        x='Timestamp',
        y='GHI',
        title="Weekly Average GHI",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GHI Distribution")
        fig = px.histogram(
            df,
            x='GHI',
            nbins=50,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Temperature vs Humidity")
        fig = px.scatter(
            df.sample(1000),  # Random sample for faster rendering
            x='Tamb',
            y='RH',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# 3. Show top days last (least critical)
with st.expander("🏆 Top Performing Days"):
    top_days = get_top_days(df)
    if not top_days.empty:
        st.dataframe(
            top_days.style.format({"GHI": "{:.1f} W/m²"}),
            use_container_width=True
        )