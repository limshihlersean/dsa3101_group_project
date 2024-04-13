import streamlit as st
import pandas as pd
from io import StringIO
import app

st.title("Upload your data here!")  # add a title
with st.expander("Overseas Cable Car"):
    uploaded_file = st.file_uploader("Choose a file", key=1)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=5):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'overseas')

with st.expander("Bundle packages"):
    uploaded_file = st.file_uploader("Choose a file", key=2)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=6):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'allisbundle')

with st.expander("Citizen (Single Attractions)"): 
    uploaded_file = st.file_uploader("Choose a file", key=3)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=7):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'citsingle')

with st.expander("Non-citizen (Single Attractions)"): 
    uploaded_file = st.file_uploader("Choose a file", key=4)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=8):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'noncitsingle')
