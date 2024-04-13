import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import app
import streamlit as st

# Load the data
data = app.load_data('ped_data')

def analyze_group(group_df):
    # Convert prices and quantities to numeric, coerce errors to NaN, then drop NaN values
    prices = pd.to_numeric(group_df['price'], errors='coerce').dropna().tolist()
    quantities = pd.to_numeric(group_df['quantity'], errors='coerce').dropna().tolist()
    
    # Check if there are valid price and quantity values to analyze
    if not prices or not quantities:
        st.error("Selected group has no data or contains non-numeric values.")
        return

    # Create new prices array for interpolation
    new_prices = np.arange(min(prices), max(prices) + 1)
    new_quantities = np.interp(new_prices, prices, quantities)

    # Calculate percentage changes
    percent_change_quantity = np.diff(new_quantities) / new_quantities[:-1]
    percent_change_price = np.diff(new_prices) / new_prices[:-1]
    PED = percent_change_quantity / percent_change_price

    # Calculate revenue
    revenue = new_prices[:-1] * new_quantities[:-1]
    optimal_price_index = np.argmax(revenue)
    optimal_price = new_prices[optimal_price_index]
    closest_ped_index = np.argmin(np.abs(np.abs(PED) - 1))
    closest_ped_price = new_prices[closest_ped_index]
    closest_ped_revenue = revenue[closest_ped_index]

    results_df = pd.DataFrame({
        "Price": new_prices[:-1],
        "Quantity": new_quantities[:-1],
        "PED": PED,
        "Revenue": revenue
    })

    st.write("Results Table:")
    st.dataframe(results_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(new_prices[:-1], new_quantities[:-1], marker='o', linestyle='-', color='b')
    ax.set_title("Price vs Quantity")
    ax.set_xlabel("Price")
    ax.set_ylabel("Quantity")
    ax.grid(True)
    ax.annotate(f'Closest PED to -1: ${closest_ped_price}\nRevenue: ${closest_ped_revenue}', 
                xy=(closest_ped_price, new_quantities[closest_ped_index]), 
                xytext=(closest_ped_price + 5, new_quantities[closest_ped_index] + 10),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=10)
    st.pyplot(fig)

    st.write(f"Optimal price that maximizes revenue: {optimal_price}")
    st.write(f"Price Elasticity of Demand (PED) at the optimal price: {PED[optimal_price_index]}")

st.title('Price Elasticity of Demand Analysis')

is_citizen_selection = st.selectbox('Citizenship Status', options=[1, 0])
is_adult_selection = st.selectbox('Age Group', options=[1, 0])

# Initialize an empty DataFrame as a fallback
filtered_group = pd.DataFrame()

if data is not None:
    # Filter data based on user selection
    filtered_group = data[(data['is_citizen'] == is_citizen_selection) & (data['is_adult'] == is_adult_selection)]

    if not filtered_group.empty:
        st.write("Filtered Data:")
        st.dataframe(filtered_group)
    else:
        st.error("No data available for the selected criteria.")

if st.button('Analyze'):
    if not filtered_group.empty:
        analyze_group(filtered_group)
    else:
        st.error("Selected group has no data.")
