FROM python:3.10-slim-bullseye

RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "runserver" ]