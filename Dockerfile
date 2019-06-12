# Builds the docker image. Data is not mounted here so tests run externally.

from ubuntu:19.04 

# Copy the working directory here 
WORKDIR /ReEMS/Algorithms
COPY . /ReEMS/Algorithms
COPY ./data-cruz-roja-clean /ReEMS/data-cruz-roja-clean

# Download python3.7 and use the requirements
RUN apt-get upgrade -y && \
	apt-get update -y && \
	apt-get install -y python3 python3-pip
RUN python3 -m pip install -r requirements.txt 

