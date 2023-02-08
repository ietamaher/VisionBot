# Use an official Python runtime as the parent image
FROM python:3.7

# Set the working directory to /code
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install the required packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /code/app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Specify the command to run the code when the container starts
CMD ["python", "./app/flask_gui.py", "--host=0.0.0.0" ]