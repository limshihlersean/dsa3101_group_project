# DSA3101 Group Project


## Table of Contents
1. [Introduction and Overview](#introduction-and-overview)
2. [Repository Structure](#repository-structure)
3. [Frontend Features](#frontend-features)
4. [Backend Features](#backend-features)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

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


- **backend:** Contains the backend code for the MFLG project.
  - **Controller:** Houses the Flask server routes for managing interactions between the client-side interface and server-side functionality.
  - **Model:** Facilitates accurate pricing predictions and handles the MySQL database.
  - **Services:** Ensures reliability and consistency of data used in the cable car pricing prediction system.
- **frontend:** Contains the frontend code for the MFLG project.
  - **components:** Vue.js components representing different pages of the dashboard interface.
  - **assets:** Contains static assets such as images.
  - **App.vue:** Main Vue.js component.
  - **main.js:** Entry point for the Vue.js application.
- **pages:** Contains Python scripts for different pages of the dashboard interface.

## Frontend Features

### Data Input Interface
The Data Input Interface allows users to upload and update data files, providing a seamless experience for managing raw data.

### Competitor Analysis
The Competitor Analysis feature offers a panoramic view of the pricing landscape, conducting comparative analysis against industry benchmarks.

### Upload
The Upload page allows users to upload their own data into the database.

### Update
The Update page allows users to view their data in a table form. They can also delete their data by selecting the rows they would like to delete on this page.

### Optimise
The Price Optimization Interface synthesizes overseas cable car data to suggest optimal pricing strategies, leveraging data-driven analytics and machine learning algorithms.

### Price Elasticity of Demand
The PED page offers users the optimal price for revenue maximization based on selected filters. It provides visual graphs and allows customization, utilizing user-uploaded datasets for accurate and updated results. 

## Backend Features

### Controller
The Controller directory houses the Flask server routes, managing interactions between the client-side interface and server-side functionality. It orchestrates HTTP requests and responses, ensuring smooth user experience and maintaining code organization.

### Model
The model subdirectory plays a pivotal role in facilitating accurate pricing predictions for the cable car service and serves as the repository for the business logic related to handling the mySQL database. It encompasses modules dedicated to implementing and managing the machine learning model utilized for price optimization and also includes modules responsible for data retrieval, storage and manipulation.

### Services
The services subdirectory plays a crucial role in ensuring the reliability and consistency of data used in the cable car pricing prediction system. It provides a structured approach to data validation, helping maintain clean and valid datasets for accurate analysis and prediction.
Each module within the services subfolder is dedicated to validating specific data attributes or parameters used in the cable car pricing prediction system. 

### Conclusion
The MFLG project leverages data-driven analytics to optimize cable car pricing strategies. With features like the Data Input Interface, Competitor Analysis, and Price Optimization Interface, it offers a comprehensive solution for strategic price optimization. The structured organization of the frontend and backend components promotes ease of maintenance, scalability, and future enhancements to the pricing prediction system.

For further details or inquiries, please refer to the project repository or contact the project team.


## Installation

### Frontend Installation
To install the frontend dependencies, please follow these steps:

1. Navigate to the frontend directory of the project.
2. Create a virtual environment (optional but recommended).
3. Activate the virtual environment (if created).
4. Run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```
### Backend Installation
To install the backend dependencies, please follow these steps:

1. Navigate to the backend directory of the project.
2. Create a virtual environment (optional but recommended).
3. Activate the virtual environment (if created).
4. Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```
## Usage

### Frontend Usage
To use the frontend part of the project, follow these steps:

1. Ensure that the frontend dependencies are installed (refer to the [Installation](#installation) section for instructions).
2. Navigate to the frontend directory of the project.
3. Run the following command to start the frontend server:

```bash
streamlit run main.py
```
4. Access the frontend interface in your web browser by navigating to http://localhost:8501.

### Backend Usage
To use the backend part of the project, follow these steps:

1. Ensure that the backend dependencies are installed (refer to the Installation section for instructions).
2. Navigate to the backend directory of the project.
3. Run the following command to start the backend server:
```bash
python app.py
```
4. The backend server will start running at http://localhost:5000.
5. Use API endpoints defined in the backend controllers to interact with the server, for example:
  a. Upload data: POST /upload
  b. Update data: PUT /update
  c. Perform competitor analysis: GET /competitor-analysis
  d. Optimize pricing strategy: POST /optimize


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
git commit -am 'Add new feature or fix bug'
```
6. Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```
7. Submit a pull request (PR) to the main repository's main branch. Provide a clear description of your changes and why they are needed.

## License
[Specify the project's license, such as MIT, Apache 2.0, or another open-source license. Include any additional terms or conditions as necessary.]


