import streamlit as st
from models.user import User, init_db

def login_page():
    st.title("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = User.get_by_email(email)
            if user and user.verify_password(password):
                st.session_state.user = user
                st.session_state.is_authenticated = True
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    st.markdown("---")
    st.markdown("Don't have an account? [Sign Up](/signup)")

def signup_page():
    st.title("Create Your Account")
    
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if password != password_confirm:
                st.error("Passwords don't match")
                return
                
            try:
                user = User.create(email=email, password=password, full_name=full_name)
                st.success("Account created successfully! Please login.")
                st.session_state.require_login = True
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

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
