# install python 3.10, less bloated and Debian linux
FROM python:3.10-slim-buster 

# change the working directory to app or create if it does not exist
WORKDIR /app

# copy all files from current directory to working directory in container
COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]