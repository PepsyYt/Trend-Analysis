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
    # Add dark mode styles
    st.markdown("""
        <style>
        /* Dark mode styles */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }

        .feature-card {
            background-color: #1F2937;
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid #374151;
            margin-bottom: 1rem;
        }

        .feature-card h3 {
            color: #FF385C;
            margin-bottom: 1rem;
        }

        .feature-card p {
            color: #D1D5DB;
        }

        .platform-card {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            color: #D1D5DB !important;
        }

        /* Hide auth pages when logged in */
        .auth-page {
            display: none;
        }

        /* Custom styling for metrics */
        [data-testid="stMetricValue"] {
            color: #FF385C !important;
        }
        </style>
    """, unsafe_allow_html=True)

    try:
        with open("assets/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

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

    # Hide Streamlit's default menu and auth pages when logged in
    hide_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    button[data-testid="baseButton-header"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)

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

    # Feature cards with enhanced styling for dark mode
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
    st.title("Market Analysis")
    from pages.market_analysis import main
    main()

def show_price_comparison():
    st.title("Price Comparison")
    from pages.price_comparison import main
    main()

def show_roi_calculator():
    st.title("ROI Calculator")
    from pages.roi_calculator import main
    main()

def main():
    init_auth()
    load_css()

    # Check if the user is trying to access auth pages while logged in
    if st.session_state.is_authenticated:
        current_page = st.experimental_get_query_params().get("page", [""])[0]
        if current_page in ["Signup", "Login"]:
            st.experimental_set_query_params(page="")
        show_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()