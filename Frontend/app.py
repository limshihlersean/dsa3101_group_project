import streamlit as st
import requests
import pandas as pd
import json

# Define the base URL for the backend API
BASE_URL = 'http://backend:8080'

#load tables
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
    try:
        json_data_dict = json.loads(json_data)
        response = requests.post(BASE_URL + '/insert/' + endpoint, json=json_data_dict)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    if response.status_code == 200:
        st.success("Data updated successfully.")
    else:
        st.error("Failed to update data in the database.")

#not working yet not referenced anywhere yet
def delete_data(json_data, endpoint):
    try:
        json_data_dict = json.loads(json_data)
        response = requests.delete(BASE_URL + '/delete/' + endpoint, json=json_data_dict)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    if response.status_code == 200:
        st.write("Your updated data:")
        updated_table = load_data(endpoint) 
        st.dataframe(updated_table, width=1000)
        st.success("Data deleted successfully.")
    else:
        st.error("Failed to delete data in the database.")

#PRICE OPTIMISATION MODEL
#post parameter data to the backend 
