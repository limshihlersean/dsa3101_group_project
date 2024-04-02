import streamlit as st
import requests

st.title('Streamlit Frontend')

if st.button('Get Message from Backend'):
    response = requests.get('http://localhost:5000/data')
    if response.status_code == 200:
        data = response.json()
        st.write(data['message'])
    else:
        st.error('Failed to get data from backend')
