# Custom user app for Django

Custom user app for Django framework with simple RESTful interface for authorization and user obtaining.

## Requirements

* `django==3.0`
* `sqlalchemy==1.3.11`
* `mysqlclient==1.4.6` (for MySQL support)
* `psycopg2==2.8.4` (for PostgreSQL support)

## Installation

* Install dependencies with `pip install -r requirements.txt` (if not already)
* Start Django project with `django startproject <project name>` (if not already)
* Place `django_custom_user_app` app folder inside the project folder (it's possible to have it in a different location)
* Add `django_custom_user_app` to `INSTALLED_APPS` in Django `settings.py` file
* Add `django_custom_user_app.middleware.AuthMiddleware` to `MIDDLEWARE` in Django `settings.py` file
* Include `django_custom_user_app.urls` in the project's `urls.py` file

## HTTP methods

The app supports following HTTP methods:

* GET `api/profiles/<user_id>`, where `user_id` is either int or `me`  
Returns JSON serialized user object
* POST `api/auth/` with `email` and `password` fields  
*Login method*  
Returns `auth_token` and JSON serialized user object in case of successful login or error otherwise

## Example

The project contains fully functioning example, to run it:

* Add a folder that contains `django_custom_user_app` to `PYTHONPATH` environment variable (for example with `export PYTHONPATH=.` or `set PYTHONPATH=.` for Windows)
* Fill the database with test data (if you wish). To do that simply run `example/fill_db.py`
* Start the server with `example/manage.py runserver [<ip>:<port>]`