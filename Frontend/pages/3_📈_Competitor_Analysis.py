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
        x=x_axis,
        y=y_axis,
        color=color_category,
        tooltip=['company', 'city', x_axis, y_axis]
    ).interactive().properties(
        width=300,
        height=300,
        title=title
    )

'''# Function to preprocess the data
def preprocess_data(df):
    # Convert 'Tourist_volume_of_cable_car' to numeric after removing commas
    df['Tourist_volume_of_cable_car'] = df['Tourist_volume_of_cable_car'].str.replace(',', '').astype(float)
    # Additional preprocessing steps...
    return df'''

# Load and preprocess the data
dist_dur_price_data = app.get_distance_duration_price()

# Filters in the sidebar
st.sidebar.header("Filter for Cable Car Price Analysis")
selected_countries = st.sidebar.multiselect(
    'Select Countries',
    options=np.unique(dist_dur_price_data['country']),
    default=np.unique(dist_dur_price_data['country']),
    key='country_select_dist_dur_price'
)

# Filter data based on selection
filtered_data = dist_dur_price_data[dist_dur_price_data['country'].isin(selected_countries)]

# Generate scatter plots
scatter_duration_price = create_scatter_plot(
    filtered_data,
    'duration',
    'cable_car_price',
    'country:N',
    "Duration (Mins) vs. Cable car Price (SGD)"
)

scatter_distance_price = create_scatter_plot(
    filtered_data,
    'distance',
    'cable_car_price',
    'country:N',
    "Distance (KM) vs. Cable car Price (SGD)"
)

# Combine the scatter plots side by side
combined_scatter_plots = alt.hconcat(scatter_duration_price, scatter_distance_price)

# Display the scatter plots
st.altair_chart(combined_scatter_plots, use_container_width=True)

