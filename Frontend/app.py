import streamlit as st
import requests
import pandas as pd

# Define the base URL for the backend API
BASE_URL = 'http://localhost:5000/api/data'

def get_message():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        st.write(data['message'])
    else:
        st.error('Failed to get data from backend')

def send_data():
    data = {'key': 'value'}
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 200:
        response_data = response.json()
        st.write('Response from backend:', response_data)
    else:
        st.error('Failed to send data to backend')

def update_backend_data(item_id, new_value):
    patch_data = {'item_id': item_id, 'value': new_value}
    response = requests.patch(BASE_URL, json=patch_data)
    if response.status_code == 200:
        updated_data = response.json()
        st.write('Updated data received from backend:', updated_data)
    else:
        st.error('Failed to update data in backend')


def update_resource(resource_id, data):
    base_url = 'http://localhost:5000/api/resource/'
    url = f'{base_url}{resource_id}'

    response = requests.put(url, json=data)
    
    if response.status_code == 200:
        print('Resource updated successfully:', response.json())
    else:
        print('Failed to update resource:', response.status_code)

# Example usage
data_to_update = {'name': 'Updated Resource', 'value': 150}
update_resource('1', data_to_update)

def delete_resource(resource_id):
    base_url = 'http://localhost:5000/api/resource/'
    url = f'{base_url}{resource_id}'

    response = requests.delete(url)
    
    if response.status_code == 200:
        print('Resource deleted successfully:', response.json())
    else:
        print('Failed to delete resource:', response.status_code)

# Example usage
delete_resource('1')

# Your Streamlit UI components
st.title('Streamlit Frontend')

if st.button('Get Message from Backend'):
    get_message()

if st.button('Send Data to Backend'):
    send_data()

item_id = st.text_input('Item ID')
new_value = st.text_input('New Value')
if st.button('Update Data in Backend') and item_id and new_value:
    update_backend_data(item_id, new_value)

