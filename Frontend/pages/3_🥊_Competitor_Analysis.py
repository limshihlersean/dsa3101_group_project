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

# Define navigation
option = st.sidebar.selectbox(
    'Choose a section',
    ('Cable Car Price Analysis', 'Standard Pricing Overview', 'Dynamic Pricing Chart', 'Local Discounts', 'Bundled Discounts')
)

# Import and call functions dynamically based on user choice
if option == 'Cable Car Price Analysis':
    from competitor_analysis.cable_car_price import display_chart
elif option == 'Standard Pricing Overview':
    from competitor_analysis.standard_pricing import display_chart
elif option == 'Dynamic Pricing Chart':
    from competitor_analysis.dynamic_pricing import display_chart
elif option == 'Local Discounts':
    from competitor_analysis.local_discount import display_chart
elif option == 'Bundled Discounts':
    from competitor_analysis.bundled_discount import display_chart
display_chart()

#------------------------------------------------------------------------------#
