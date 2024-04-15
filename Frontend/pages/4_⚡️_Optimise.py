#opening a new file
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
import app
import requests

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
cable_car_data = load_data('cable_car_cleaned_v2.csv')
dist_dur_price_data = app.load_data('distance_duration_price')


# Filters in the sidebar
'''
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

filtered_data = cable_car_data[cable_car_data['duration'] == selected_value]

#FILTER 2: DISTANCE 

st.sidebar.header("Preferred Distance")
selected_distance = st.sidebar.slider(
    'Select a distance', 0, 15, 3, 
    key='distance_select'
    #unique identifier for the duration
)
custom_distance = st.sidebar.number_input(
    "Or enter a custom value", 
    min_value=0, max_value=15, 
    value=3)

selected_distance_new = selected_distance if custom_distance is None else custom_distance

filtered_data_distance = cable_car_data[cable_car_data['distance'] == selected_distance_new]

#FILTER 3: SNOW 

st.sidebar.header("Presence of Snow")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['Yes', 'No']
selected_snow = st.sidebar.selectbox(
    'Select option', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select'
)

# Logic to determine the selected value
selected_snow_value = yes_no_options.index(selected_snow)
filtered_data_snow = cable_car_data[cable_car_data['snow'] == selected_snow]
'''

#FILTER 4: Total volume of cable car 
st.sidebar.header("Total Volume of Cable Car")
selected_volume = st.sidebar.slider(
    'Select a volume', 100, 1000000, 5000, 
    key='volume_select'
    #unique identifier for the duration
)
#I dont think need this 
custom_volume = st.sidebar.number_input(
    "Or enter a custom value", 
    min_value=100, max_value=1000000, 
    value=5000)

selected_volume_new = selected_volume if custom_volume is None else custom_volume

#filtered_data_volume = cable_car_data[cable_car_data['tourist_volume_of_cable_car'] == selected_volume_new]
#check this because it seems like its == instead of inputting a new value 

#FILTER 5: AGE RANGE
st.sidebar.header("Age")


multiple_options = ['Child', 'Student', 'Adult', 'Senior Citizen/ Handicapped']
selected_age = st.sidebar.selectbox(
    'Select option', 
    options=multiple_options,
    index=0,  # Default index for 'Child'
    key='option_select_age'
)

# Mapping selected age to its corresponding index
age_mapping = {'Child': 0, 'Student': 1, 'Adult': 2, 'Senior Citizen/ Handicapped': 3}
selected_age_index = age_mapping[selected_age]



'''
#FILTER 6: NATURE 

st.sidebar.header("City or Nature")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['City', 'Nature']
selected_nature = st.sidebar.selectbox(
    'Select option', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select_nature'
)

# Logic to determine the selected value
selected_nature_value = yes_no_options.index(selected_nature)

filtered_data_nature = cable_car_data[cable_car_data['is_nature'] == selected_nature]

'''
#FILTER 7: TYPE OF TRIP
st.sidebar.header("Type of Trip")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['Round trip', 'One-way trip']
selected_trip = st.sidebar.selectbox(
    'Select option', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select_trip'
)

# Logic to determine the selected value
selected_trip_value = yes_no_options.index(selected_trip)
#filtered_data_trip = cable_car_data[cable_car_data['type_of_trip'] == selected_trip]

#FILTER 7: CITIZENSHIP
st.sidebar.header("Citizenship")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['Citizen', 'Non-citizen']
selected_citizenship = st.sidebar.selectbox(
    'Select option', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select_citizenship'
)

# Logic to determine the selected value
selected_citizen_value = yes_no_options.index(selected_citizenship)
filtered_data_citizen = cable_car_data[cable_car_data['is_citizen'] == selected_trip]


#Generating the optimal prices 
# Create a "Generate" button
if st.sidebar.button("Generate"):
    # Prepare the data to be sent to the backend
    selected_filters = {
        'selected_volume': selected_volume_new,
        'selected_age': selected_age,
        'selected_trip': selected_trip,
        'selected_citizenship': selected_citizenship
    }

#Converting the input data into a dictionary format 
# Initialize an empty dictionary to store the selected filters and values
data = {}

# Add selected volume to the dictionary
data['tourist_volume'] = selected_volume_new

# Add selected age to the dictionary
data['age_range'] = selected_age_index

# Add selected trip to the dictionary
data['is_one_way'] = selected_trip_value

# Add selected citizenship to the dictionary
data['is_citizen'] = selected_citizen_value

# Send a POST request to the backend
response = requests.post('http://backend:8080/model/priceoptmodel', json=data)

# Check if the request was successful
if response.status_code == 200:
    # Extract the response data
    response_data = response.json()
    
    # Extract the optimal price from the response
    optimal_price = response_data["optimal_price"]
    
    # Do something with the optimal price
    print("Optimal price:", optimal_price)
    st.write("Optimal price:", optimal_price)
else:
    print("Error:", response.text)





