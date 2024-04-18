import numpy as np
import pandas as pd
import streamlit as st
import app
import altair as alt

st.set_page_config(layout="wide")

def apply_filters(data, is_citizen_value, is_adult_value):
    if data is not None:
        filtered_data = data[(data['is_citizen'] == is_citizen_value) & (data['is_adult'] == is_adult_value)]
        return filtered_data
    return pd.DataFrame()

def analyze_group(group_df):
    prices = pd.to_numeric(group_df['price'], errors='coerce').dropna()
    quantities = pd.to_numeric(group_df['quantity'], errors='coerce').dropna()
    
    if prices.empty or quantities.empty:
        st.error("Selected group has no data or contains non-numeric values.")
        return

    # Ensure both arrays are the same length
    min_length = min(len(prices), len(quantities))
    prices = prices.iloc[:min_length]
    quantities = quantities.iloc[:min_length]

    # Linear interpolation for the new quantities
    new_prices = np.linspace(min(prices), max(prices), num=100)
    new_quantities = np.interp(new_prices, prices, quantities)

    # Calculating percent changes
    percent_change_quantity = np.diff(new_quantities) / new_quantities[:-1]
    percent_change_price = np.diff(new_prices) / new_prices[:-1]
    PED = percent_change_quantity / percent_change_price
    revenue = new_prices[:-1] * new_quantities[:-1]

    # Finding optimal price and PED
    optimal_price_index = np.argmax(revenue)
    optimal_price = new_prices[optimal_price_index]
    closest_ped_index = np.argmin(np.abs(PED + 1))
    closest_ped_price = new_prices[closest_ped_index]
    closest_ped_revenue = revenue[closest_ped_index]

    # Preparing DataFrame for Altair visualization
    chart_df = pd.DataFrame({
        'Price': np.round(new_prices[:-1], 2),
        'Quantity': np.round(new_quantities[:-1], 2),
        'PED': np.round(PED, 2),
        'Revenue': np.round(revenue, 2)
    })

    # Define color for visibility in dark and light mode
    point_color = 'firebrick'

    # Altair chart for Price vs Quantity
    line_chart = alt.Chart(chart_df).mark_line().encode(
        x=alt.X('Price', title='Price', scale=alt.Scale(domain=(min(chart_df['Price']), max(chart_df['Price'])))),
        y=alt.Y('Quantity', title='Quantity', scale=alt.Scale(domain=(0, max(chart_df['Quantity'])+10))),
        tooltip=['Price', 'Quantity', 'PED', 'Revenue']
    )

    # Solid and smaller circle points on the line chart
    points = line_chart.mark_circle(
        size=50,
        color=point_color,
        opacity=1
    ).encode(
        x='Price',
        y='Quantity'
    )

    # Text annotation for the closest PED point
    text = alt.Chart(pd.DataFrame({
        'x': [closest_ped_price],
        'y': [new_quantities[closest_ped_index]],
        'text': [f'Closest PED: {PED[closest_ped_index]:.2f} at Price {closest_ped_price:.2f}']
    })).mark_text(
        align='left',
        dx=10,  # Nudge text to right so it doesn't overlay the point
        dy=-10,  # Nudge text up to avoid overlap
        fontSize=12,
        color=point_color
    ).encode(
        x='x:Q',
        y='y:Q',
        text='text:N'
    )

    # Combine the line chart, points, and text annotations
    chart = alt.layer(line_chart, points, text).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Displaying results in the app
    st.write(f"Optimal price that maximizes revenue: ${optimal_price:.2f}")
    st.write(f"Price Elasticity of Demand (PED) at the optimal price: {PED[optimal_price_index]:.2f}")

st.title('Price Elasticity of Demand Analysis')

# Selection boxes for filtering
is_citizen_selection = st.selectbox('Citizenship Status', options=['Citizen', 'Non-Citizen'])
is_adult_selection = st.selectbox('Age Group', options=['Adult', 'Child'])

# Mappings
is_citizen_mapping = {'Citizen': 1, 'Non-Citizen': 0}
is_adult_mapping = {'Adult': 1, 'Child': 0}
is_citizen_value = is_citizen_mapping[is_citizen_selection]
is_adult_value = is_adult_mapping[is_adult_selection]

# Processing the backend data
backend_data = app.load_data('ped_data')
filtered_backend_data = apply_filters(backend_data, is_citizen_value, is_adult_value)
if not filtered_backend_data.empty:
    st.write("Filtered Data:")
    st.dataframe(filtered_backend_data, use_container_width=True)
    if st.button('Analyze Filtered Data'):
        analyze_group(filtered_backend_data)
else:
    st.error("No data available for the selected criteria or 'ped_data' not loaded correctly.")
