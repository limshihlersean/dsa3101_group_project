**data_controller.py**

Contains Python Flask application that serves as a RESTful API for managing and querying a database. 
In this document, the different routes for each API call are clearly defined, which helps us to seamlessly integrate with the frontend team to receive and retrieve required data. 
The code interacts with the Database.py file under the model to query and access the MYSQL database. 
It also references various other python files under services to conduct data validation for all the tables. Lastly, the code also interacts with our price optimization and PED models to receive, train and  fetch optimal price recommendations and PED data for the frontend team. 
