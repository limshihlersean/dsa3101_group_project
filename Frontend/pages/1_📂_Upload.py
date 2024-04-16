import streamlit as st
import pandas as pd
from io import StringIO
import app

st.title("Upload your data here!")  # add a title

def display_headers_as_table(df):
    # Extract headers
    headers = df.columns.tolist()

    # Create a DataFrame with headers as the only row
    headers_df = pd.DataFrame(None, columns=headers)

    # Display the DataFrame
    return headers_df

overseas_table = app.load_data('overseas')
all_isbundle_table = app.load_data('all_isbundle')
citizen_single_table = app.load_data('citizen_single')
noncitizen_single_table = app.load_data('noncitizen_single')

with st.expander("Overseas Cable Car"):
    columns = display_headers_as_table(overseas_table)
    st.write("Your data should have the following columns filled:")
    st.write(columns)
    uploaded_file = st.file_uploader("Choose a file", key=1)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=5):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'overseas')

with st.expander("Bundle packages"):
    columns = display_headers_as_table(all_isbundle_table)
    st.write("Your data should have the following columns filled:")
    st.write(columns)    
    uploaded_file = st.file_uploader("Choose a file", key=2)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=6):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'all_isbundle')

with st.expander("Citizen (Single Attractions)"): 
    columns = display_headers_as_table(citizen_single_table)
    st.write("Your data should have the following columns filled:")
    st.write(columns)   
    uploaded_file = st.file_uploader("Choose a file", key=3)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=7):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'citizen_single')

with st.expander("Non-citizen (Single Attractions)"): 
    columns = display_headers_as_table(noncitizen_single_table)
    st.write("Your data should have the following columns filled:")
    st.write(columns)   
    uploaded_file = st.file_uploader("Choose a file", key=4)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=8):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'noncitizen_single')
