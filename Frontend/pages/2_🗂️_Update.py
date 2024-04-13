import pandas as pd
import streamlit as st
import requests
import app

def overseas_table():
    return app.load_data('overseas')

def all_isbundle_table():
    return app.load_data('all_isbundle')

def citizen_single_table():
    return app.load_data('citizen_single')

def noncitizen_single_table():
    return app.load_data('noncitizen_single')

st.title("Your data")  # add a title

with st.expander("Overseas"):
    edited_df = st.data_editor(overseas_table(), num_rows="dynamic")
    if st.button('Update', key=1):
        json = edited_df.to_json(orient ='records')
        app.update_data(json, 'overseas')

with st.expander("All is bundle"):
    edited_df = st.data_editor(all_isbundle_table(), num_rows="dynamic")
    if st.button('Update', key=2):
        json = edited_df.to_json(orient ='records')
        app.update_data(json, 'all_isbundle')


with st.expander("Citizen Single"): 
    edited_df = st.data_editor(citizen_single_table(), num_rows="dynamic")
    if st.button('Update', key=3):
        json = edited_df.to_json(orient ='records')
        app.update_data(json, 'citsingle')


with st.expander("Non-citizen Single"): 
    edited_df = st.data_editor(noncitizen_single_table(), num_rows="dynamic")
    if st.button('Update', key=4):
        json = edited_df.to_json(orient ='records')
        app.update_data(json, 'noncitsingle')





