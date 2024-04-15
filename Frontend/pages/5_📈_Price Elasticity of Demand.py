import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import app

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

    # Ensure both arrays are the same length by limiting them to the shorter length
    min_length = min(len(prices), len(quantities))
    prices = prices.iloc[:min_length].tolist()
    quantities = quantities.iloc[:min_length].tolist()

    new_prices = np.arange(min(prices), max(prices) + 1)
    new_quantities = np.interp(new_prices, prices, quantities)

    # Calculate percent changes
    if len(new_quantities) > 1:
        percent_change_quantity = np.diff(new_quantities) / new_quantities[:-1]
        percent_change_price = np.diff(new_prices) / new_prices[:-1]
        PED = percent_change_quantity / percent_change_price
        revenue = new_prices[:-1] * new_quantities[:-1]

        if revenue.size > 0:
            optimal_price_index = np.argmax(revenue)
            optimal_price = new_prices[optimal_price_index]
            closest_ped_index = np.argmin(np.abs(PED + 1))  # Finding PED closest to -1
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
        else:
            st.error("No valid revenue data to analyze.")
    else:
        st.error("Not enough data points to calculate changes and elasticity.")

st.title('Price Elasticity of Demand Analysis')

is_citizen_selection = st.selectbox('Citizenship Status', options=['Citizen', 'Non-Citizen'])
is_adult_selection = st.selectbox('Age Group', options=['Adult', 'Child'])
is_citizen_mapping = {'Citizen': 1, 'Non-Citizen': 0}
is_adult_mapping = {'Adult': 1, 'Child': 0}
is_citizen_value = is_citizen_mapping[is_citizen_selection]
is_adult_value = is_adult_mapping[is_adult_selection]

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type.lower() == 'csv':
        dataframe = pd.read_csv(uploaded_file)
    elif file_type.lower() == 'xlsx':
        dataframe = pd.read_excel(uploaded_file)

    filtered_uploaded_data = apply_filters(dataframe, is_citizen_value, is_adult_value)
    if st.button('Analyze Uploaded Data'):
        if not filtered_uploaded_data.empty:
            analyze_group(filtered_uploaded_data)
        else:
            st.error("No data available for the selected criteria.")
else:
    backend_data = app.load_data('ped_data')
    filtered_backend_data = apply_filters(backend_data, is_citizen_value, is_adult_value)
    if not filtered_backend_data.empty:
        st.write("Filtered Data:")
        st.dataframe(filtered_backend_data)
        if st.button('Analyze Filtered Data'):
            analyze_group(filtered_backend_data)
    else:
        st.error("No data available for the selected criteria or 'ped_data' not loaded correctly.")

