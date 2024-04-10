FROM python:latest

WORKDIR /api

RUN pip3 install flask redis

expose 5000