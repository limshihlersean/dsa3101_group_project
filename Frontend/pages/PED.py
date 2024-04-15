import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import app
import streamlit as st

data = app.load_data('ped_data')

def analyze_group(group_df):
    prices = group_df['price'].tolist()
    quantities = group_df['quantity'].tolist()
    
    if len(prices) == 0 or len(quantities) == 0:
        st.error("Selected group has no data.")
        return

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

# Streamlit page setup
st.title('Price Elasticity of Demand Analysis')

# User selection of groups using Streamlit's selectbox
is_citizen_selection = st.selectbox('Citizenship Status', options=['Citizen', 'Non-Citizen'], format_func=lambda x: 'Yes' if x == 'Citizen' else 'No')
is_adult_selection = st.selectbox('Age Group', options=['Adult', 'Child'], format_func=lambda x: 'Yes' if x == 'Adult' else 'No')

# Filter data based on user selection
filtered_group = data[(data['is_citizen'] == (is_citizen_selection == 'Citizen')) & (data['is_adult'] == (is_adult_selection == 'Adult'))]

# Button to trigger the analysis
if st.button('Analyze'):
    analyze_group(filtered_group)


'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Read the CSV file into a DataFrame
data = pd.read_csv('../data/NewCableCarPED.csv')

# Group the data by the first two columns (Is_Citizen and Is_Adult)
groups = data.groupby(['is_citizen', 'is_adult'])

# Define a function to calculate PED, find optimal price, create graph, and table for each group
def analyze_group(group_df, is_citizen, is_adult):
    prices = group_df['price'].tolist()
    quantities = group_df['quantity'].tolist()
    
    # Interpolate between existing data points
    new_prices = np.arange(min(prices), max(prices) + 1)  # Generate new price points as integers from min to max

    # Interpolate quantities for new price points
    new_quantities = np.interp(new_prices, prices, quantities)

    # Calculate percentage change in quantity demanded
    percent_change_quantity = np.diff(new_quantities) / new_quantities[:-1]

    # Calculate percentage change in price
    percent_change_price = np.diff(new_prices) / new_prices[:-1]

    # Calculate PED
    PED = percent_change_quantity / percent_change_price

    # Calculate revenue
    revenue = new_prices * new_quantities

    # Find price that maximizes revenue
    optimal_price_index = np.argmax(revenue)
    optimal_price = new_prices[optimal_price_index]

    # Find the price point with PED closest to -1
    closest_ped_index = np.argmin(np.abs(np.abs(PED) - 1))
    closest_ped_price = new_prices[closest_ped_index]
    closest_ped_revenue = revenue[closest_ped_index]

    # Create a DataFrame to display the results
    results_df = pd.DataFrame({
        "Price": new_prices[:-1],  # Exclude the last price point to match the size of other arrays
        "Quantity": new_quantities[:-1],  # Exclude the last quantity value to match the size of other arrays
        "PED": PED,
        "Revenue": revenue[:-1]  # Exclude the last revenue value to match the size of other arrays
    })

    # Display the results table in Streamlit
    st.write("Results Table:")
    st.dataframe(results_df)

    # Plot the price vs quantity graph
    plt.figure(figsize=(10, 6))
    plt.plot(new_prices[:-1], new_quantities[:-1], marker='o', linestyle='-', color='b')
    plt.title("Price vs Quantity")
    plt.xlabel("Price")
    plt.ylabel("Quantity")
    plt.grid(True)

    # Create and display the price vs quantity graph in Streamlit
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... (existing code to create the plot)
    
    st.pyplot(fig)

    # Display the optimal price and PED in Streamlit
    st.write(f"Optimal price that maximizes revenue: {optimal_price}")
    st.write(f"Price Elasticity of Demand (PED) at the optimal price: {PED[optimal_price_index]}")

    # Annotate the price point closest to PED = -1
    plt.annotate(f'Price Point for closest |PED| to 1: ${closest_ped_price}\nTotal Revenue: ${closest_ped_revenue}', 
                 xy=(closest_ped_price, new_quantities[closest_ped_index]), 
                 xytext=(closest_ped_price + 5, new_quantities[closest_ped_index] + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=10
                )

    # Annotate the group
    group_label = f"{'Citizen' if is_citizen else 'Non-Citizen'}, {'Adult' if is_adult else 'Child'}"
    plt.annotate(group_label, xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12)

    plt.show()

    # Print the optimal price and PED
    print("\nOptimal price that maximizes revenue:", optimal_price)
    print("Price Elasticity of Demand (PED) at the optimal price:", PED[optimal_price_index])

# Iterate over each group and analyze it
for group_name, group_df in groups:
    print(f"\nGroup: {group_name}")
    is_citizen, is_adult = group_name
    analyze_group(group_df, is_citizen, is_adult)

# Streamlit page setup
st.title('Price Elasticity of Demand Analysis')

# User selection of groups using Streamlit's selectbox
is_citizen_selection = st.selectbox('Citizenship Status', options=['Citizen', 'Non-Citizen'])
is_adult_selection = st.selectbox('Age Group', options=['Adult', 'Child'])

# Filter data based on user selection
filtered_group = data[(data['is_citizen'] == is_citizen_selection) & (data['is_adult'] == is_adult_selection)]

# Button to trigger the analysis
if st.button('Analyze'):
    analyze_group(filtered_group, is_citizen_selection == 'Citizen', is_adult_selection == 'Adult')
'''