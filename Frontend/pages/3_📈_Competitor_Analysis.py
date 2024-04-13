# Required Libraries
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
import app 


#To show the title of Dashboard
st.title('Competitor Analysis Dashboard')

# Define the sidebar at the top of your script
st.sidebar.title('Filter and Selection Sidebar')


# Load CSV data
def load_data(filename):
    # Construct the full path to the file within the 'data' folder
    # The '..' moves up one directory level from the current script's location
    folder_path = os.path.join('..', 'data')
    full_path = os.path.join(folder_path, filename)
    
    # Load and return the CSV file
    return pd.read_csv(full_path)


#------------------------------------------------------------------------------#
st.header("Cable Car Price Analysis")

# Function to create scatter plot
def create_scatter_plot(data, x_axis, y_axis, color_category, title):
    return alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X(x_axis, title = x_axis),
        y=alt.Y(y_axis, title = y_axis, type = 'quantitative'),
        color=color_category,
        tooltip=['company', 'city', x_axis, y_axis]
    ).interactive().properties(
        width=300,
        height=300,
        title=title
    )

# Load and preprocess the data
dist_dur_price_data = app.load_data('distance_duration_price')


# Filters in the sidebar
st.sidebar.header("Filter for Cable Car Price Analysis")
selected_countries = st.sidebar.multiselect(
    'Select Countries',
    options=np.unique(dist_dur_price_data["country"]),
    default=np.unique(dist_dur_price_data["country"].unique()[:10]),
    key='country_select_dist_dur_price'
)

# Filter data based on selection
filtered_data = dist_dur_price_data[dist_dur_price_data['country'].isin(selected_countries)]

# Generate scatter plots
scatter_duration_price = create_scatter_plot(
    filtered_data,
    'duration',
    'price',
    'country:N',
    "Duration (Mins) vs. Cable car Price (SGD)"
)

scatter_distance_price = create_scatter_plot(
    filtered_data,
    'distance',
    'price',
    'country:N',
    "Distance (KM) vs. Cable car Price (SGD)"
)

# Combine the scatter plots side by side
combined_scatter_plots = alt.hconcat(scatter_duration_price, scatter_distance_price)

# Display the scatter plots
st.altair_chart(combined_scatter_plots, use_container_width=True)

#------------------------------------------------------------------------------#

st.header('Standard Pricing Overview')

