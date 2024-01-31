FROM python:slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app

CMD ["python3","run.py"]



