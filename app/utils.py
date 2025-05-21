# utils.py
import pandas as pd
import streamlit as st
import os
from datetime import datetime

DATA_DIR = "data"

@st.cache_data(ttl=3600, show_spinner=False)  # Faster caching
def load_country_data(country_name):
    """Optimized data loading with selective columns"""
    replace_string = {"Sierra Leone": "sierraleone",
                      "Togo": "togo", 
                      "Benin":"benin" }
    try:
        filepath = os.path.join(DATA_DIR, f"{replace_string[country_name]}_clean.csv")
        
        # Only read necessary columns to save memory
        cols = ['Timestamp', 'GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
        df = pd.read_csv(filepath, usecols=cols, parse_dates=['Timestamp'])
        
        # Downcast numeric columns to save memory
        for col in df.select_dtypes(include=['float64']):
            df[col] = pd.to_numeric(df[col], downcast='float')
            
        return df.sort_values('Timestamp')
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def get_top_days(df, metric='GHI', n=5):
    """Optimized daily aggregation"""
    if df.empty or 'Timestamp' not in df.columns:
        return pd.DataFrame()
    
    return (df.set_index('Timestamp')
              .resample('D')[metric]
              .mean()
              .nlargest(n)
              .reset_index())