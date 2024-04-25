### Controller
The Controller directory houses the Flask server routes, managing interactions between the client-side interface and server-side functionality. It orchestrates HTTP requests and responses, ensuring smooth user experience and maintaining code organization.

### Model
The model subdirectory plays a pivotal role in facilitating accurate pricing predictions for the cable car service and serves as the repository for the business logic related to handling the mySQL database. It encompasses modules dedicated to implementing and managing the machine learning model utilized for price optimization and also includes modules responsible for data retrieval, storage and manipulation.

### Services
The services subdirectory plays a crucial role in ensuring the reliability and consistency of data used in the cable car pricing prediction system. It provides a structured approach to data validation, helping maintain clean and valid datasets for accurate analysis and prediction.
Each module within the services subfolder is dedicated to validating specific data attributes or parameters used in the cable car pricing prediction system. 

**app.py**

This is the entry point for running a Flask application. It imports the Flask class and an instance of the application (app) from the controller.data_controller module and then starts the Flask server.

**requirements.txt**

To manage and specify dependencies required for backend

**dockerfile**

This dockerfile provides instructions for how to build our Python Flask application using the following steps:
1. Specifying base image for Docker Image - Python 3.11
2. Set Working Directory: all subsequent commands will be executed relative to this directory
3. Copying of Required Files
4. Installing Dependencies
5. Making script executable
6. Exposing Ports
7. Setting Entrypoint to run

**wait-for-it.sh**

Shell script that ensures flask app waits for mySQL database to initialize before running.

