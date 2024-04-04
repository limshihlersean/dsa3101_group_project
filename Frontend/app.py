import streamlit as st
import requests

st.title('Streamlit Frontend')

if st.button('Get Message from Backend'):
    response = requests.get('http://localhost:5000/api/data') #is this the correct address
    if response.status_code == 200:
        data = response.json()
        st.write(data['message'])
    else:
        st.error('Failed to get data from backend')

if st.button('Send Data to Backend'):
    data = {'key': 'value'}
    response = requests.post('http://localhost:5000/api/data', json=data)
    if response.status_code == 200:
        response_data = response.json()
        st.write('Response from backend:', response_data)
    else:
        st.error('Failed to send data to backend')