#------------------------------------------------------------------------------#
'''
st.header('Standard Pricing Overview')

def create_price_comparison_chart(data):
    # Melt the dataframe to have a long-form dataframe for Altair
    data_melted = data.melt(id_vars=['Attraction', 'Category'], 
                            value_vars=['Adult Price', 'Senior Price', 'Child Price'],
                            var_name='Ticket Type', value_name='Price')

    # Use facet to create a single row for each ticket type, side by side
    chart = alt.Chart(data_melted).mark_bar().encode(
        x=alt.X('Attraction:N', axis=alt.Axis(title='Attraction')),
        y=alt.Y('Price:Q', axis=alt.Axis(title='Price'), scale=alt.Scale(zero=False)),
        color='Ticket Type:N',
        tooltip=['Attraction', 'Ticket Type', 'Price']
    ).properties(
        title='Competitor Pricing Comparison',
        width=200,  # Adjust the width as needed
        height=200  # Adjust the height as needed
    ).facet(
        column=alt.Column('Ticket Type:N', header=alt.Header(labelAngle=0, titleOrient='top')),
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
pricing_data = load_data('pricing.csv')

# Streamlit sidebar widget for category and attraction selection
st.sidebar.header('Filters for Standard Pricing Overview')
selected_categories = st.sidebar.multiselect(
    'Select Categories:',
    options=pricing_data['Category'].unique(),
    default=pricing_data['Category'].unique(),
    key='category_select_pricing'
)

selected_attractions = st.sidebar.multiselect(
    'Select Attractions:',
    options=pricing_data['Attraction'].unique(),
    default=pricing_data['Attraction'].unique(),
    key='attraction_select_pricing'
)

# Apply filters to pricing_data based on selected categories and attractions
filtered_pricing_data = pricing_data[pricing_data['Category'].isin(selected_categories)]
filtered_pricing_data = filtered_pricing_data[filtered_pricing_data['Attraction'].isin(selected_attractions)]

# Create the price comparison chart using the filtered data
price_comparison_chart = create_price_comparison_chart(filtered_pricing_data)

# Display the chart in the Streamlit app
st.altair_chart(price_comparison_chart, use_container_width=True)

#------------------------------------------------------------------------------#

st.header("Dynamic Pricing Analysis")

def create_dynamic_pricing_chart(data, selected_attractions):
    # Define color scheme for the attractions
    color_scale = alt.Scale(domain=selected_attractions, scheme='category10')

    # Define a unique shape for each age range
    shape_scale = alt.Scale(domain=['Adult', 'Child', 'Senior'],
                            range=['circle', 'square', 'triangle-right'])

    # Define the tooltip content
    tooltip_content = [
        alt.Tooltip('year(Date):T', title='Year'),
        alt.Tooltip('Price:Q', title='Price'),
        alt.Tooltip('Event:N', title='Event'),
        alt.Tooltip('Attraction:N', title='Attraction'),
        alt.Tooltip('Age Range:N', title='Age Range')
    ]

    # Create a base chart to define the legend for attractions
    legend_chart = alt.Chart(data).mark_point().encode(
        color=alt.Color('Attraction:N', scale=color_scale, legend=alt.Legend(title="Attraction")),
        shape=alt.Shape('Age Range:N', scale=shape_scale, legend=alt.Legend(title="Age Range"))
    ).transform_filter(
        alt.datum.Attraction == 'This is a fake filter to hide the points'
    )

    # Initialize an empty list to collect chart layers
    chart_layers = [legend_chart]  # Start with the legend chart

    for attraction in selected_attractions:
        # Filter data for the current attraction
        attraction_data = data[data['Attraction'] == attraction]

        if attraction_data.empty:
            continue  # Skip attractions with no data

        # Loop through the age ranges to create separate line and point charts
        for age_range in ['Adult', 'Child', 'Senior']:
            # Filter data for the current age range within the attraction
            age_range_data = attraction_data[attraction_data['Age Range'] == age_range]

            # Create a line chart for the current age range within the attraction
            lines = alt.Chart(age_range_data).mark_line().encode(
                x='year(Date):T',
                y='Price:Q',
                color=alt.Color('Attraction:N', scale=color_scale, legend=None),
                tooltip=tooltip_content
            )

            # Create points for the line chart
            points = alt.Chart(age_range_data).mark_point(filled=True, size=100).encode(
                x='year(Date):T',
                y='Price:Q',
                shape=alt.Shape('Age Range:N', scale=shape_scale, legend=None),
                color=alt.Color('Attraction:N', scale=color_scale, legend=None),
                tooltip=tooltip_content
            )

            # Add the line and point charts for the current age range as layers
            chart_layers.append(lines + points)

    # Combine all chart layers
    final_chart = alt.layer(*chart_layers).resolve_scale(color='independent') if chart_layers else alt.Chart().mark_text(text='No data to display', align='left')

    return final_chart

# Load the data
dynamic_pricing_data = load_data('dynamic_pricing.csv')

# Convert the 'Date' column to datetime type
dynamic_pricing_data['Date'] = pd.to_datetime(dynamic_pricing_data['Date'].astype(str) + '-01-01')

# Streamlit widget for attraction selection
st.sidebar.header('Filter for Dynamic Pricing Analysis')
selected_attractions = st.sidebar.multiselect(
    'Select Attractions:',
    options=dynamic_pricing_data['Attraction'].unique(),
    default=dynamic_pricing_data['Attraction'].unique()[0]  # Default to first attraction
)

# Display the chart only if at least one attraction is selected
if selected_attractions:
    # Call the function to create the chart
    dynamic_pricing_chart = create_dynamic_pricing_chart(dynamic_pricing_data, selected_attractions)
    # Display the chart
    st.altair_chart(dynamic_pricing_chart, use_container_width=True)
else:
    st.write("Please select at least one attraction to visualize the dynamic pricing data.")

#------------------------------------------------------------------------------#
    
st.header("Local Discounts")

# Load the data
loc_disc_data = load_data('local_discount.csv')  # Update the file name as necessary

# Preprocess the data to ensure correct data types
loc_disc_data['Original Average Price'] = pd.to_numeric(loc_disc_data['Original Average Price'], errors='coerce')
loc_disc_data['Local Average Price'] = pd.to_numeric(loc_disc_data['Local Average Price'], errors='coerce')
loc_disc_data['Percentage Discount'] = pd.to_numeric(loc_disc_data['Percentage Discount'], errors='coerce')

# Filter out any rows with missing data
data = loc_disc_data.dropna(subset=['Original Average Price', 'Local Average Price', 'Percentage Discount'])

# Function to create a horizontal bar chart
def create_local_discount_bar_chart(data, title):
    # Horizontal bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Percentage Discount:Q', title='Percentage Discount'),
        y=alt.Y('Attraction:N', sort='-x', title=''),  # Sort bars by discount percentage
        color=alt.Color('Attraction:N'),  # Color by attraction
        tooltip=[
            alt.Tooltip('Attraction:N', title='Attraction'),
            alt.Tooltip('Original Average Price:Q', title='Original Price'),
            alt.Tooltip('Local Average Price:Q', title='Local Price'),
            alt.Tooltip('Percentage Discount:Q', title='Discount', format='.2f')
        ]
    ).properties(title=title, height=300)  # Set the height to ensure that all bars are visible
    return chart

# Streamlit sidebar widget for attraction selection
st.sidebar.header('Filter for Local Discounts')
selected_attractions = st.sidebar.multiselect(
    'Select Attractions:',
    options=loc_disc_data['Attraction'].unique(),
    default=loc_disc_data['Attraction'].unique(),  # Default to all attractions selected
    key='attraction_select_local'
)

# Apply filters to data based on selected attractions
filtered_data = loc_disc_data[loc_disc_data['Attraction'].isin(selected_attractions)]

# Create and display the price comparison chart
local_discount_bar_chart = create_local_discount_bar_chart(filtered_data, 'Local Discounts by Attraction')
st.altair_chart(local_discount_bar_chart, use_container_width=True)

#------------------------------------------------------------------------------#
st.header("Bundled Discounts")

# Load the data
bun_data = load_data('bundled_discount.csv')  # Make sure the file name matches your CSV

# Preprocess the data to ensure correct data types
bun_data['Original Average Price'] = pd.to_numeric(bun_data['Original Average Price'], errors='coerce')
bun_data['Bundled Average Price'] = pd.to_numeric(bun_data['Bundled Average Price'], errors='coerce')
bun_data['Percentage Discount'] = pd.to_numeric(bun_data['Percentage Discount'], errors='coerce')

# Filter out any rows with missing data
data = bun_data.dropna(subset=['Original Average Price', 'Bundled Average Price', 'Percentage Discount'])

# Create a horizontal bar chart function
def create_discount_bar_chart(data, title):
    # Horizontal bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Percentage Discount:Q', title='Percentage Discount'),
        y=alt.Y('Attraction:N', sort='-x', title=''),  # Sort bars by discount percentage
        color=alt.Color('Attraction:N'),  # Color by attraction
        tooltip=[
            alt.Tooltip('Attraction:N', title='Attraction'),
            alt.Tooltip('Original Average Price:Q', title='Original Price'),
            alt.Tooltip('Bundled Average Price:Q', title='Bundled Price'),
            alt.Tooltip('Percentage Discount:Q', title='Discount', format='.2f')
        ]
    ).properties(title=title, height=300)  # Set the height to ensure that all bars are visible
    return chart

# Streamlit sidebar widget for attraction selection
st.sidebar.header('Filter for Bundled Discounts')
selected_attractions = st.sidebar.multiselect(
    'Select Attractions:',
    options=bun_data['Attraction'].unique(),
    default=bun_data['Attraction'].unique(),  # Default to all attractions selected
    key='attraction_select_bundled'
)

# Apply filters to data based on selected attractions
filtered_data = bun_data[bun_data['Attraction'].isin(selected_attractions)]

# Create and display the price comparison chart
discount_bar_chart = create_discount_bar_chart(filtered_data, 'Discounts by Attraction')
st.altair_chart(discount_bar_chart, use_container_width=True)

#------------------------------------------------------------------------------#'''
