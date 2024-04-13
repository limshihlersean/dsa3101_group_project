import numpy as np
import pandas as pd
from model import Database # Import the Database class

# Read the CSV file into a DataFrame
data = pd.read_csv('data/NewCableCarPED.csv')

# Group the data by the first two columns (Is_Citizen and Is_Adult)
groups = data.groupby(['Is_Citizen', 'Is_Adult'])

class PEDModel:
    def __init__(self):
        self.db = Database()  # Instantiate the Database class

    def analyze_group(self):
        for group_name, group_df in groups:
            is_citizen, is_adult = group_name
            self._analyze_group(group_df, is_citizen, is_adult)

    def _analyze_group(self, group_df, is_citizen, is_adult):
        prices = group_df['Price'].tolist()
        quantities = group_df['Quantity'].tolist()
        
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

        # Prepare data for database insertion
        data_tuples = list(zip(new_prices[:-1], new_quantities[:-1], PED, revenue[:-1], [is_citizen] * len(new_prices[:-1]), [is_adult] * len(new_prices[:-1])))

        # Insert data into database table
        self.db.insert_data_into_table(data_tuples)

# Instantiate the PEDModel object
# ped_model = PEDModel()

# Analyze each group and store the results in the database
# ped_model.analyze_group()
