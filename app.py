import streamlit as st
import pandas as pd
from utils.data_generator import generate_listings_data
from utils.visualization import create_metric_cards
from pages.auth import init_auth, login_page, auth_required

# Set dark theme as default
st.set_page_config(
    page_title="Airbnb Market Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

def load_css():
    # Dark mode styles
    st.markdown("""
        <style>
        /* Base dark theme */
        .stApp {
            background-color: #0E1117;
            color: #E5E7EB;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1F2937;
            border-right: 1px solid #374151;
        }

        /* Cards and containers */
        .feature-card, .platform-card, div[data-testid="stExpander"] {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            color: #E5E7EB !important;
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #F3F4F6 !important;
        }

        /* Text */
        p, label, div {
            color: #E5E7EB !important;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #FF385C !important;
            font-weight: bold !important;
        }

        [data-testid="stMetricDelta"] {
            color: #10B981 !important;
        }

        /* Buttons */
        button[kind="primary"] {
            background-color: #FF385C !important;
            color: white !important;
        }

        button[kind="secondary"] {
            border-color: #374151 !important;
            color: #E5E7EB !important;
        }

        /* Inputs */
        input, textarea, select {
            background-color: #374151 !important;
            color: #E5E7EB !important;
            border: 1px solid #4B5563 !important;
        }

        /* Hide auth pages when logged in */
        body[data-auth="true"] .auth-page {
            display: none !important;
        }

        /* Links */
        a {
            color: #FF385C !important;
            text-decoration: none !important;
        }

        a:hover {
            text-decoration: underline !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

@auth_required
def show_dashboard():
    # Sidebar navigation
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.user.full_name}! 👋")

        # Navigation options
        pages = {
            "🏠 Dashboard": "dashboard",
            "📊 Market Analysis": "market_analysis",
            "💰 Price Comparison": "price_comparison",
            "📈 ROI Calculator": "roi_calculator",
            "⚙️ Settings": "settings"
        }

        selected = st.radio(
            "Navigation",
            list(pages.keys()),
            label_visibility="collapsed"
        )

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.is_authenticated = False
            st.session_state.user = None
            st.rerun()

    # Main content based on selection
    if "Dashboard" in selected:
        show_main_dashboard()
    elif "Market Analysis" in selected:
        show_market_analysis()
    elif "Price Comparison" in selected:
        show_price_comparison()
    elif "ROI Calculator" in selected:
        show_roi_calculator()
    elif "Settings" in selected:
        show_settings()

def show_main_dashboard():
    st.title("Your Airbnb Market Analysis Dashboard")

    # Quick Stats
    df = generate_listings_data()
    metrics = create_metric_cards(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average Price", metrics['Average Price'], delta="↑ 5%")
    with col2:
        st.metric("Average Rating", metrics['Average Rating'], delta="↑ 0.2")
    with col3:
        st.metric("Occupancy Rate", metrics['Occupancy Rate'], delta="↑ 3%")
    with col4:
        st.metric("Total Properties", "156", delta="↑ 12")

    # Feature cards
    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;'>
        <div class='feature-card'>
            <h3>📊 Market Analysis</h3>
            <p>Get detailed insights about property performance, pricing trends, and market dynamics</p>
        </div>
        <div class='feature-card'>
            <h3>💰 Price Comparison</h3>
            <p>Compare your prices with competitors across multiple platforms</p>
        </div>
        <div class='feature-card'>
            <h3>📈 ROI Calculator</h3>
            <p>Calculate potential returns and analyze investment opportunities</p>
        </div>
        <div class='feature-card'>
            <h3>🎯 Recommendations</h3>
            <p>Get personalized suggestions to optimize your listing</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_settings():
    st.title("⚙️ Account Settings")
    with st.form("profile_settings"):
        st.text_input("Full Name", value=st.session_state.user.full_name)
        st.text_input("Email", value=st.session_state.user.email, disabled=True)
        st.form_submit_button("Update Profile")

def show_market_analysis():
    from pages.market_analysis import main
    main()

def show_price_comparison():
    from pages.price_comparison import main
    main()

def show_roi_calculator():
    from pages.roi_calculator import main
    main()

def main():
    init_auth()
    load_css()

    # Check if the user is trying to access auth pages while logged in
    if st.session_state.is_authenticated:
        show_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()