FROM python:3.11-slim

WORKDIR /code

ENV PYTHONBUFFERED=1

COPY requirements.txt /code

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y gettext

COPY . .