# template dockerfile for python3 http server

# Use the official image as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3080 available to the world outside this container
EXPOSE 3080

# RUN app.py when the container launches
CMD ["python3", "app.py"]