def create_price_comparison_chart(data):
    # Assuming 'data' already has the format with 'company' as attraction, 'table_name' as category, 'age' as ticket type, and 'price'
    # No need to melt the data if it's already in long format
    
    # Create the chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('company:N', axis=alt.Axis(title='Attraction')),
        y=alt.Y('price:Q', axis=alt.Axis(title='Price'), scale=alt.Scale(zero=False)),
        color='age:N',  # Assuming 'age' column contains the ticket type
        tooltip=['company', 'age', 'price']
    ).properties(
        title='Competitor Pricing Comparison',
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

# Streamlit sidebar widget for category and attraction selection
st.sidebar.header('Filters for Standard Pricing Overview')
selected_categories = st.sidebar.multiselect(
    'Select Categories:',
    options=pricing_data['table_name'].unique(),
    default=pricing_data['table_name'].unique()[0],
    key='category_select_pricing'
)

filtered_data = pricing_data[pricing_data['table_name'].isin(selected_categories)]

selected_attractions = st.sidebar.multiselect(
    'Select Attractions:',
    options=filtered_data['company'].unique(),
    default=filtered_data['company'].unique()[:3]if len(filtered_data['company'].unique()) >= 3 else filtered_data['company'].unique(),
    key='attraction_select_pricing'
)

# Apply filters to pricing_data based on selected categories and attractions
filtered_pricing_data = pricing_data[pricing_data['table_name'].isin(selected_categories)]
filtered_pricing_data = filtered_pricing_data[filtered_pricing_data['company'].isin(selected_attractions)]

# Create the price comparison chart using the filtered data
price_comparison_chart = create_price_comparison_chart(filtered_pricing_data)

# Display the chart in the Streamlit app
st.altair_chart(price_comparison_chart, use_container_width=True)

#------------------------------------------------------------------------------#

import streamlit as st
import altair as alt
import pandas as pd

# Assuming 'data' is the DataFrame created from your JSON data
data = app.load_data('dynamic_pricing')

# Convert 'year' column to datetime format if necessary
data['year'] = pd.to_datetime(data['year'].astype(str), format='%Y')

def create_dynamic_pricing_chart(data, selected_companies):
    # Define color scheme for the companies
    color_scale = alt.Scale(domain=selected_companies, scheme='category10')

    # Define a unique shape for each age range
    shape_scale = alt.Scale(domain=['Adult', 'Child', 'Senior'],
                            range=['circle', 'square', 'triangle-right'])

    # Define the tooltip content
    tooltip_content = [
        alt.Tooltip('year:T', title='Year'),
        alt.Tooltip('price:Q', title='Price'),
        alt.Tooltip('events:N', title='Event'),
        alt.Tooltip('company:N', title='Company'),
        alt.Tooltip('age:N', title='Age')
    ]

    # Create the base chart for legend, no data will be displayed due to the filter
    legend_chart = alt.Chart(data).mark_point().encode(
        color=alt.Color('company:N', scale=color_scale, legend=alt.Legend(title="Company")),
        shape=alt.Shape('age:N', scale=shape_scale, legend=alt.Legend(title="Age"))
    ).transform_filter(
        alt.datum.company == 'This is a fake filter to hide the points'
    )

    # Initialize an empty list to collect chart layers
    chart_layers = [legend_chart]  # Start with the legend chart

    for company in selected_companies:
        # Filter data for the current company
        company_data = data[data['company'] == company]

        if company_data.empty:
            continue  # Skip companies with no data

        # Loop through the age ranges to create separate line and point charts
        for age in ['Adult', 'Child', 'Senior']:
            # Filter data for the current age range within the company
            age_range_data = company_data[company_data['age'] == age]

            # Create a line chart for the current age range within the company
            lines = alt.Chart(age_range_data).mark_line().encode(
                x='year:T',
                y='price:Q',
                color=alt.Color('company:N', scale=color_scale, legend=None),
                tooltip=tooltip_content
            )

            # Create points for the line chart
            points = alt.Chart(age_range_data).mark_point(filled=True, size=100).encode(
                x='year:T',
                y='price:Q',
                shape=alt.Shape('age:N', scale=shape_scale, legend=None),
                color=alt.Color('company:N', scale=color_scale, legend=None),
                tooltip=tooltip_content
            )

            # Add the line and point charts for the current age range as layers
            chart_layers.append(lines + points)

    # Combine all chart layers
    final_chart = alt.layer(*chart_layers).resolve_scale(color='independent') if chart_layers else alt.Chart().mark_text(text='No data to display', align='left')

    return final_chart

# Streamlit widget for company selection
st.sidebar.header('Filter for Dynamic Pricing Analysis')
selected_companies = st.sidebar.multiselect(
    'Select Companies:',
    options=data['company'].unique(),
    default=data['company'].unique()[:3]  # Default to first company
)

# Display the chart only if at least one company is selected
if selected_companies:
    dynamic_pricing_chart = create_dynamic_pricing_chart(data, selected_companies)
    st.altair_chart(dynamic_pricing_chart, use_container_width=True)
else:
    st.write("Please select at least one company to visualize the dynamic pricing data.")


#------------------------------------------------------------------------------#
    
st.header("Local Discounts")

# Load the data
loc_disc_data = app.load_data('local_discount')  # Update the file name as necessary

# Preprocess the data to ensure correct data types
loc_disc_data['non_citizen_price'] = pd.to_numeric(loc_disc_data['non_citizen_price'], errors='coerce')
loc_disc_data['citizen_price'] = pd.to_numeric(loc_disc_data['citizen_price'], errors='coerce')
loc_disc_data['discount'] = pd.to_numeric(loc_disc_data['discount'], errors='coerce')
loc_disc_data.drop_duplicates(inplace=True)

# Filter out any rows with missing data
loc_disc_data = loc_disc_data.dropna(subset=['non_citizen_price', 'citizen_price', 'discount'])

st.write('Max discount:', loc_disc_data['discount'].max())

# Function to create a grouped bar chart with age categories
# Function to create a horizontal bar chart with side-by-side bars for different age categories
def create_local_discount_bar_chart(data, title):
    # Horizontal bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('discount:Q', title='Percentage Discount', scale=alt.Scale(zero=False)),
        y=alt.Y('company:N', title=''),  # Y-axis will show company names
        color=alt.Color('age:N', legend=alt.Legend(title="Age Category")),  # Color by age category
        row=alt.Row('age:N'),  # Create separate columns for each age category
        tooltip=[
            alt.Tooltip('company:N', title='Attraction'),
            alt.Tooltip('non_citizen_price:Q', title='Original Price'),
            alt.Tooltip('citizen_price:Q', title='Local Price'),
            alt.Tooltip('discount:Q', title='Percentage Discount', format='.2f'),
            alt.Tooltip('age:N', title='Age Category')
        ]
    ).properties(
        title=title # Set the height to ensure that all bars are visible
    )

    # Configure the facet spacing and the width of each bar group
    chart = chart.configure_facet(
        spacing=5
    ).configure_view(
        stroke=None  # Remove the border around each facet to create a seamless view
    )
    
    return chart


