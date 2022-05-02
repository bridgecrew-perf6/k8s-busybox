# set base image (host OS)
FROM python:3.9.10-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY . .

# install dependencies
RUN pip3 install -r requirements.txt

# command to run on container start
CMD [ "python3","main.py" ]