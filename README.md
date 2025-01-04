# Sequencer App
This is a Django based web application that allows users to create, edit, delete and view number sequences.

# Features
- Admin can create a department.
- Admin can create a document.
- Admin can create a year.
- Admin can assign users to a department and assign role (admin, user)
- Admin department can create a sequence using the year, document and department.
- Admin department can assign other users to the department.
- Users can create a emission using the sequence.
- Users can view the emission.
- Users can update the emission.
- Users can upload files to the emission.
- Admin department can view all the emissions.
- Admin department can reassign the emission to another user.
- Admin department can receive the emission.
- Admin department can view the emission files.

# Environment Setup
To setup the environment, run the following command.
```python
pip install -r requirements.txt
```
To environment variables, create a .env file in the root directory copy the content from .env.example and update the values.
```bash
cp .env.example .env
```
If variable *DJANGO_DATABASE_URL* is not set, for default sqlite database will be used.
This configuration is in *settings.py* file.

# For Google OAuth
Create a google app to obtain a key and secret through the developer console.

Google Developer Console
https://console.developers.google.com/

>After you create a project you will have to create a "Client ID" and fill in some project details for the consent form that will be presented to the client.

>Under "APIs & auth" go to "Credentials" and create a new Client ID. Probably you will want a "Web application" Client ID. Provide your domain name or test domain name in "Authorized JavaScript origins". Finally fill in http://127.0.0.1:8000/accounts/google/login/callback/ in the "Authorized redirect URI" field. You can fill multiple URLs, one for each test domain.

After creating the Client ID you will copy the "Client ID" and "Client secret" to the .env file.

# For Start App
To setup the database, run the following command.
```python
python manage.py migrate
```
To run the server, use the following command.
```python
python manage.py runserver
```
To create a superuser, use the following command.
```python
python manage.py createsuperuser
```

# For Docker
To build the docker image, use the following command.
```python
docker compose build
```
To run the docker image, use the following command.
```python
docker compose up
```
To migrate
```python
docker compose exec web python manage.py migrate
```