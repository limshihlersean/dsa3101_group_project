import streamlit as st
import altair as alt
import pandas as pd
import app  # Assuming 'app' is a module for data handling

def display_chart():
    st.header("Local Discounts")

    st.markdown("The Local Discounts Overview presents a comparative bar chart illustrating discounts offered to Singaporean citizens at local attractions. Calculated using the formula:")
    st.latex(r'\text{Local Discount} = \left( \frac{\text{Original Price} - \text{Local Discounted Price}}{\text{Original Price}} \right) \times 100')
    st.markdown("These discounts are highlighted across various age groups and attractions. Users can filter results to gain insights for competitive pricing strategy adjustments, ensuring a competitive edge in the market.")


    # Load the data
    loc_disc_data = app.load_data('local_discount')  # Update the file name as necessary

    # Preprocess the data to ensure correct data types
    loc_disc_data['non_citizen_price'] = pd.to_numeric(loc_disc_data['non_citizen_price'], errors='coerce')
    loc_disc_data['citizen_price'] = pd.to_numeric(loc_disc_data['citizen_price'], errors='coerce')
    loc_disc_data['discount'] = pd.to_numeric(loc_disc_data['discount'], errors='coerce')
    loc_disc_data.drop_duplicates(inplace=True)
    loc_disc_data['discount_percent'] = loc_disc_data['discount'].map('{:.2f}%'.format)


    # Filter out any rows with missing data
    loc_disc_data = loc_disc_data.dropna(subset=['non_citizen_price', 'citizen_price', 'discount'])

    # Function to create a horizontal bar chart
    def create_local_discount_bar_chart(data, title):
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('discount:Q', title='Percentage Discount (%)', scale=alt.Scale(zero=False)),
            y=alt.Y('company:N', title=''),
            color=alt.Color('age:N',legend=None),  # Remove the legend for age
            row=alt.Row('age:N', title='Age Category'),
            tooltip=[
                alt.Tooltip('company:N', title='Attraction'),
                alt.Tooltip('non_citizen_price:Q', title='Original Price', format='$.2f'),
                alt.Tooltip('citizen_price:Q', title='Local Price', format='$.2f'),
                alt.Tooltip('discount_percent:O', title='Percentage Discount'),
                alt.Tooltip('age:N', title='Age Category')
            ]
        ).properties(
            title=title
        ).configure_facet(
            spacing=5
        ).configure_view(
            stroke=None
        ).configure_axis(
            labelFontSize=12  # Adjust label font size as necessary
        )
    
        return chart

    # Streamlit sidebar widget for age category selection
    st.sidebar.header('Filter for Local Discounts')
    selected_age_categories = st.sidebar.multiselect(
        'Select Age Categories:',
        options=loc_disc_data['age'].unique(),
        default=loc_disc_data['age'].unique(),
        key='age_category_select'
    )

    # Filter the data based on selected age categories
    filtered_age_category_data = loc_disc_data[loc_disc_data['age'].isin(selected_age_categories)]

    # Streamlit sidebar widget for attraction selection
    selected_attractions = st.sidebar.multiselect(
        'Select Attractions:',
        options=filtered_age_category_data['company'].unique(),
        default=filtered_age_category_data['company'].unique()[:5] if len(filtered_age_category_data['company'].unique()) >= 5 else filtered_age_category_data['company'].unique(),
        key='attraction_select_local'
    )

    # Apply filters to data based on selected attractions
    filtered_data = filtered_age_category_data[filtered_age_category_data['company'].isin(selected_attractions)]

    if len(filtered_data):
        # Create and display the price comparison chart
        local_discount_bar_chart = create_local_discount_bar_chart(filtered_data, 'Local Discounts by Attraction')
        st.altair_chart(local_discount_bar_chart, use_container_width=False)
    else:
        st.write("Please select at least one category to visualize the Local Discounts.")