# Streamlit sidebar widget for age category selection
st.sidebar.header('Filter for Local Discounts')
selected_age_categories = st.sidebar.multiselect(
    'Select Age Categories:',
    options=loc_disc_data['age'].unique(),
    default=loc_disc_data['age'].unique()[0],
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

# Create and display the price comparison chart
local_discount_bar_chart = create_local_discount_bar_chart(filtered_data, 'Local Discounts by Attraction')
st.altair_chart(local_discount_bar_chart, use_container_width=True)

#------------------------------------------------------------------------------#
st.header("Bundled Discounts")

# Load the data
bun_data = app.load_data('bundle_discount')  # Make sure the file name matches your CSV

# Preprocess the data to ensure correct data types
bun_data['original_price'] = pd.to_numeric(bun_data['original_price'], errors='coerce')
bun_data['price'] = pd.to_numeric(bun_data['price'], errors='coerce')
bun_data['discount'] = pd.to_numeric(bun_data['discount'], errors='coerce')

# Filter out any rows with missing data
data = bun_data.dropna(subset=['original_price', 'price', 'discount'])

def create_grouped_discount_bar_chart(data, title):
    # Grouped horizontal bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('discount:Q', title='Percentage Discount', scale=alt.Scale(zero=False)),
        y=alt.Y('company:N', title='', axis=alt.Axis(labels=False)),  # Y-axis will show company names but hide labels to avoid repetition
        color=alt.Color('age:N', legend=alt.Legend(title="Age Category")),  # Color by age category
        row=alt.Row('age:N', header=alt.Header(title='Age Category')), # Create separate panes for each age category
        tooltip=[
            alt.Tooltip('company:N', title='Company'),
            alt.Tooltip('original_price:Q', title='Original Price'),
            alt.Tooltip('price:Q', title='Bundled Price'),
            alt.Tooltip('discount:Q', title='Percentage Discount', format='.2f'),
            alt.Tooltip('age:N', title='Age Category')
        ]
    ).properties(
        title=title,
        width=150  # Set the width of each pane
    ).configure_view(
        stroke=None  # Remove the border around each pane to create a seamless view
    ).configure_facet(
        spacing=10  # Adjust the spacing between panes
        
    )

    return chart

# Streamlit sidebar widget for filters
st.sidebar.header('Filters for Bundled Discounts')
st.sidebar.subheader('Filter for Local Categories')
# Filter by Age
selected_ages = st.sidebar.multiselect(
    'Select Age Group:',
    options=bun_data['age'].unique(),
    default=bun_data['age'].unique(),  # Default to all age groups selected
    key='age_select_local'
)

# Filter by Company
selected_attractions = st.sidebar.multiselect(
    'Select Companies:',
    options=bun_data['company'].unique(),
    default=bun_data['company'].unique()[:5],  # Default to top 5 companies selected
    key='company_select_local'
)

# Apply filters to data based on selected age groups, citizenship status, and companies
filtered_data = bun_data[bun_data['age'].isin(selected_ages)]
filtered_data = filtered_data[filtered_data['is_citizen'] == 1]
filtered_data = filtered_data[filtered_data['company'].isin(selected_attractions)]

# Create and display the price comparison chart
discount_bar_chart = create_grouped_discount_bar_chart(filtered_data, 'Discounts by Attraction')
st.altair_chart(discount_bar_chart, use_container_width=True)

st.sidebar.subheader('Filter for Non-Local Categories')
# Filter by Age
selected_ages = st.sidebar.multiselect(
    'Select Age Group:',
    options=bun_data['age'].unique(),
    default=bun_data['age'].unique(),  # Default to all age groups selected
    key='age_select_non_local'
)

# Filter by Company
selected_attractions = st.sidebar.multiselect(
    'Select Companies:',
    options=bun_data['company'].unique(),
    default=bun_data['company'].unique()[:5],  # Default to top 5 companies selected
    key='company_select_non_local'
)

# Apply filters to data based on selected age groups, citizenship status, and companies
filtered_data = bun_data[bun_data['age'].isin(selected_ages)]
filtered_data = filtered_data[filtered_data['is_citizen'] == 0]
filtered_data = filtered_data[filtered_data['company'].isin(selected_attractions)]

# Create and display the price comparison chart
discount_bar_chart = create_grouped_discount_bar_chart(filtered_data, 'Discounts by Attraction')
st.altair_chart(discount_bar_chart, use_container_width=True)

#------------------------------------------------------------------------------#'''
