# Fyle Xero Integration Web App
This repository is home to the **Fyle Xero Integration Web App**.

## Description
*Fyle Xero Integration Web App* is a Django application that enables export of settlements from Fyle to Xero.

### Development setup

#### a) Regular setup

1. Install the project dependencies by running `pip install -r requirements.txt`in a python environment of your choice
2. Rename the file ```.env.template``` to ```.env``` and customize it accordingly
3. Run ```python manage.py migrate``` to populate your database
4. Run ```python manage.py createsuperuser``` and follow the instructions to create an superuser 
5. Run ```python manage.py runserver``` to start the server on localhost

#### b) Using docker-compose

Install docker-compose
```pip install docker-compose```

1. Rename the file .env.template to .env and set the following defaults
    ```
    DATABASE_URL = postgres://postgres@db:5432/postgres
    ```
    and update the remaining fields accordingly

2. Build the images specified in docker-compose.yml file 
    ```docker-compose build```
3. Run the containers in background ```docker-compose up -d```
4. Apply the model migrations ```docker exec -it fyle_xero_web_app python manage.py migrate```
5. Create super-user ```docker exec -it fyle_xero_web_app python createsuperuser```
6. Access the application at [http://localhost:8000](http://localhost:8000)
7. To stop the containers do ```docker-compose down```


Visit [http://localhost:8000](http://localhost:8000) to access the application

### Tests
To run the tests do
``` python manage.py test```