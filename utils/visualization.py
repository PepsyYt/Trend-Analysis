import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_price_distribution_plot(df):
    fig = px.histogram(
        df,
        x='price',
        nbins=30,
        title='Price Distribution in Your Area',
        color_discrete_sequence=['#FF385C']
    )
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(t=40, l=40, r=40, b=40)
    )
    return fig

def create_occupancy_trend(df):
    fig = px.line(
        df,
        x='date',
        y='price',
        title='Seasonal Price Trends',
        color_discrete_sequence=['#00A699']
    )
    fig.update_layout(
        template='plotly_white',
        margin=dict(t=40, l=40, r=40, b=40)
    )
    return fig

def create_competitor_comparison(df):
    fig = px.box(
        df,
        x='platform',
        y='price',
        title='Price Comparison Across Platforms',
        color='platform',
        color_discrete_sequence=['#FF385C', '#00A699', '#484848']
    )
    fig.update_layout(
        template='plotly_white',
        margin=dict(t=40, l=40, r=40, b=40)
    )
    return fig

def create_metric_cards(df):
    avg_price = df['price'].mean()
    avg_rating = df['rating'].mean()
    avg_occupancy = df['occupancy_rate'].mean()
    
    return {
        'Average Price': f'${avg_price:.2f}',
        'Average Rating': f'{avg_rating:.1f}',
        'Occupancy Rate': f'{avg_occupancy*100:.1f}%'
    }
