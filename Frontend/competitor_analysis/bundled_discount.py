import streamlit as st
import altair as alt
import pandas as pd
import app  # Assuming 'app' is your data handling module

def display_chart():
    st.header("Bundled Discounts")

    st.markdown("The Bundled Discounts dives into two types of horizontal bar charts for locals and non-locals, showcasing discounts offered by various local competitors of MFLG. The bundle discounts are calculated using the formula:")
    st.latex(r'\text{Bundled Discount} = \left( \frac{\text{Original Summed Price} - \text{Bundle Price}}{\text{Original Summed Price}} \right) \times 100')
    st.markdown("Filter options based on age group and companies provide insights into bundling dynamics, empowering strategic decision-making.")


    # Load and preprocess the data
    bun_data = app.load_data('bundle_discount')  # Update the file name as necessary
    bun_data['original_price'] = pd.to_numeric(bun_data['original_price'], errors='coerce')
    bun_data['price'] = pd.to_numeric(bun_data['price'], errors='coerce')
    bun_data['discount'] = pd.to_numeric(bun_data['discount'], errors='coerce')
    bun_data['discount_percent'] = bun_data['discount'].map('{:.2f}%'.format)

    # Function to create a grouped horizontal bar chart
    def create_grouped_discount_bar_chart(data, title):
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('discount:Q', title='Percentage Discount (%)', scale=alt.Scale(zero=False)),
            y=alt.Y('company:N', title='', axis=alt.Axis(labels=False)),
            color=alt.Color('age:N', legend=None),
            row=alt.Row('age:N', header=alt.Header(title='Age Category')),
            tooltip=[
                alt.Tooltip('company:N', title='Company'),
                alt.Tooltip('original_price:Q', title='Original Price', format='$.2f'),
                alt.Tooltip('price:Q', title='Bundled Price', format='$.2f'),
                alt.Tooltip('discount_percent:O', title='Percentage Discount'),
                alt.Tooltip('age:N', title='Age Category')
            ]
        ).properties(
            title=title,
            width=150
        ).configure_view(
            stroke=None
        ).configure_facet(
            spacing=10
        )
        return chart

    # Sidebar and filtering for Local Categories
    st.sidebar.subheader('Filter for Local Categories')
    filtered_local_data = bun_data[bun_data['is_citizen'] == 1]
    selected_ages_local = st.sidebar.multiselect(
        'Select Age Group (Local):',
        options=filtered_local_data['age'].unique(),
        default=filtered_local_data['age'].unique()[:1],
        key='age_select_local'
    )
    filtered_age_data_local = filtered_local_data[filtered_local_data['age'].isin(selected_ages_local)]
    selected_companies_local = st.sidebar.multiselect(
        'Select Companies (Local):',
        options=filtered_age_data_local['company'].unique(),
        default=filtered_age_data_local['company'].unique()[:5],
        key='company_select_local'
    )
    final_filtered_data_local = filtered_age_data_local[filtered_age_data_local['company'].isin(selected_companies_local)]
    if final_filtered_data_local.empty:
        st.write("Please select at least one category to visualize the Local Bundled Discounts.")
    else:
        # Create and display the chart for Local Categories
        local_discount_chart = create_grouped_discount_bar_chart(final_filtered_data_local, 'Bundled Discounts for Locals')
        st.altair_chart(local_discount_chart, use_container_width=True)

    # Sidebar and filtering for Non-Local Categories
    st.sidebar.subheader('Filter for Non-Local Categories')
    filtered_non_local_data = bun_data[bun_data['is_citizen'] == 0]
    selected_ages_non_local = st.sidebar.multiselect(
        'Select Age Group (Non-Local):',
        options=filtered_non_local_data['age'].unique(),
        default=filtered_non_local_data['age'].unique()[:1],
        key='age_select_non_local'
    )
    filtered_age_data_non_local = filtered_non_local_data[filtered_non_local_data['age'].isin(selected_ages_non_local)]
    selected_companies_non_local = st.sidebar.multiselect(
        'Select Companies (Non-Local):',
        options=filtered_age_data_non_local['company'].unique(),
        default=filtered_age_data_non_local['company'].unique()[:5],
        key='company_select_non_local'
    )
    final_filtered_data_non_local = filtered_age_data_non_local[filtered_age_data_non_local['company'].isin(selected_companies_non_local)]
    if final_filtered_data_non_local.empty:
        st.write("Please select at least one category to visualize the Non-Local Bundled Discounts.")
    else:
        # Create and display the chart for Non-Local Categories
        non_local_discount_chart = create_grouped_discount_bar_chart(final_filtered_data_non_local, 'Bundled Discounts for Non-Locals')
        st.altair_chart(non_local_discount_chart, use_container_width=True)

