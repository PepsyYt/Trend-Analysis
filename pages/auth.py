import streamlit as st
from models.user import User, init_db

def login_page():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; font-size: 3rem; margin-bottom: 2rem; background: linear-gradient(135deg, #FF385C, #ff1f4b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Welcome Back! 👋
        </h1>
        <p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">
            Log in to access your Airbnb analytics dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="card animate-slide-in" style="background: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        """, unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;" class="animate-fade-in">
        <p style="font-size: 1.1rem;">Don't have an account? <a href="1_signup" target="_self" style="color: #FF385C; font-weight: 600;">Sign Up</a></p>
    </div>
    """, unsafe_allow_html=True)

def signup_page():
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center; font-size: 3rem; margin-bottom: 2rem; background: linear-gradient(135deg, #FF385C, #ff1f4b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Create Your Account 🚀
        </h1>
        <p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">
            Join thousands of successful Airbnb hosts using our analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="card animate-slide-in" style="background: rgba(255,255,255,0.9); backdrop-filter: blur(10px);">
        """, unsafe_allow_html=True)

        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")

            st.markdown("""
            <div style="margin: 1.5rem 0;">
                <label style="display: flex; align-items: center; gap: 0.5rem; color: #666;">
            """, unsafe_allow_html=True)
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            st.markdown("</div>", unsafe_allow_html=True)

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
                        st.session_state.require_login = True
                        # Redirect to login page after 2 seconds
                        st.script("""
                            <script>
                            setTimeout(function(){
                                window.location.href = '/';
                            }, 2000);
                            </script>
                        """, unsafe_allow_html=True)
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;" class="animate-fade-in">
        <p style="font-size: 1.1rem;">Already have an account? <a href="/" target="_self" style="color: #FF385C; font-weight: 600;">Login</a></p>
    </div>
    
    <div class="signature">
        Designed with 💖 by epsyy pepsy
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