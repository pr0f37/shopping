FROM python:3.7
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app

CMD gunicorn --bind 0.0.0.0:5000 -w 4 "wsgi:app"