# Frontend Development README

## Project Overview

This project focuses on developing a comprehensive dashboard for Mount Faber Leisure Group (MFLG) to analyze cable car pricing strategies and optimize prices for their offerings. The frontend development plays a crucial role in delivering an intuitive and visually appealing user interface for accessing and interacting with analytical insights.

## Usage Guide

The frontend dashboard provides various features for analyzing competitor pricing and optimizing cable car prices. Here's how to use it:

1. **Data Input Interface**: 
The dashboard facilitates dataset uploads through the intuitive Upload page, allowing users to upload their datasets easily. With simplified file browsing and built-in data validation, users can easily select their files and ensure data integrity before uploading. Additionally, the Update page enhances backend dataset management by streamlining access and enabling effortless deletion of rows. This functionality simplifies data maintenance tasks, allowing users to efficiently update and manage their datasets as needed.

2. **Competitor Analysis Page**:
The Competitor Analysis Page offers an extensive set of cable car pricing visualizations, providing users with valuable insights into various pricing strategies. These visualizations encompass Cable Car Price Analysis, Standard Pricing Overview, Dynamic Pricing Chart, Local Discount, and Bundled Discount. Users can explore these visualizations to gain a holistic understanding of pricing dynamics within the cable car industry. Moreover, the page incorporates interactive features such as real-time interactive filtering and on-hover information, enhancing the user experience and facilitating deeper analysis of pricing data.

3. **Price Optimised Pages**:
The Price Optimization feature allows users to calculate optimal pricing for old cable car rides by prominently displaying parameters for easy input by the user and price calculation.

### app.py
The app.py file serves as the backbone of a Streamlit web application designed to facilitate the interaction with a backend API for data management tasks. 
Its primary objective is to empower users with functionalities to load, update, and potentially delete data stored in the backend database. 
Leveraging Streamlit's intuitive interface, the app provides a user-friendly environment for accessing and manipulating datasets. 

### requirements.txt
To manage and specify dependencies required for frontend

### Dockerfile 
This Dockerfile is creating an environment to run a Streamlit web application. It copies the project files into the container, installs the required dependencies specified in the requirements.txt file, exposes port 8501 for accessing the Streamlit application, and runs the Streamlit application specified by 1_🏡_Home.py when the container is launched.

To build a Docker image using the provided Dockerfile, follow these instructions:
1) Use a Python base image
2) Set working directory in the container
3) Copy the current directory contents into the container at app
4) Install any needed packages specified in requirements.txt
5) Make port 8501 available to the world outside this container
6) Run Home.py when the container launches



