# Accuknox Social Media Assignment

## Instructions

The simple way to run the project is simply to use docker compose

* Run `docker compose up --build` in the root directory of this project.

If you wish to install and run the project locally, you will require Python 3.10 or
newer.

1. Create a virtual environment with `python -m venv venv`
2. Activate the virtual environment `source venv/bin/activate`
3. Install the requirements with `pip install requirements.txt`
4. Run migrations with `python manage.py migrate`. Since the project uses an SQLite DB, this will also create an SQLite DB file at the root directory.
5. Run the project with `python manage.py runserver`

Additionally, it will also help to create a superuser with access to the admin panel.
Create one with `python manage.py createsuperuser` and provide an email and password.
You can then access the admin panel at [this URL](http://localhost:8000/admin).

## Postman Collection

The Postman Collection for the APIs in the project are provided in [this file](Accuknox.postman_collection.json).
Please create a user, login to that user and use the returned token in the environment variables as "token" to authenticate all requests. Otherwise, replace the `Authorization` header in all requests with `Token <token value>`