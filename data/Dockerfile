FROM python:3.11

# Set working directory in the container
WORKDIR /app

# Copy your Python script and CSV file into the container
COPY requirements.txt .
COPY database.py .
COPY local_attractions_citandnon_isbundle_2024.csv .
COPY local_attractions_citizen_alacarte_allyears.csv .
COPY local_attractions_noncitizen_alacarte_2024.csv .
COPY cable_car_cleaned_v2.csv .
COPY NewCableCarPED.csv .
COPY .env .

RUN pip install -r requirements.txt

# Command to run your script
CMD ["python", "database.py"]