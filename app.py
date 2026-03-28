# Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# page settings
st.set_page_config(page_title='Car Market Analyzer',
                   page_icon='🚗',
                   layout='wide')

# Read files
car_data = pd.read_csv('vehicles_us.csv')

# Header
st.header('Car Market Analyzer')
st.write('This is a car market analyzer that allows you to analyze the car market in the United States.')

st.write('---')

# Data visualizations
st.header('Data Visualizations')

# Histogram section
st.subheader('Histogram')
st.write('This histogram shows the distribution of the odometer readings of the cars in the dataset.')

build_histogram = st.checkbox("Build histogram")
if build_histogram:
    st.write('Generating histogram...')
    fig = px.histogram(car_data, x="odometer", nbins=50)
    st.plotly_chart(fig, use_container_width=True)

st.write('---')

# Scatter Plot section
st.subheader('Scatter Plot')
st.write('This scatter plot shows the relationship between odometer and price.')

build_scatter = st.checkbox("Build scatter plot")
if build_scatter:
    st.write('Generating scatter plot...')
    fig = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig, use_container_width=True)
