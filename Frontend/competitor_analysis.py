# Required Libraries
import streamlit as st
import pandas as pd
import altair as alt
import os

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

# Visualization for Competitor Pricing Comparison
def create_price_comparison_chart(data, title):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Attraction:N', axis=alt.Axis(title='Attraction')),
        y=alt.Y('Adult_Price:Q', axis=alt.Axis(title='Average Adult Price')),
        color='Attraction:N',
        tooltip=['Attraction:N', 'Adult_Price:Q', 'Child_Price:Q']
    ).properties(title=title)
    return chart

# Load the data
pricing_data = load_data('pricing.csv')

# Ensure the data types are correct
pricing_data['Adult_Price'] = pd.to_numeric(pricing_data['Adult_Price'], errors='coerce')
pricing_data['Child_Price'] = pd.to_numeric(pricing_data['Child_Price'], errors='coerce')

# Handle any missing or erroneous data if necessary
# For example, dropping rows where the price is NaN after conversion
pricing_data = pricing_data.dropna(subset=['Adult_Price', 'Child_Price'])

# Streamlit sidebar widget for category selection
st.sidebar.header('Filters for Pricing Comparison')
selected_categories = st.sidebar.multiselect(
    'Select categories:',
    options=pricing_data['Category'].unique(),  # This should be the list of all categories available in the data
    default=pricing_data['Category'].unique()   # Default to all categories selected
)

# Apply filters to pricing_data based on selected categories
filtered_pricing_data = pricing_data[pricing_data['Category'].isin(selected_categories)]


# Create the price comparison chart using the filtered data
price_comparison_chart = create_price_comparison_chart(
    filtered_pricing_data, 
    'Competitor Pricing Comparison'
)

# Display the chart in the Streamlit app
st.header('Competitor Pricing Comparison')
st.altair_chart(price_comparison_chart, use_container_width=True)



#------------------------------------------------------------------------------#


def create_price_differentiation_chart(data, chart_type):
    # Filter data for the chosen chart type
    filtered_data = data[data['Chart_Type'] == chart_type]

    # Check if the filtered data is empty
    if filtered_data.empty:
        st.error('No data available for the selected chart type.')
        return None

    # Create the pie chart using the 'Count' for the size of pie slices
    chart = alt.Chart(filtered_data).mark_arc().encode(
        theta='Count:Q',  # Size of pie slice based on the count
        color=alt.Color('Category:N', legend=alt.Legend(title="Category")),  # Color by category
        tooltip=['Category:N', 'Count:Q']  # Show tooltip on hover
    ).properties(
        title=f'Price Differentiation: {chart_type}'
    )

    return chart


# Load the data
differentiation_data = load_data('differentiation.csv')

# Ensure 'Count' is a float
differentiation_data['Count'] = pd.to_numeric(differentiation_data['Count'], errors='coerce')
if differentiation_data['Count'].isnull().any():
    st.error('Some count values could not be converted to numeric.')

# Sidebar for Chart_Type selection
chart_type_selection = st.sidebar.selectbox(
    'Select Chart Type:',
    options=differentiation_data['Chart_Type'].unique(),
)

# Generate and display the chart if the data is valid
price_differentiation_chart = create_price_differentiation_chart(differentiation_data, chart_type_selection)
if price_differentiation_chart:
    st.altair_chart(price_differentiation_chart, use_container_width=True)
else:
    st.write("No valid chart data available for the selected type.")
