import streamlit as st
from models.user import User, init_db

def login_page():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; margin-bottom: 2rem;">Welcome Back! 👋</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                with st.spinner("Logging in..."):
                    user = User.get_by_email(email)
                    if user and user.verify_password(password):
                        st.session_state.user = user
                        st.session_state.is_authenticated = True
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <p>Don't have an account? <a href="/signup" target="_self">Sign Up</a></p>
    </div>
    """, unsafe_allow_html=True)

def signup_page():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; margin-bottom: 2rem;">Create Your Account 🚀</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
                        st.session_state.require_login = True
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <p>Already have an account? <a href="/" target="_self">Login</a></p>
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