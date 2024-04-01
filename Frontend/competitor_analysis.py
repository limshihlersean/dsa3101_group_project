# Required Libraries
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np

# Load CSV data
def load_data(filename):
    # Construct the full path to the file within the 'data' folder
    # The '..' moves up one directory level from the current script's location
    folder_path = os.path.join('..', 'data')
    full_path = os.path.join(folder_path, filename)
    
    # Load and return the CSV file
    return pd.read_csv(full_path)

#To show the title of Dashboard
st.title('Competitor Analysis Dashboard')

def create_dynamic_pricing_chart(data, selected_attractions):
    # Define the tooltip content
    tooltip_content = [
        alt.Tooltip('year(Date):T', title='Year'),
        alt.Tooltip('Price:Q', title='Price'),
        alt.Tooltip('Event:N', title='Event'),
        alt.Tooltip('Attraction:N', title='Attraction')
    ]

    # Initialize an empty list to collect chart layers
    chart_layers = []

    # Define color scheme for the age ranges
    color_scale = alt.Scale(domain=['Adult', 'Child', 'Senior'],
                            range=['blue', 'orange', 'green'])

    # Loop through the selected attractions
    for attraction in selected_attractions:
        # Filter data for the current attraction
        attraction_data = data[data['Attraction'] == attraction]

        if attraction_data.empty:
            continue  # Skip attractions with no data

        # Create a line chart for the current attraction
        lines = alt.Chart(attraction_data).mark_line().encode(
            x=alt.X('year(Date):T', title='Year'),
            y=alt.Y('Price:Q', title='Price'),
            color=alt.Color('Age Range:N', scale=color_scale, legend=alt.Legend(title="Age Range")),
            tooltip=tooltip_content
        ).properties(
            title=f'Dynamic Pricing Models: {attraction}'
        )

        # Create points for the line chart
        points = alt.Chart(attraction_data).mark_point().encode(
            x='year(Date):T',
            y='Price:Q',
            color=alt.Color('Age Range:N', scale=color_scale),
            tooltip=tooltip_content
        )

        # Combine line chart with points and add to the list of layers
        chart_layers.append(lines + points)

    # Combine all chart layers
    final_chart = alt.layer(*chart_layers) if chart_layers else alt.Chart().mark_text(text='No data to display', align='left')

    # Return the combined chart
    return final_chart

# Load the data
dynamic_pricing_data = load_data('dynamic_pricing.csv')

# Convert the 'Date' column to datetime type
dynamic_pricing_data['Date'] = pd.to_datetime(dynamic_pricing_data['Date'].astype(str) + '-01-01')

# Streamlit widget for attraction selection
st.sidebar.header('Select Attractions for Visualization')
selected_attractions = st.sidebar.multiselect(
    'Select attractions:',
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




#------------------------------------------------------------------------------#

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
st.sidebar.header('Select Attractions for Visualization')
selected_attractions = st.sidebar.multiselect(
    'Select attractions:',
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
st.sidebar.header('Select Attractions for Visualization')
selected_attractions = st.sidebar.multiselect(
    'Select attractions:',
    options=bun_data['Attraction'].unique(),
    default=bun_data['Attraction'].unique(),  # Default to all attractions selected
    key='attraction_select_bundled'
)

# Apply filters to data based on selected attractions
filtered_data = bun_data[bun_data['Attraction'].isin(selected_attractions)]

# Create and display the price comparison chart
discount_bar_chart = create_discount_bar_chart(filtered_data, 'Discounts by Attraction')
st.altair_chart(discount_bar_chart, use_container_width=True)



#------------------------------------------------------------------------------#


# Function to create scatter plot
def create_scatter_plot(data, x_axis, y_axis, color_category, title):
    return alt.Chart(data).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color=color_category,
        tooltip=['Company', 'City', x_axis, y_axis]
    ).interactive().properties(
        width=300,
        height=300,
        title=title
    )

# Function to preprocess the data
def preprocess_data(df):
    # Convert 'Tourist_volume_of_cable_car' to numeric after removing commas
    df['Tourist_volume_of_cable_car'] = df['Tourist_volume_of_cable_car'].str.replace(',', '').astype(float)
    # Additional preprocessing steps...
    return df

# Load and preprocess the data
dist_dur_price_data = load_data('distance_duration_price.csv')
dist_dur_price_data = preprocess_data(dist_dur_price_data)

# Filters in the sidebar
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    'Select Countries',
    options=np.unique(dist_dur_price_data['Country']),
    default=np.unique(dist_dur_price_data['Country']),
    key='country_select_dist_dur_price'
)

# Filter data based on selection
filtered_data = dist_dur_price_data[dist_dur_price_data['Country'].isin(selected_countries)]

# Generate scatter plots
scatter_duration_price = create_scatter_plot(
    filtered_data,
    'Duration (Mins)',
    'Cable car Price (SGD)',
    'Country:N',
    "Duration (Mins) vs. Cable car Price (SGD)"
)

scatter_distance_price = create_scatter_plot(
    filtered_data,
    'Distance (KM)',
    'Cable car Price (SGD)',
    'Country:N',
    "Distance (KM) vs. Cable car Price (SGD)"
)

# Combine the scatter plots side by side
combined_scatter_plots = alt.hconcat(scatter_duration_price, scatter_distance_price)

# Display the scatter plots
st.header("Interactive Scatter Plots")
st.altair_chart(combined_scatter_plots, use_container_width=True)

#------------------------------------------------------------------------------#

# Visualization for Competitor Pricing Comparison
def create_price_comparison_chart(data):
    # Melt the dataframe to have a long-form dataframe for Altair
    data_melted = data.melt(id_vars=['Attraction', 'Category'], 
                            value_vars=['Adult Price', 'Senior Price', 'Child Price'],
                            var_name='Ticket Type', value_name='Price')

    chart = alt.Chart(data_melted).mark_bar().encode(
        x=alt.X('Attraction:N', axis=alt.Axis(title='Attraction')),
        y=alt.Y('Price:Q', axis=alt.Axis(title='Price')),
        color='Ticket Type:N',
        column='Ticket Type:N',
        tooltip=['Attraction', 'Ticket Type', 'Price']
    ).properties(
        title='Competitor Pricing Comparison'
    )
    return chart

# Load the data
pricing_data = load_data('pricing.csv')

# Streamlit sidebar widget for category and attraction selection
st.sidebar.header('Filters for Pricing Comparison')
selected_categories = st.sidebar.multiselect(
    'Select categories:',
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
st.header('Competitor Pricing Comparison')
st.altair_chart(price_comparison_chart, use_container_width=True)