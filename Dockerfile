FROM python:3.9.5

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "run:app" ]
