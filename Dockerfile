FROM python:3.9.5

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN flask db upgrade

EXPOSE 5000
CMD [ "python", "run.py" ]
