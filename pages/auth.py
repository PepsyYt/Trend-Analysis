import streamlit as st
from models.user import User, init_db

def login_page():
    st.markdown("""
    <style>
    /* Dark mode auth styling */
    .auth-container {
        background-color: #1F2937;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #374151;
        color: #D1D5DB;
    }
    .auth-title {
        color: #FF385C;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-subtitle {
        color: #9CA3AF;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .auth-link {
        color: #FF385C !important;
        text-decoration: none;
        font-weight: 600;
    }
    .auth-link:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-container">
        <h1 class="auth-title">Welcome Back! 👋</h1>
        <p class="auth-subtitle">Log in to access your Airbnb analytics dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                    return

                with st.spinner("Logging in..."):
                    try:
                        user = User.get_by_email(email)
                        if user and user.verify_password(password):
                            st.session_state.user = user
                            st.session_state.is_authenticated = True
                            st.success("Successfully logged in!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    if not st.session_state.get('is_authenticated', False):
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #D1D5DB;">Don't have an account? <a href="?page=Signup" class="auth-link">Sign Up</a></p>
        </div>
        """, unsafe_allow_html=True)

def signup_page():
    if st.session_state.get('is_authenticated', False):
        st.experimental_set_query_params(page="")
        st.rerun()
        return

    st.markdown("""
    <div class="auth-container">
        <h1 class="auth-title">Create Your Account 🚀</h1>
        <p class="auth-subtitle">Join thousands of successful Airbnb hosts using our analytics</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            submit = st.form_submit_button("Create Account", use_container_width=True)

            if submit:
                if not terms:
                    st.error("Please agree to the Terms of Service and Privacy Policy")
                    return

                if not full_name or not email or not password:
                    st.error("Please fill in all required fields")
                    return

                if password != password_confirm:
                    st.error("Passwords don't match")
                    return

                if len(password) < 8:
                    st.error("Password must be at least 8 characters long")
                    return

                with st.spinner("Creating your account..."):
                    try:
                        user = User.create(email=email, password=password, full_name=full_name)
                        st.success("Account created successfully! Please login.")
                        st.experimental_set_query_params(page="")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")

    if not st.session_state.get('is_authenticated', False):
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #D1D5DB;">Already have an account? <a href="?page=" class="auth-link">Login</a></p>
        </div>
        """, unsafe_allow_html=True)

def init_auth():
    # Initialize database tables
    init_db()

    # Initialize session state
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

    if 'user' not in st.session_state:
        st.session_state.user = None

def auth_required(func):
    def wrapper(*args, **kwargs):
        if not st.session_state.get('is_authenticated', False):
            st.warning("Please login to access this feature")
            login_page()
            return
        return func(*args, **kwargs)
    return wrapper