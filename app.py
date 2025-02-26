import streamlit as st
import pandas as pd
from utils.data_generator import generate_listings_data
from utils.visualization import create_metric_cards
from pages.auth import init_auth, login_page, auth_required

st.set_page_config(
    page_title="Airbnb Market Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Add signature
    st.markdown("""
        <div class="signature">
            Designed with 💖 by epsyy pepsy
        </div>
    """, unsafe_allow_html=True)

@auth_required
def show_dashboard():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; font-size: 3rem; margin-bottom: 2rem; background: linear-gradient(135deg, #FF385C, #ff1f4b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Welcome to Your Airbnb Analytics Dashboard 🏠
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards with hover effects
    st.markdown("""
    <div class="animate-slide-in">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
            <a href="Market_Analysis" class="feature-card" style="text-decoration: none;">
                <h4 style="color: #FF385C; font-size: 1.4rem; margin-bottom: 1rem;">📊 Market Analysis</h4>
                <p style="color: #666; line-height: 1.6;">Real-time market insights and competitive analysis</p>
            </a>
            <a href="Price_Comparison" class="feature-card" style="text-decoration: none;">
                <h4 style="color: #FF385C; font-size: 1.4rem; margin-bottom: 1rem;">💰 Price Comparison</h4>
                <p style="color: #666; line-height: 1.6;">Compare prices across multiple platforms instantly</p>
            </a>
            <a href="ROI_Calculator" class="feature-card" style="text-decoration: none;">
                <h4 style="color: #FF385C; font-size: 1.4rem; margin-bottom: 1rem;">📈 ROI Calculator</h4>
                <p style="color: #666; line-height: 1.6;">Advanced ROI calculations and projections</p>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats with enhanced styling
    df = generate_listings_data()
    metrics = create_metric_cards(df)

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0s;">
            <h3 style="font-size: 1.2rem; opacity: 0.9;">Average Price</h3>
            <h2 style="font-size: 3rem; margin: 1rem 0;">{metrics['Average Price']}</h2>
            <p style="opacity: 0.8; font-size: 1.1rem;">per night</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0.2s;">
            <h3 style="font-size: 1.2rem; opacity: 0.9;">Average Rating</h3>
            <h2 style="font-size: 3rem; margin: 1rem 0;">{metrics['Average Rating']}</h2>
            <p style="opacity: 0.8; font-size: 1.1rem;">from guests</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0.4s;">
            <h3 style="font-size: 1.2rem; opacity: 0.9;">Occupancy Rate</h3>
            <h2 style="font-size: 3rem; margin: 1rem 0;">{metrics['Occupancy Rate']}</h2>
            <p style="opacity: 0.8; font-size: 1.1rem;">average</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    init_auth()
    load_css()

    # Add sidebar navigation
    if st.session_state.is_authenticated:
        with st.sidebar:
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h2 style="color: white; font-size: 1.5rem; margin-bottom: 2rem;">Navigation</h2>
            </div>
            """, unsafe_allow_html=True)

            st.page_link("app.py", label="🏠 Dashboard", use_container_width=True)
            st.page_link("pages/market_analysis.py", label="📊 Market Analysis", use_container_width=True)
            st.page_link("pages/price_comparison.py", label="💰 Price Comparison", use_container_width=True)
            st.page_link("pages/roi_calculator.py", label="📈 ROI Calculator", use_container_width=True)

    if not st.session_state.is_authenticated:
        login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()