# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del .build-deps

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["scrapy", "crawl", "mtnspider"]
