import pandas as pd
import streamlit as st
import requests


def load_data():
    response = requests.get('http://localhost:5000/')
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        st.error("Failed to fetch data from database.")
        return None

def update_data():
    response = requests.post('http://localhost:5000/')
    if response.status_code == 200:
        st.success("Data updated successfully.")
    else:
        st.error("Failed to update data in the database.")

#df = load_data()

st.title("Your data")  # add a title
df = pd.read_csv("../data/cable_car_data_with_PPP.csv")

#allow users to add and delete rows
edited_df = st.data_editor(df, num_rows="dynamic")

if st.button('Update Data'):
    update_data(df)



