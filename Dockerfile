# syntax=docker/dockerfile:1
FROM python:3.9.5-slim-buster

WORKDIR /app
COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN chmod u+x ./entrypoint.sh

EXPOSE 5000
CMD ["./entrypoint.sh"]
