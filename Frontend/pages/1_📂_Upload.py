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

    # Create a DataFrame with headers as the only row
    headers_df = pd.DataFrame(None, columns=headers)

    st.write("Your data should have the following columns filled:")  
    
    # Display the DataFrame
    st.dataframe(headers_df, width=1000)

def validate_null(df):
    if df.isnull().any().any():
        st.error("Your data has empty values. Please fill it in.")
        return False
    return True

def validate_type(df, target_datatypes):
    # Check if column names match
    if not df.columns.tolist() == list(target_datatypes.keys()):
        st.error("Column names in the uploaded file do not match with database column names.")
        return False
    
    # Check if data types match for each column
    for col in df.columns:
        try:
            df[col].astype(target_datatypes[col])
        except ValueError:
            st.error(f"Data type of column '{col}' does not match with database data type.\
                     Should be '{target_datatypes[col]}'.")
    
    return True

def validate_value_constraint(df, target_constraints):
    for col, values in target_constraints.items():
        if not df[col].isin(values).all():
            st.error(f"There exists values in column '{col}' that are not in '{values}'.")
            return False
    return True
            



datatype_overseas = {
    "company": "object",
    "country": "object",
    "city": "object",
    "duration": "int64",
    "distance": "float64",
    "snow": "int64",
    "tourist_volume_of_cable_car": "int64",
    "cable_car_price": "float64",
    "age_range": "int64",
    "is_nature": "int64",
    "type_of_trip": "int64",
    "is_citizen": "int64",
}

overseas_value_constraint = {
    "snow": [0,1],
    "age_range": [0,1,2,3,4],
    "is_nature": [0,1],
    "type_of_trip": [0,1],
    "is_citizen": [0,1],
}

datatype_bundle = {
    "company": "object",
    "age": "object",
    "is_citizen": "int64",
    "events": "object",
    "price": "float64",
    "singleA": "int64",
    "singleB": "int64",
    "singleC": "int64",
    "singleD": "int64",
    "singleE": "int64",
}

bundle_value_constraint = {
    "age": ["Child", "Adult", "Senior"],
    "is_citizen": [0,1],
}

datatype_citizen = {
    "company": "object",
    "year": "int64",
    "age": "object",
    "events": "object",
    "price": "float64",
}

citizen_value_constraint = {
    "age": ["Child", "Adult", "Senior"],
}

datatype_noncitizen = {
    "company": "object",
    "age": "object",
    "events": "object",
    "price": "float64",
}

noncitizen_value_constraint = {
    "age": ["Child", "Adult", "Senior"],
}

datatype_ped = {
    "is_citizen": "int64",
    "is_adult": "int64",
    "price": "float64",
    "quantity": "float64",
}

ped_constraint = {
    "is_citizen": [0,1],
    "is_adult": [0,1],
}

overseas_table = app.load_data('overseas')
all_isbundle_table = app.load_data('all_isbundle')
citizen_single_table = app.load_data('citizen_single')
noncitizen_single_table = app.load_data('noncitizen_single')
ped_table = app.load_data('ped_data')


def read_file(filename): 
    df = pd.read_csv(filename) 
    if(df.empty): 
        print ('CSV file is empty') 
    else: 
        print ('CSV file is not empty') 
        return df

with st.expander("Overseas Cable Car"):
    columns = display_headers_as_table(overseas_table)
    uploaded_file = st.file_uploader("Choose a file", key=1)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file) 
        st.dataframe(df)
        if validate_null(df) and validate_type(df, datatype_overseas) and validate_value_constraint(df, overseas_value_constraint):
            if st.button('Update', key=5):
                json = df.to_json(orient ='records')
                app.update_data(json, 'overseas')

with st.expander("Bundle packages"):
    columns = display_headers_as_table(all_isbundle_table)  
    uploaded_file = st.file_uploader("Choose a file", key=2)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if validate_null(df) and validate_type(df, datatype_bundle) and validate_value_constraint(df, bundle_value_constraint):
            if st.button('Update', key=6):
                json = df.to_json(orient ='records')
                app.update_data(json, 'all_isbundle')

with st.expander("Citizen (Single Attractions)"): 
    columns = display_headers_as_table(citizen_single_table)
    uploaded_file = st.file_uploader("Choose a file", key=3)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if validate_null(df) and validate_type(df, datatype_citizen) and validate_value_constraint(df, citizen_value_constraint):
            if st.button('Update', key=7):
                json = df.to_json(orient ='records')
                app.update_data(json, 'citizen_single')

with st.expander("Non-citizen (Single Attractions)"): 
    columns = display_headers_as_table(noncitizen_single_table)
    uploaded_file = st.file_uploader("Choose a file", key=4)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        # validation
        if validate_null(df) and validate_type(df, datatype_noncitizen) and validate_value_constraint(df, noncitizen_value_constraint):
            if st.button('Update', key=8):
                json = df.to_json(orient ='records')
                app.update_data(json, 'noncitizen_single')

with st.expander("PED data"): 
    columns = display_headers_as_table(ped_table)
    uploaded_file = st.file_uploader("Choose a file", key=9)
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if validate_null(df) and validate_type(df, datatype_ped) and validate_value_constraint(df, ped_constraint):
            if st.button('Update', key=10):
                json = df.to_json(orient ='records')
                app.update_data(json, 'ped_table')

