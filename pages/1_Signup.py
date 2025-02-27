import streamlit as st
from pages.auth import signup_page
from models.user import init_db

def main():
    # Initialize database
    init_db()
    
    # Show signup page
    signup_page()

if __name__ == "__main__":
    main()
