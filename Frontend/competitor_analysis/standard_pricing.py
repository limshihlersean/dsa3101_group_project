import streamlit as st
import altair as alt
import app  # assuming 'app' is a module for handling data operations

def display_chart():
    st.header('Standard Pricing Overview')

    st.write("The standard pricing overview presents a comparative bar chart of cable car fares across age groups and operator categories, focusing on local Singapore attractions versus overseas. Users can filter results by age and attraction, offering insights for pricing strategy adjustments to stay competitive.")

    def create_price_comparison_chart(data):
        # Create the chart
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('company:N', axis=alt.Axis(title='Attraction')),
            y=alt.Y('price:Q', axis=alt.Axis(title='Price (SGD)', format='$.2f'), scale=alt.Scale(zero=False)),  # Format the y-axis
            color=alt.Color('age:N', legend=None),  # Assuming 'age' column contains the ticket type
            tooltip=[
                alt.Tooltip('company:N', title='Company'),
                alt.Tooltip('age:N', title='Age Group'),
                alt.Tooltip('price:Q', title='Price', format='$.2f')  # Format price in tooltip to two decimal places
            ]
        ).properties(
            width=200,  # Adjust the width as needed
            height=200  # Adjust the height as needed
        ).facet(
            column=alt.Column('age:N', header=alt.Header(labelAngle=0, titleOrient='top')),
            spacing=20
        ).resolve_scale(
            x='independent',
            y='shared'
        ).configure_view(
            step=100
        ).configure_facet(
            spacing=10
        )

        return chart

    # Load the data
    pricing_data = app.load_data('pricing')

    st.sidebar.header("Filter for Standard Pricing Overview")

    selected_ages = st.sidebar.multiselect(
        'Select Age Groups:',
        options=pricing_data['age'].unique(),
        default=pricing_data['age'].unique()[:3],
        key='age_select_pricing'
    )
    filtered_data = pricing_data[pricing_data['age'].isin(selected_ages)]

    selected_categories = st.sidebar.multiselect(
        'Select Categories:',
        options=filtered_data['table_name'].unique(),
        default=filtered_data['table_name'].unique()[:1],
        key='category_select_pricing'
    )
    filtered_data = filtered_data[filtered_data['table_name'].isin(selected_categories)]

    selected_attractions = st.sidebar.multiselect(
        'Select Attractions:',
        options=filtered_data['company'].unique(),
        default=filtered_data['company'].unique()[:3] if len(filtered_data['company'].unique()) >= 3 else filtered_data['company'].unique(),
        key='attraction_select_pricing'
    )

    filtered_pricing_data = filtered_data[filtered_data['company'].isin(selected_attractions)]

    if len(filtered_pricing_data):
        price_comparison_chart = create_price_comparison_chart(filtered_pricing_data)
        st.altair_chart(price_comparison_chart, use_container_width=True)
    else:
        st.write("Please select at least one category to visualize the standard pricing overview.")
