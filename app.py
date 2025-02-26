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
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")

        # Navigation options
        selected = st.radio(
            "",
            ["🏠 Dashboard", "📊 Market Analysis", "💰 Price Comparison", "📈 ROI Calculator"],
            label_visibility="collapsed"
        )

        # Logout button
        st.button("🚪 Logout", on_click=lambda: setattr(st.session_state, 'is_authenticated', False))

    # Main content
    st.title("Airbnb Market Analysis Dashboard")

    # Quick Stats
    df = generate_listings_data()
    metrics = create_metric_cards(df)

    # Display metrics in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Price", metrics['Average Price'])
    with col2:
        st.metric("Average Rating", metrics['Average Rating'])
    with col3:
        st.metric("Occupancy Rate", metrics['Occupancy Rate'])

    # Feature cards
    st.subheader("Available Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Market Analysis\nGet detailed market insights and trends")
    with col2:
        st.info("💰 Price Comparison\nCompare prices across platforms")
    with col3:
        st.info("📈 ROI Calculator\nCalculate potential returns")

def main():
    init_auth()
    load_css()

    if not st.session_state.is_authenticated:
        login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()