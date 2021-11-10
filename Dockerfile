# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /contact-api

# copy the requirements file used for dependencies
COPY requirements.txt .

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


CMD exec uvicorn main:app --host 0.0.0.0 --port 8080
