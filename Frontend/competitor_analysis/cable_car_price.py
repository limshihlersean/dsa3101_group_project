import streamlit as st
import numpy as np
import altair as alt
import app  # assuming 'app' is a module for handling data operations

def display_chart():
    st.header("Cable Car Price Analysis")

    st.write("The cable car price analysis features two scatterplots: Duration Vs Cable Car Price and Distance Vs Cable Car Price. These visualizations enable the exploration of potential pricing patterns in cable car fares across various countries, selectable through a sidebar.")

    # Function to create scatter plot
    def create_scatter_plot(data, x_axis, y_axis, color_category, x_title, y_title, title):
        return alt.Chart(data).mark_circle(size=60).encode(
            x=alt.X(x_axis, title=x_title),
            y=alt.Y(y_axis, title=y_title, type='quantitative',axis=alt.Axis(format='$.2f')),
            color=color_category,
            tooltip=[
                alt.Tooltip('country:N',title='Country'),
                alt.Tooltip('company:N', title='Company'),
                alt.Tooltip('city:N', title='City'),
                alt.Tooltip(x_axis + ':Q', title=x_title),
                alt.Tooltip(y_axis + ':Q', title=y_title, format='$.2f')  # Format price to two decimal places
            ]
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

    if len(filtered_data):
        # Generate scatter plots
        scatter_duration_price = create_scatter_plot(
            filtered_data,
            'duration',
            'price',
            'country:N',
            "Duration (Mins)",
            "Cable car Price (SGD)",
            "Duration (Mins) vs. Cable car Price (SGD)"
        )
        scatter_distance_price = create_scatter_plot(
            filtered_data,
            'distance',
            'price',
            'country:N',
            "Distance (KM)",
            "Cable car Price (SGD)",
            "Distance (KM) vs. Cable car Price (SGD)"
        )
        # Combine the scatter plots side by side
        combined_scatter_plots = alt.hconcat(scatter_duration_price, scatter_distance_price)
        # Display the scatter plots
        st.altair_chart(combined_scatter_plots, use_container_width=True)
    else:
        st.write("Please select at least one category to visualize the Cable Car Price Analysis.")
