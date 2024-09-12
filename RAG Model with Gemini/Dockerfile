# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variable
ENV GOOGLE_API_KEY="AIzaSyBg7Ham4jFlNEzrIsCK3PuXbfONKXPCCSs"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the .streamlit directory
COPY .streamlit /root/.streamlit

# Expose the port Streamlit will run on
EXPOSE 8501

# Define the command to run your app
CMD ["streamlit", "run", "app.py"]