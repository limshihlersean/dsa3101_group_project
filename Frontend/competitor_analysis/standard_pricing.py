
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
            y=alt.Y('price:Q', axis=alt.Axis(title='Price (SGD)', format='$.2f'), scale=alt.Scale(zero=False)),
            color=alt.Color('age:N', legend=None),
            tooltip=[
                alt.Tooltip('company:N', title='Company'),
                alt.Tooltip('age:N', title='Age Group'),
                alt.Tooltip('price:Q', title='Price', format='$.2f')
            ]
        ).properties(
            width=200,
            height=200
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

    # Define the available age groups and categories dynamically based on the data
    age_groups = pricing_data['age'].unique()
    categories = pricing_data['table_name'].unique()
    companies = pricing_data['company'].unique()

    # Filter for age groups
    selected_ages = st.sidebar.multiselect(
        'Select Age Groups:',
        options=age_groups,
        default=age_groups[:3] if age_groups.size > 0 else [],
        key='age_select_pricing'
    )

    # Update the data based on age group selection
    filtered_data = pricing_data[pricing_data['age'].isin(selected_ages)] if selected_ages else pricing_data

    # Filter for categories
    updated_categories = filtered_data['table_name'].unique()
    selected_categories = st.sidebar.multiselect(
        'Select Categories:',
        options=updated_categories,
        default=updated_categories[:1] if updated_categories.size > 0 else [],
        key='category_select_pricing'
    )

    # Further refine the data based on category selection
    further_filtered_data = filtered_data[filtered_data['table_name'].isin(selected_categories)] if selected_categories else filtered_data

    # Filter for attractions
    updated_companies = further_filtered_data['company'].unique()
    selected_attractions = st.sidebar.multiselect(
        'Select Attractions:',
        options=updated_companies,
        default=updated_companies[:3] if updated_companies.size > 0 else [],
        key='attraction_select_pricing'
    )

    final_filtered_data = further_filtered_data[further_filtered_data['company'].isin(selected_attractions)] if selected_attractions else further_filtered_data

    if final_filtered_data.empty:
        st.write("Please select at least one category to visualize the standard pricing overview.")
    else:
        price_comparison_chart = create_price_comparison_chart(final_filtered_data)
        st.altair_chart(price_comparison_chart, use_container_width=True)

display_chart()


