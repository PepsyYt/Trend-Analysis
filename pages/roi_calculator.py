import streamlit as st
import numpy as np
import pandas as pd

def calculate_roi(purchase_price, monthly_revenue, monthly_expenses, appreciation_rate):
    annual_revenue = monthly_revenue * 12
    annual_expenses = monthly_expenses * 12
    annual_profit = annual_revenue - annual_expenses
    
    property_value_after_year = purchase_price * (1 + appreciation_rate/100)
    total_return = annual_profit + (property_value_after_year - purchase_price)
    
    roi = (total_return / purchase_price) * 100
    return roi, annual_profit, total_return

def main():
    st.title("📈 ROI Calculator")
    
    # Property details
    st.subheader("Property Details")
    purchase_price = st.number_input("Purchase Price ($)", min_value=0, value=300000)
    
    # Revenue
    st.subheader("Monthly Revenue")
    nightly_rate = st.number_input("Average Nightly Rate ($)", min_value=0, value=150)
    occupancy_rate = st.slider("Expected Occupancy Rate (%)", 0, 100, 70)
    monthly_revenue = (nightly_rate * 30 * occupancy_rate/100)
    
    # Expenses
    st.subheader("Monthly Expenses")
    col1, col2 = st.columns(2)
    with col1:
        mortgage = st.number_input("Mortgage Payment ($)", min_value=0, value=1500)
        utilities = st.number_input("Utilities ($)", min_value=0, value=200)
        insurance = st.number_input("Insurance ($)", min_value=0, value=100)
    with col2:
        property_tax = st.number_input("Property Tax ($)", min_value=0, value=300)
        maintenance = st.number_input("Maintenance ($)", min_value=0, value=200)
        cleaning = st.number_input("Cleaning Services ($)", min_value=0, value=300)
    
    monthly_expenses = mortgage + utilities + insurance + property_tax + maintenance + cleaning
    
    # Appreciation
    appreciation_rate = st.slider("Expected Annual Appreciation Rate (%)", 0, 15, 3)
    
    # Calculate ROI
    roi, annual_profit, total_return = calculate_roi(
        purchase_price,
        monthly_revenue,
        monthly_expenses,
        appreciation_rate
    )
    
    # Display results
    st.subheader("Investment Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Annual ROI</h3>
            <h2>{roi:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Annual Profit</h3>
            <h2>${annual_profit:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Return</h3>
            <h2>${total_return:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Monthly breakdown
    st.subheader("Monthly Breakdown")
    st.markdown(f"""
    <div class="property-card">
        <p>Monthly Revenue: ${monthly_revenue:,.2f}</p>
        <p>Monthly Expenses: ${monthly_expenses:,.2f}</p>
        <p>Monthly Net Income: ${monthly_revenue - monthly_expenses:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
