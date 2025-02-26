import streamlit as st
import pandas as pd
from utils.data_generator import generate_listings_data, generate_seasonal_data
from utils.visualization import create_price_distribution_plot, create_occupancy_trend

def main():
    st.title("📊 Market Analysis Dashboard")
    
    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox(
            "Property Type",
            ["All", "Apartment", "House", "Villa", "Condo", "Studio"]
        )
    with col2:
        neighborhood = st.selectbox(
            "Neighborhood",
            ["All", "Downtown", "Suburb", "Beach Area", "Historic District", "Business District"]
        )
    
    # Generate and filter data
    df = generate_listings_data()
    if property_type != "All":
        df = df[df['property_type'] == property_type]
    if neighborhood != "All":
        df = df[df['neighborhood'] == neighborhood]
    
    # Price distribution
    st.plotly_chart(create_price_distribution_plot(df), use_container_width=True)
    
    # Seasonal trends
    seasonal_data = generate_seasonal_data()
    st.plotly_chart(create_occupancy_trend(seasonal_data), use_container_width=True)
    
    # Property listings
    st.subheader("Nearby Properties")
    for _, row in df.head(5).iterrows():
        st.markdown(f"""
        <div class="property-card">
            <h3>{row['property_type']} in {row['neighborhood']}</h3>
            <p>Price: ${row['price']:.2f}/night</p>
            <p>Rating: {row['rating']:.1f} ⭐ ({row['reviews_count']} reviews)</p>
            <p>{row['bedrooms']} beds • {row['bathrooms']} baths • {row['occupancy_rate']*100:.1f}% occupancy</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
