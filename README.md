# DSA3101 Group Project By Team Vamos


## Table of Contents
1. [Introduction and Overview](#introduction-and-overview)
2. [Purpose of the Document](#purpose-of-the-document)
3. [Overview of Content](#overview-of-content)
4. [Repository Structure](#repository-structure)
5. [Frontend Features](#frontend-features)
6. [Backend Features](#backend-features)
7. [Installation and Usage](#installation-and-usage)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction and Overview

### Purpose of the Document
The purpose of this document is to provide an overview of the MFLG project, detailing its objectives, features, and repository structure. It is intended for stakeholders, project managers, developers, and anyone interested in understanding the project's scope and organization.

### Overview of Content
1. Introduction and Overview
2. Repository Structure
3. Frontend Features
4. Backend Features
5. Conclusion

## Repository Structure
The code repository for the MFLG project is structured as follows:

- **frontend:** Contains the frontend code for the MFLG project.
- **backend:** Contains the backend code for the MFLG project.
- **data** Contains intialization of database script

## Frontend Features

### Data Input Interface
* **Description:**
Provides a user-friendly interface for inputting data into the application.
* **Key Functionality:**
Allows users to enter data relevant to the application, such as ticket information, company details, and pricing data.
Offers input validation to ensure data accuracy and integrity.
Supports file upload.

### Competitor Analysis Page with Interactive Features
* **Description:**
Enables users to perform competitor analysis and visualize data in an interactive manner.
* **Key Functionality:**
Presents data-driven insights and visualizations to facilitate competitive analysis.
Offers interactive charts, graphs, and tables for exploring competitor data.
Provides filtering, sorting, and comparison features to identify key trends, strengths, and weaknesses of competitors.
Supports customization options to tailor analysis based on user preferences and requirements.

### Price Optimization Pages
* **Description:**
Allows users to vary input parameters to query the model and receive an optimized price.
* **Key Functionality:**
Enables users to adjust input parameters such as adult/child, citizen/noncitzen, duration, distance and weather conditions etc.
Utilizes a model or algorithm to process the input parameters and generate an optimized price recommendation.
Supports scenario analysis and what-if simulations to explore different pricing strategies and their potential outcomes.

### Data Validation Methods
* **Description:**
Ensures the integrity and validity of data entered into the application.
* **Key Functionality:**
Implements validation logic to verify the correctness and completeness of user inputs.
Validates data against predefined rules, formats, or constraints to prevent errors or inconsistencies.
Handles edge cases and boundary conditions to maintain data quality and reliability.
Provides feedback and error messages to users to assist in correcting invalid or erroneous inputs.

## Backend Features

### Database
* **Description:**
Manages the storage and retrieval of application data.
* **Key Functionality:**
Utilizes MySQL as the database management system to store structured data.
Defines tables and relationships to organize and represent data entities.
Supports CRUD (Create, Read, Update, Delete) operations to interact with data stored in the database.
Ensures data integrity and consistency through constraints, indexes, and foreign key relationships.

### Price Optimization Model
* **Description:**
Utilizes algorithms or machine learning models to optimize pricing strategies.
* **Key Functionality:**
Analyzes historical data and other relevant factors to generate price recommendations.
Provides insights and recommendations to help users make informed decisions about pricing adjustments.

### RESTful APIs with Flask
* **Description:**
Provides endpoints and routes to handle HTTP requests and serve data to the frontend.
* **Key Functionality:**
Implements RESTful APIs using Flask, a lightweight web framework for Python.
Defines routes to handle different types of requests, such as GET, POST, and DELETE.
Processes incoming requests, interacts with the database, and returns data or responses to the client.
Enables communication between the frontend and backend components of the application.

### Data Validation Methods
* **Description:**
Ensures the integrity and validity of data entered into the application.
* **Key Functionality:**
Implements validation logic to verify the correctness and completeness of user inputs.
Validates data against predefined rules, formats, or constraints to prevent errors or inconsistencies.
Handles edge cases and boundary conditions to maintain data quality and reliability.
Provides feedback and error messages to users to assist in correcting invalid or erroneous inputs.


### Conclusion
The MFLG project leverages data-driven analytics to optimize cable car pricing strategies. With features like the Data Input Interface, Competitor Analysis, Price Optimization Interface, data validation methods and models, it offers a comprehensive solution for strategic price optimization. The structured organization of the frontend and backend components promotes ease of maintenance, scalability, and future enhancements to the pricing prediction system.

For further details or inquiries, please refer to the project repository or contact the project team.


## Installation and Usage

To run/test the app locally, follow these step-by-step instructions:

**Step 1:** Clone Git Repo
Clone this Git repository containing the application source code to your local machine.

**Step 2:** Create a Virtual Environment
Set up a virtual environment for the application to ensure isolated dependencies.

**Step 3:** Start Docker Compose
Open a terminal and navigate to the root directory of the cloned repository.
Run the following command to start Docker Compose:
```bash
docker-compose up
```
**Step 4:** Wait for Docker Containers
Wait for Docker to create the necessary containers for the application.

<img width="1205" alt="Screenshot 2024-04-26 at 10 20 21 AM" src="https://github.com/limshihlersean/dsa3101_group_project/assets/98541932/b9244ef5-2f70-444c-b9e4-0f5d160fb208">

Once it says “Connected to MySQL server successfully!!!!”,  go to step 5.

**Step 5:** Access the Dashboard
Open your web browser (Chrome/Safari) and type the following URL in the address bar:
```bash
localhost:8501
```

**Step 6:** Use the Dashboard
Once the page loads, you can interact with the dashboard to explore its features and functionalities.

Dependencies will be automatically installed through the Dockerfile, which references the requirements.txt file.

To run the deployed app, follow these step-by-step instructions:

**Step 1:** 
SSH into the EC2 Instance called “Team_Vamos” on research.rlcatalyst website using the following commands:
```bash
ssh -i /path/to/private_key.pem -L 8501:localhost:8501 ec2-user@ec2-instance-public-dns
```

**Step 2:**
If the app is not already running, run the following commands:

```bash
cd dsa3101_group_project
docker-compose up
```

**Step 3:**
Open your web browser (Chrome/Safari) and type the following URL in the address bar: localhost:8501

**Step 4:**
Once the page loads, you can interact with the dashboard to explore its features and functionalities.


## Contributing

We welcome contributions from the community to improve the project. Here's how you can contribute:

### Bug Reports and Feature Requests
If you encounter any bugs or have ideas for new features, please [open an issue](https://github.com/your-username/your-project/issues) on GitHub. Provide detailed information about the bug or feature request, including steps to reproduce the issue if applicable.

### Code Contributions
1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make changes to the codebase.
5. Commit your changes:
```bash
git commit -m 'Add new feature or fix bug'
```
6. Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```
7. Submit a pull request (PR) to the main repository's main branch. Provide a clear description of your changes and why they are needed.

