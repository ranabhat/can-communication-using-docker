# For more information, please refer to https://aka.ms/vscode-docker-python
FROM --platform=linux/arm/v7 debian:buster-slim

# Use /usr/src/app as our workdir. The following instructions will be executed in this location.
WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update && apt-get install -y \ 
    nano \ 
    python3 \ 
    python3-pip \ 
    python3-setuptools \ 
    git \ 
    iproute2 \ 
    can-utils \ 
    python3-can \ 
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*  

COPY . /usr/src/app
