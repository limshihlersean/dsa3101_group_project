FROM python:3.11

# Set working directory in the container
WORKDIR /frontend

# Copy the current directory contents into the container at app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --timeout=1000

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run Home.py when the container launches
CMD ["streamlit", "run", "1_🏡_Home.py"]
