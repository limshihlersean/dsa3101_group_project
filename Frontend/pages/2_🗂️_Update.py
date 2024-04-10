import pandas as pd
import streamlit as st
import requests

# load overseas table
def load_data_overseas():
    response = requests.get('http://localhost:8080/tables/overseas')
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1]
        df = pd.DataFrame(rows, columns=columns)
        return df
    else:
        st.error("Failed to fetch data from database.")
        return None

#load all_isbundle table
def load_data_all_isbundle():
    response = requests.get('http://localhost:8080/tables/all_isbundle')
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1]
        df = pd.DataFrame(rows, columns=columns)
        return df
    else:
        st.error("Failed to fetch data from database.")
        return None
    
#load citizen_single table
def load_data_citizen_single():
    response = requests.get('http://localhost:8080/tables/citizen_single')
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1]
        df = pd.DataFrame(rows, columns=columns)
        return df
    else:
        st.error("Failed to fetch data from database.")
        return None
    
#load noncitizen_single table
def load_data_noncitizen_single():
    response = requests.get('http://localhost:8080/tables/noncitizen_single')
    if response.status_code == 200:
        data = response.json()
        columns = data[0]
        rows = data[1]
        df = pd.DataFrame(rows, columns=columns)
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

df = load_data_citizen_single()

st.title("Your data")  # add a title


#allow users to add and delete rows
edited_df = st.data_editor(df, num_rows="dynamic")

if st.button('Update Data'):
    update_data(df)



