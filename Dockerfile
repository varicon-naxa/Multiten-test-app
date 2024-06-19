from python:3.10-slim-bullseye

RUN apt update && apt install -y gcc
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . /app/

EXPOSE 8000
