import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_listings_data(n_samples=100):
    np.random.seed(42)
    
    property_types = ['Apartment', 'House', 'Villa', 'Condo', 'Studio']
    neighborhoods = ['Downtown', 'Suburb', 'Beach Area', 'Historic District', 'Business District']
    
    data = {
        'property_id': range(1, n_samples + 1),
        'property_type': np.random.choice(property_types, n_samples),
        'neighborhood': np.random.choice(neighborhoods, n_samples),
        'price': np.random.normal(150, 50, n_samples),
        'bedrooms': np.random.choice([1, 2, 3, 4], n_samples),
        'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3], n_samples),
        'rating': np.random.uniform(3.5, 5, n_samples),
        'occupancy_rate': np.random.uniform(0.4, 0.9, n_samples),
        'reviews_count': np.random.randint(10, 200, n_samples)
    }
    
    return pd.DataFrame(data)

def generate_seasonal_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    n_days = len(dates)
    
    base_price = 150
    seasonal_factor = np.sin(np.linspace(0, 2*np.pi, n_days)) * 30
    weekend_factor = [30 if d.weekday() >= 5 else 0 for d in dates]
    
    data = {
        'date': dates,
        'price': base_price + seasonal_factor + weekend_factor + np.random.normal(0, 10, n_days)
    }
    
    return pd.DataFrame(data)

def generate_competitor_data(n_samples=20):
    platforms = ['Airbnb', 'OYO', 'MMT']
    data = []
    
    for platform in platforms:
        base_price = 150 if platform == 'Airbnb' else (130 if platform == 'OYO' else 170)
        prices = np.random.normal(base_price, 20, n_samples)
        
        for price in prices:
            data.append({
                'platform': platform,
                'price': price,
                'rating': np.random.uniform(3.5, 5),
                'reviews': np.random.randint(10, 200)
            })
    
    return pd.DataFrame(data)
