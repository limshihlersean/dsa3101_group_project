FROM python:3.11

# Set working directory in the container
WORKDIR /frontend

# Copy the current directory contents into the container at app
COPY ./frontend .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "frontend/app.py"]