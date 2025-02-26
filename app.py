import streamlit as st
import pandas as pd
from utils.data_generator import generate_listings_data
from utils.visualization import create_metric_cards
from pages.auth import init_auth, login_page, auth_required

st.set_page_config(
    page_title="Airbnb Market Analysis",
    page_icon="🏠",
    layout="wide"
)

def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Add cursor animation
    st.markdown("""
    <script>
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    document.addEventListener('mousedown', () => cursor.classList.add('hover'));
    document.addEventListener('mouseup', () => cursor.classList.remove('hover'));
    </script>
    """, unsafe_allow_html=True)

@auth_required
def show_dashboard():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 2rem; background: linear-gradient(135deg, #FF385C, #ff1f4b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Welcome to Your Airbnb Analytics Dashboard 🏠
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Header with property images in a floating animation
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="float-animation" style="transition-delay: 0s;">
            <img src="https://images.unsplash.com/photo-1549439602-43ebca2327af" style="width: 100%; border-radius: 16px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);">
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="float-animation" style="transition-delay: 0.2s;">
            <img src="https://images.unsplash.com/photo-1469796466635-455ede028aca" style="width: 100%; border-radius: 16px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);">
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="float-animation" style="transition-delay: 0.4s;">
            <img src="https://images.unsplash.com/photo-1507652313519-d4e9174996dd" style="width: 100%; border-radius: 16px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="animate-fade-in" style="text-align: center; margin: 3rem 0;">
        <h2 style="font-size: 1.8rem; margin-bottom: 1.5rem;">Make Data-Driven Decisions for Your Property Listings</h2>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Unlock the power of market insights with our comprehensive analysis tools</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="animate-slide-in">
        <h3 style="font-size: 1.5rem; margin-bottom: 1.5rem;">🚀 Key Features</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div class="feature-card" style="padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h4 style="color: #FF385C;">📊 Market Analysis</h4>
                <p>Comprehensive market insights and trends</p>
            </div>
            <div class="feature-card" style="padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h4 style="color: #FF385C;">💰 Price Comparison</h4>
                <p>Compare prices across multiple platforms</p>
            </div>
            <div class="feature-card" style="padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h4 style="color: #FF385C;">📈 ROI Calculator</h4>
                <p>Calculate potential returns on investment</p>
            </div>
            <div class="feature-card" style="padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h4 style="color: #FF385C;">🤖 AI Pricing</h4>
                <p>AI-powered pricing recommendations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    df = generate_listings_data()
    metrics = create_metric_cards(df)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0s;">
            <h3>Average Price</h3>
            <h2 style="font-size: 2.5rem; margin: 1rem 0;">{metrics['Average Price']}</h2>
            <p style="opacity: 0.9;">per night</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0.2s;">
            <h3>Average Rating</h3>
            <h2 style="font-size: 2.5rem; margin: 1rem 0;">{metrics['Average Rating']}</h2>
            <p style="opacity: 0.9;">from guests</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card animate-fade-in" style="transition-delay: 0.4s;">
            <h3>Occupancy Rate</h3>
            <h2 style="font-size: 2.5rem; margin: 1rem 0;">{metrics['Occupancy Rate']}</h2>
            <p style="opacity: 0.9;">average</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    init_auth()
    load_css()

    if not st.session_state.is_authenticated:
        login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()