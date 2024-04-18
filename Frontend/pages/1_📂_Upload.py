import streamlit as st
import pandas as pd
from io import StringIO
import app

st.title("Upload your data here!")  # add a title

st.markdown("""
            Click on the different drop downs to upload the respective data.
            Ensure your csv files have the corresponding headers as shown in each expander.
            """)

def display_headers_as_table(df):
    # Extract headers
    headers = df.columns.tolist()
    edited_headers = [header.replace('_', ' ') for header in headers]

    # Create a DataFrame with headers as the only row
    headers_df = pd.DataFrame(None, columns=edited_headers)

    st.write("Your data should have the following columns filled:")  
    
    # Display the DataFrame
    st.dataframe(headers_df, width=1000)



overseas_table = app.load_data('overseas')
all_isbundle_table = app.load_data('all_isbundle')
citizen_single_table = app.load_data('citizen_single')
noncitizen_single_table = app.load_data('noncitizen_single')

with st.expander("Overseas Cable Car"):
    columns = display_headers_as_table(overseas_table)
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
    uploaded_file = st.file_uploader("Choose a file", key=4)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if st.button('Update', key=8):
            json = dataframe.to_json(orient ='records')
            app.update_data(json, 'noncitizen_single')

# upload_page.py

import streamlit as st
import pandas as pd

st.title("Upload your PED data here!")

st.markdown("""
            Upload the CSV file for analysis here. After uploading, you can navigate to the Price Elasticity of Demand page.
            """)

# Function to save the uploaded file in Streamlit's session state
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.session_state['uploaded_data'] = dataframe
        st.write(dataframe)
        st.dataframe(dataframe, use_container_width=True)
        st.success("File uploaded successfully!")

# Upload file and save it to session state
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
save_uploaded_file(uploaded_file)

# Reminder to go to the PED Analysis page for further analysis
st.markdown("Please go to the **PED Analysis** page to view the analysis.")
