import streamlit as st
import requests
import pandas as pd

# Define the base URL for the backend API
BASE_URL = 'http://backend:8080'

#load overseas table
def load_data(table_name):
    response = requests.get(BASE_URL + '/tables/' + table_name)
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1]
        df = pd.DataFrame(rows, columns=columns)

        return df
    else:
        st.error(f'Failed to get data from backend: {response.status_code}')

def update_data(json_data, endpoint):
    response = requests.post(BASE_URL + '/insert/' + endpoint, json = json_data)
    if response.status_code == 200:
        st.success("Data updated successfully.")
    else:
        st.error("Failed to update data in the database.")

#PRICE OPTIMISATION MODEL
#post parameter data to the backend 
def input_parameters():
    