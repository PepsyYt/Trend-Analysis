import streamlit as st
import pandas as pd
from utils.data_generator import generate_listings_data
from utils.visualization import create_metric_cards

st.set_page_config(
    page_title="Airbnb Market Analysis",
    page_icon="🏠",
    layout="wide"
)

def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    
    st.title("🏠 Airbnb Market Analysis Tool")
    
    # Header with property images
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://images.unsplash.com/photo-1549439602-43ebca2327af", use_column_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1469796466635-455ede028aca", use_column_width=True)
    with col3:
        st.image("https://images.unsplash.com/photo-1507652313519-d4e9174996dd", use_column_width=True)
    
    st.markdown("""
    Welcome to the Airbnb Market Analysis Tool! Make data-driven decisions for your property listings
    with our comprehensive analysis tools.
    
    ### Features:
    - 📊 Market Analysis Dashboard
    - 💰 Price Comparison
    - 📈 ROI Calculator
    - 🤖 AI-powered Pricing Suggestions
    """)
    
    # Quick Stats
    df = generate_listings_data()
    metrics = create_metric_cards(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Average Price</h3>
            <h2>{}</h2>
        </div>
        """.format(metrics['Average Price']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Average Rating</h3>
            <h2>{}</h2>
        </div>
        """.format(metrics['Average Rating']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Occupancy Rate</h3>
            <h2>{}</h2>
        </div>
        """.format(metrics['Occupancy Rate']), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
