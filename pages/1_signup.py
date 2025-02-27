import streamlit as st
from models.user import User, init_db
from pages.auth import signup_page

def main():
    signup_page()

if __name__ == "__main__":
    main()
