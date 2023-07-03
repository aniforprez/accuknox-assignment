FROM python:3.10-slim-bullseye

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "manage.py", "runserver" ]