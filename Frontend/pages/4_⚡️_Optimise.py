#opening a new file
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
import app
import requests

# Center-align the content
st.markdown("""
    <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

#show title of the dashboard 
st.write("<h1 style='font-size: 36px;'>Price Optimisation</h1>", unsafe_allow_html=True)

#st.markdown('<h1 style="text-align: center;">Selection of Factors</h1>', unsafe_allow_html=True)
#st.markdown('<h2 style="text-align: center;">Price Optimisation Based on Total Volume of Cable Car, Age, Type of Trip, Citizenship</h2>', unsafe_allow_html=True)



#load csv file 
def load_data(filename):
    # Construct the full path to the file within the 'data' folder
    # The '..' moves up one directory level from the current script's location
    folder_path = os.path.join('..', 'data')
    full_path = os.path.join(folder_path, filename)
    print(full_path)
    # Load and return the CSV file
    return pd.read_csv(full_path)

#st.header("Price Optimization Based on Total Volume of Cable Car, Age, Type of Trip, Citizenship")
#st.write("<h1 style='color: darkgreen;'>Price Optimization Based on Total Volume of Cable Car, Age, Type of Trip, Citizenship</h1>", unsafe_allow_html=True)
st.write("Price Optimization Based on Total Volume of Cable Car, Age, Type of Trip, Citizenship")
st.subheader("Explore the optimal price of cable car with your inputs")
st.markdown("""Click on the different dropdowns to select your parameters. Then, you may click on "generate" to obtain the best price of a cable car ticket for your given parameters! """)
#loading the data 
#cable_car_data = load_data('cable_car_cleaned_v2.csv')
cable_car_data = app.load_data('overseas')
#dist_dur_price_data = app.load_data('distance_duration_price')


# Filters in the sidebar

# FILTER 4: Total volume of cable car 
#st.sidebar.header("Total Volume of Customers (per year)")

# Input for custom volume

selected_volume_new = st.number_input(
    "Input the total volume of customers for your cable car per year", 
    min_value=100000, max_value=1000000, 
    value=100000,
    step=1,  # Optional: You can adjust the step size if needed
    key='volume_input'  # Unique identifier for the input widget
)


selected_volume_new = selected_volume_new

#filtered_data_volume = cable_car_data[cable_car_data['tourist_volume_of_cable_car'] == selected_volume_new]
#check this because it seems like its == instead of inputting a new value 

#FILTER 5: AGE RANGE
#st.sidebar.header("Age")


multiple_options = ['Child', 'Student', 'Adult', 'Senior Citizen', 'Handicapped']
selected_age = st.selectbox(
    'Select the age range of your customer', 
    options=multiple_options,
    index=0,  # Default index for 'Child'
    key='option_select_age'
)

# Mapping selected age to its corresponding index
age_mapping = {'Child': 0, 'Student': 1, 'Adult': 2, 'Senior Citizen': 3, 'Handicapped':4}
selected_age_index = age_mapping[selected_age]



#FILTER 7: TYPE OF TRIP
#st.sidebar.header("Type of Trip")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['Round trip', 'One-way trip']
selected_trip = st.selectbox(
    'Select the type of trip', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select_trip'
)

# Logic to determine the selected value
selected_trip_value = yes_no_options.index(selected_trip)
#filtered_data_trip = cable_car_data[cable_car_data['type_of_trip'] == selected_trip]

#FILTER 7: CITIZENSHIP
#st.sidebar.header("Citizenship")

# Dropdown box for selecting 'Yes' or 'No'
yes_no_options = ['Citizen', 'Non-citizen']
selected_citizenship = st.selectbox(
    'Select the citizenship of your customer', 
    options=yes_no_options,
    index=0,  # Default index for 'Yes'
    key='option_select_citizenship'
)

# Logic to determine the selected value
#selected_citizen_value = yes_no_options.index(selected_citizenship)
#filtered_data_citizen = cable_car_data[cable_car_data['is_citizen'] == selected_trip]
selected_citizen_value = 1 if selected_citizenship == 'Citizen' else 0


#Generating the optimal prices 
# Create a "Generate" button
if st.button("Generate"):
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
        #st.write("Optimal price:", optimal_price)
        st.write(f"<h2 style='color:#106732;'>Optimal price: ${optimal_price:.2f}</h2>", unsafe_allow_html=True)

    else:
        print("Error:", response.text)

#st.image('https://www.mountfaberleisure.com/wp-content/uploads/2024/03/1080-x-1080_SkyOrb-SM-379x293.jpg', caption='Image of SkyOrb Cabins, the world\'s first chrome-finished spherical cable car cabin')

