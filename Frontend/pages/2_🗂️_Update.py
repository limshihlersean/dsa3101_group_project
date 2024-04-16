import pandas as pd
import streamlit as st
import requests
import app

st.title("View your data here!")  # add a title

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

overseas_table = app.load_data('overseas')
all_isbundle_table = app.load_data('all_isbundle')
citizen_single_table = app.load_data('citizen_single')
noncitizen_single_table = app.load_data('noncitizen_single')

with st.expander("Overseas Cable Car"):
    selection = dataframe_with_selections(overseas_table)
    st.write("Your selection:")
    st.write(selection)
    if st.button('Delete', key=1):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'overseas')

with st.expander("Bundle packages"):
    selection = dataframe_with_selections(all_isbundle_table)
    st.write("Your selection:")
    st.write(selection)
    if st.button('Delete', key=2):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'all_isbundle')

with st.expander("Citizen (Single Attractions)"): 
    selection = dataframe_with_selections(citizen_single_table)
    st.write("Your selection:")
    st.write(selection)
    if st.button('Delete', key=3):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'citizen_single')


with st.expander("Non-citizen (Single Attractions)"): 
    selection = dataframe_with_selections(noncitizen_single_table)
    st.write("Your selection:")
    st.write(selection)
    if st.button('Delete', key=4):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'noncitizen_single')

