# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the Django project code to the working directory
COPY . .

# Expose the port on which the Django development server will run
EXPOSE 8000

# Define the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]