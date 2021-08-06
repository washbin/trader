# syntax=docker/dockerfile:1
FROM python:3.9.5-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN chmod u+x ./docker_entrypoints/dev.sh \
    ./docker_entrypoints/prod.sh

EXPOSE 5000
CMD ["./docker_entrypoints/dev.sh"]
