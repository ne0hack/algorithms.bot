FROM python:3.10-slim

# Make a directory for our application
WORKDIR /algosbot

# Copying the dependency file and the program code to the working directory
COPY requirements.txt .
COPY main.py .
COPY app/ app/

# Install dependency
RUN apt-get update
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Run app
ENTRYPOINT ["python3", "main.py"]