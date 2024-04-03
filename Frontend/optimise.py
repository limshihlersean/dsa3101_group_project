#opening a new file
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np

#show title of the dashboard 
st.title('Price Optimisation Dashboard')

#sidebar 
st.sidebar.title('Selection of Factors')

#load csv file 
def load_data(filename):
    # Construct the full path to the file within the 'data' folder
    # The '..' moves up one directory level from the current script's location
    folder_path = os.path.join('..', 'data')
    full_path = os.path.join(folder_path, filename)
    
    # Load and return the CSV file
    return pd.read_csv(full_path)


st.header("Price Optimisation Based on Selected Factors")

#loading the data 
cable_car_data = load_data('cable_car_data_with_PPP.csv')

# Filters in the sidebar

#FILTER 1: Duration

st.sidebar.header("Preferred Duration")
selected_duration = st.sidebar.slider(
    'Select a duration', 0, 100, 50, 
    key='duration_select'
    #unique identifier for the duration
)
custom_duration = st.sidebar.number_input(
    "Or enter a custom value", 
    min_value=0, max_value=100, 
    value=50)

selected_value = selected_duration if custom_duration is None else custom_duration



#filtered_data = cable_car_data[cable_car_data['Duration (Mins)'].isin(selected_value)]

filtered_data = cable_car_data[cable_car_data['Duration (Mins)'] == selected_value]

#FILTER 2: DISTANCE 

st.sidebar.header("Preferred Distance")
selected_distance = st.sidebar.slider(
    'Select a distance', 0, 15, 3, 
    key='distance_select'
    #unique identifier for the duration
)
custom_duration = st.sidebar.number_input(
    "Or enter a custom value", 
    min_value=0, max_value=15, 
    value=3)

selected_distance_new = selected_distance if custom_distance is None else custom_distance