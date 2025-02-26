import streamlit as st
import pandas as pd
from utils.data_generator import generate_competitor_data
from utils.visualization import create_competitor_comparison

def main():
    st.title("💰 Price Comparison")
    
    # Property details input
    col1, col2 = st.columns(2)
    with col1:
        bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=2)
    with col2:
        bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=5, value=2)
    
    amenities = st.multiselect(
        "Amenities",
        ["WiFi", "Pool", "Parking", "Kitchen", "Air Conditioning"],
        ["WiFi", "Kitchen"]
    )
    
    # Generate competitor data
    df = generate_competitor_data()
    
    # Display comparison chart
    st.plotly_chart(create_competitor_comparison(df), use_container_width=True)
    
    # Platform-wise analysis
    st.subheader("Platform Analysis")
    platforms = df.groupby('platform').agg({
        'price': ['mean', 'min', 'max'],
        'rating': 'mean',
        'reviews': 'sum'
    }).round(2)
    
    for platform in platforms.index:
        st.markdown(f"""
        <div class="property-card">
            <h3>{platform}</h3>
            <p>Average Price: ${platforms.loc[platform, ('price', 'mean')]:.2f}</p>
            <p>Price Range: ${platforms.loc[platform, ('price', 'min')]:.2f} - ${platforms.loc[platform, ('price', 'max')]:.2f}</p>
            <p>Average Rating: {platforms.loc[platform, ('rating', 'mean')]:.1f} ⭐</p>
            <p>Total Reviews: {platforms.loc[platform, ('reviews', 'sum')]}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
