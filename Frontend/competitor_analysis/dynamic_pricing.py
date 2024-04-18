import streamlit as st
import altair as alt
import pandas as pd
import app  # Assuming 'app' is your data handling module

def display_chart():
    st.header("Dynamic Pricing Chart")
    st.write("The dynamic pricing chart displays time series line graphs for various local competitors, segmented by age demographics. It tracks price changes over time and includes interactive tooltips that reveal events influencing these fluctuations. This chart provides a clear overview of pricing trends throughout the years.")

    # Load data
    dynamic_data = app.load_data('dynamic_pricing')
    
    # Ensure 'year' is treated as an integer
    dynamic_data['year'] = dynamic_data['year'].astype(int)

    # Function to create dynamic pricing chart
    def create_dynamic_pricing_chart(data, selected_companies, selected_ages):
        color_scale = alt.Scale(domain=selected_companies, scheme='category10')
        shape_scale = alt.Scale(domain=['Adult', 'Child', 'Senior', 'Student'], range=['circle', 'square', 'triangle-right', 'cross'])

        tooltip_content = [
            alt.Tooltip('year:O', title='Year'),
            alt.Tooltip('price:Q', title='Price', format='$.2f'),
            alt.Tooltip('events:N', title='Event'),
            alt.Tooltip('company:N', title='Company'),
            alt.Tooltip('age:N', title='Age')
        ]
        chart_layers = []

        for company in selected_companies:
            company_data = data[data['company'] == company]
            if company_data.empty:
                continue

            for age in selected_ages:
                age_range_data = company_data[company_data['age'] == age]
                lines = alt.Chart(age_range_data).mark_line().encode(
                    x=alt.X('year:O', title='Year', sort=sorted(data['year'].unique())),
                    y=alt.Y('price:Q', title='Price (SGD)', axis=alt.Axis(format='$,.2f')),
                    color=alt.Color('company:N', scale=color_scale, legend=alt.Legend(title="Company")),
                    tooltip=tooltip_content
                )
                points = alt.Chart(age_range_data).mark_point(filled=True, size=100).encode(
                    x='year:O',
                    y='price:Q',
                    shape=alt.Shape('age:N', scale=shape_scale, legend=None if not selected_ages else alt.Legend(title="Age", labelColor="white", symbolFillColor="white")),
                    color=alt.Color('company:N', scale=color_scale, legend=None),
                    tooltip=tooltip_content
                )
                chart_layers.append(lines + points)

        return alt.layer(*chart_layers) if chart_layers else alt.Chart().mark_text(text='No data to display', align='left')


    selected_ages = st.sidebar.multiselect(
        'Select Age Groups:',
        options=dynamic_data['age'].unique(),
        default=dynamic_data['age'].unique()[:1],
        key='age_select_pricing'
    )
    filtered_data = dynamic_data[dynamic_data['age'].isin(selected_ages)]

    selected_companies = st.sidebar.multiselect(
        'Select Companies:',
        options=filtered_data['company'].unique(),
        default=filtered_data['company'].unique()[:5]
    )
    if selected_companies:
        dynamic_pricing_chart = create_dynamic_pricing_chart(filtered_data, selected_companies, selected_ages)
        st.altair_chart(dynamic_pricing_chart, use_container_width=True)
    else:
        st.write("Please select at least one category to visualize the dynamic pricing data.")
