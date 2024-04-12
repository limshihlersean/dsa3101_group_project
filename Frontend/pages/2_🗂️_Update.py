import pandas as pd
import streamlit as st
import requests
import app

def update_data():
    response = requests.post('http://localhost:5000/')
    if response.status_code == 200:
        st.success("Data updated successfully.")
    else:
        st.error("Failed to update data in the database.")

def overseas_table():
    return app.load_data_overseas()

def all_isbundle_table():
    return app.load_data_all_isbundle()

def citizen_single_table():
    return app.load_data_citizen_single()

def noncitizen_single_table():
    return app.load_data_noncitizen_single()

st.title("Your data")  # add a title

col1, col2, col3, col4 = st.columns(4)

with col1:
    button1 = st.button('Overseas')

with col2:
    button2 = st.button('All is bundle')

with col3:
    button3 = st.button('Citizen Single')

with col4:
    button4 = st.button('Non-citizen Single')

if button1:
    edited_df = st.data_editor(overseas_table(), num_rows="dynamic")

if button2: 
    edited_df = st.data_editor(all_isbundle_table(), num_rows="dynamic")

if button3: 
    edited_df = st.data_editor(citizen_single_table(), num_rows="dynamic")

if  button4:
    edited_df = st.data_editor(noncitizen_single_table(), num_rows="dynamic")

if st.button('Not Working Update Data Button'):
    update_data(df)



