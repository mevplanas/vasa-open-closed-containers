# Base Ubuntu 20.04 image
FROM ubuntu:20.04

# Creating the working directory
WORKDIR /app

# Copying the requirements.txt file
COPY requirements.txt .

# Installing the requirements
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

# Adding the needed dependencies
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Copying over the src directory 
COPY src/ ./src

# Copying over the configuration.yml directory 
COPY configuration.yml .