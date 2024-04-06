import streamlit as st
import requests

st.title('Streamlit Frontend')

if st.button('Get Message from Backend'):
    response = requests.get('http://localhost:8080/api/data') #is this the correct address
    if response.status_code == 200:
        data = response.json()
        st.write(data['message'])
    else:
        st.error('Failed to get data from backend')

if st.button('Send Data to Backend'):
    data = {'key': 'value'}
    response = requests.post('http://localhost:8080/api/data', json=data)
    if response.status_code == 200:
        response_data = response.json()
        st.write('Response from backend:', response_data)
    else:
        st.error('Failed to send data to backend')

if st.button('Update Data in Backend'):
    item_id = st.text_input('Item ID')
    new_value = st.text_input('New Value')
    patch_data = {'item_id': item_id, 'value': new_value}
    response = requests.patch('http://localhost:8080/api/data', json=patch_data)
    if response.status_code == 200:
        updated_data = response.json()
        st.write('Updated data received from backend:', updated_data)
    else:
        st.error('Failed to update data in backend')