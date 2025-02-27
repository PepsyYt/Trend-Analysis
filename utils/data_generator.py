import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_listings_data(n_samples=100):
    np.random.seed(42)

    property_types = ['Apartment', 'Villa', 'Bungalow', 'Farmhouse', 'Heritage Home', 'Studio']
    neighborhoods = ['South Delhi', 'Bandra West', 'Koramangala', 'Jubilee Hills', 'Boat Club Road']

    data = {
        'property_id': range(1, n_samples + 1),
        'property_type': np.random.choice(property_types, n_samples),
        'neighborhood': np.random.choice(neighborhoods, n_samples),
        'price': np.random.normal(5000, 2000, n_samples),  # Indian pricing in INR
        'bedrooms': np.random.choice([1, 2, 3, 4, 5], n_samples),
        'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4], n_samples),
        'rating': np.random.uniform(3.5, 5, n_samples),
        'occupancy_rate': np.random.uniform(0.4, 0.9, n_samples),
        'reviews_count': np.random.randint(10, 500, n_samples)
    }

    df = pd.DataFrame(data)
    # Ensure reasonable price ranges
    df.loc[df['price'] < 1000, 'price'] = 1000
    return df

def generate_seasonal_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    n_days = len(dates)

    # Base price with seasonal variations
    base_price = 5000  # Base price in INR

    # Seasonal factors
    season_factor = np.sin(np.linspace(0, 2*np.pi, n_days)) * 1000

    # Festival factors (major Indian festivals)
    festival_dates = {
        'Diwali': '2023-11-12',
        'Holi': '2023-03-08',
        'New Year': '2023-12-31',
        'Dussehra': '2023-10-24'
    }

    festival_factor = np.zeros(n_days)
    for date in dates:
        for festival_date in festival_dates.values():
            festival = pd.to_datetime(festival_date)
            if abs((date - festival).days) <= 5:  # 5 days around festival
                festival_factor[dates.get_loc(date)] = 2000

    # Weekend factor
    weekend_factor = [1500 if d.weekday() >= 5 else 0 for d in dates]

    data = {
        'date': dates,
        'price': base_price + season_factor + festival_factor + weekend_factor + np.random.normal(0, 500, n_days)
    }

    return pd.DataFrame(data)

def generate_competitor_data(n_samples=20):
    platforms = ['Airbnb', 'OYO', 'MakeMyTrip', 'Booking.com', 'Goibibo', 'Agoda']
    data = []

    platform_factors = {
        'Airbnb': {'base': 5000, 'std': 1000},
        'OYO': {'base': 3500, 'std': 800},
        'MakeMyTrip': {'base': 4500, 'std': 900},
        'Booking.com': {'base': 5500, 'std': 1200},
        'Goibibo': {'base': 4000, 'std': 850},
        'Agoda': {'base': 4800, 'std': 1000}
    }

    for platform in platforms:
        base_price = platform_factors[platform]['base']
        std = platform_factors[platform]['std']
        prices = np.random.normal(base_price, std, n_samples)

        for price in prices:
            data.append({
                'platform': platform,
                'price': max(1000, price),  # Ensure minimum price
                'rating': np.random.uniform(3.5, 5),
                'reviews': np.random.randint(10, 1000)
            })

    return pd.DataFrame(data)