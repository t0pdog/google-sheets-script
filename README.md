# Script to get data from Google sheets
Test table: https://docs.google.com/spreadsheets/d/1NFIfGUrXHXkd-e0gbtWTLO1srIz4_bsIWg52NZmcFUE/edit#gid=0

## Description
The script is located in the application folder sheets_app\management\commands. Its operation is described in the google.py file, it is launched by the command: python manage.py google.
A single-page web application based on Django Templates has been developed, which gives a table with data.
Run in 3 containers via docker-compose (app, database, nginx)
![Example picture](Screenshot_1.jpg "Example picture")

## Application launch (Windows)
### To run the project:

Copy the project to the local computer (via SSH), then go to the folder with it:

```bash
git clone git@github.com:t0pdog/google-sheets-script.git
```
### You need to register a project in console.cloud.google.com, create a service account, and get a file with the Service account key, rename it to service_account.json and put it at the following address: \google_sheets_script\sheets_app\management\commands\gspread\service_account.json.
Then create a Google spreadsheet and give it editor access for the service account.

The .env file is already exist, you don't need to create it.

Deploy and activate the virtual environment.
```
python -m venv venv
. venv/Scripts/activate
```
Install Docker on your computer.

Go to the folder with docker-compose.yaml and run docker-compose with the command
```
docker-compose up
```

Execute the commands one by one
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
docker-compose exec web python manage.py google
```
### The project and the admin panel are available at:
http://localhost/
http://localhost/admin/
