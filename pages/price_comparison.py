import streamlit as st
import pandas as pd
from utils.data_generator import generate_competitor_data
from utils.visualization import create_competitor_comparison

def main():
    st.title("💰 Price Comparison Analysis")

    # Property details input
    col1, col2, col3 = st.columns(3)
    with col1:
        bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=2)
    with col2:
        bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=5, value=2)
    with col3:
        property_type = st.selectbox(
            "Property Type",
            ["Apartment", "Villa", "Bungalow", "Farmhouse", "Heritage Home", "Studio"]
        )

    # Indian-specific amenities
    st.subheader("Amenities")
    col1, col2 = st.columns(2)

    with col1:
        basic_amenities = st.multiselect(
            "Basic Amenities",
            [
                "WiFi", "TV", "Kitchen", "Washing Machine",
                "Power Backup", "Water Purifier", "Geyser",
                "24/7 Water Supply", "Parking"
            ],
            ["WiFi", "Kitchen"]
        )

    with col2:
        premium_amenities = st.multiselect(
            "Premium Amenities",
            [
                "AC (Split/Window)", "Swimming Pool", "Gym",
                "Garden/Terrace", "Security System", "Elevator",
                "Club House Access", "Servants Quarter",
                "Private Pool", "BBQ Area"
            ]
        )

    # Location features
    st.subheader("Location Features")
    location_features = st.multiselect(
        "Select Nearby Features",
        [
            "Metro Station", "Shopping Mall", "Restaurant",
            "Hospital", "School/College", "Temple",
            "Park", "Market", "Airport", "Beach"
        ]
    )

    # Generate competitor data
    df = generate_competitor_data()

    # Display comparison chart
    st.plotly_chart(create_competitor_comparison(df), use_container_width=True)

    # Platform-wise analysis
    st.subheader("Platform Analysis")

    # Create columns for platforms
    cols = st.columns(4)
    platforms = df.groupby('platform').agg({
        'price': ['mean', 'min', 'max'],
        'rating': 'mean',
        'reviews': 'sum'
    }).round(2)

    for idx, platform in enumerate(platforms.index):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="platform-card" style="padding: 1rem; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 1rem;">
                <h3 style="color: #FF385C;">{platform}</h3>
                <p><strong>Avg Price:</strong> ₹{platforms.loc[platform, ('price', 'mean')]:,.2f}</p>
                <p><strong>Price Range:</strong><br/>
                   ₹{platforms.loc[platform, ('price', 'min')]:,.2f} - ₹{platforms.loc[platform, ('price', 'max')]:,.2f}</p>
                <p><strong>Rating:</strong> {platforms.loc[platform, ('rating', 'mean')]:.1f} ⭐</p>
                <p><strong>Reviews:</strong> {platforms.loc[platform, ('reviews', 'sum'):,}</p>
            </div>
            """, unsafe_allow_html=True)

    # Pricing recommendations
    st.subheader("💡 Pricing Recommendations")
    st.info("""
    Based on your property features and location:
    - Recommended base price: ₹2,500 - ₹3,500 per night
    - Weekend surge: Add 20-30%
    - Festival season: Add 40-50%
    - Long stay discount: 10-15% for weekly bookings
    """)

if __name__ == "__main__":
    main()