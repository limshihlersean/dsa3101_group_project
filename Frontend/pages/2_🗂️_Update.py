import pandas as pd
import streamlit as st
import requests
import app

st.title("View and update your data here!")  # add a title

st.markdown("""
            Click on the different drop downs to view the respective data.
            Select the rows you wish to delete by checking the left most box of the
            corresponding rows and then click delete. 
            You may double check the rows you have selected under "Your selection:" 
            """)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        width=1000,
        disabled=df.columns
    )
    st.write("Your selection:")
    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = st.data_editor(edited_df[edited_df.Select], width=1000)

    return selected_rows.drop('Select', axis=1)

overseas_table = app.load_data('overseas')
all_isbundle_table = app.load_data('all_isbundle')
citizen_single_table = app.load_data('citizen_single')
noncitizen_single_table = app.load_data('noncitizen_single')
ped_table = app.load_data('ped_data')

with st.expander("Overseas Cable Car"):
    selection = dataframe_with_selections(overseas_table)
    if st.button('Delete', key=1):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'overseas')

with st.expander("Bundle packages"):
    selection = dataframe_with_selections(all_isbundle_table)
    if st.button('Delete', key=2):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'all_isbundle')

with st.expander("Citizen (Single Attractions)"): 
    selection = dataframe_with_selections(citizen_single_table)
    if st.button('Delete', key=3):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'citizen_single')


with st.expander("Non-citizen (Single Attractions)"): 
    selection = dataframe_with_selections(noncitizen_single_table)
    if st.button('Delete', key=4):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'noncitizen_single')

with st.expander("PED data"):
    selection = dataframe_with_selections(ped_table)
    if st.button('Delete', key=5):
        json = selection.to_json(orient ='index')
        app.delete_data(json, 'ped_table')