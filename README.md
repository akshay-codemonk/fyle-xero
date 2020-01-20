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

##### For Synchronization
To perform synchronization [Redis](https://redis.io/) is required

1. Start a Redis server by downloading and running it as mentioned [here](https://redis.io/topics/quickstart)
 or use the docker run command 
```Docker run -p 6379:6379 --name=redis redis```

2. Once Redis is up and running, start a Django Q cluster by running ```
python manage.py qcluster```

#### b) Using docker-compose

Install docker-compose
```pip install docker-compose```

1. Rename the file .env.template to .env and set the following defaults
    ```
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=
    DB_HOST=db
    DB_PORT=5432
    REDIS_HOST=redis
    REDIS_PORT=6379
    ```
    and update the remaining fields accordingly

2. Build the images specified in docker-compose.yml file 
    ```docker-compose build```
3. Run the containers in background ```docker-compose up -d```
4. Apply the model migrations ```docker exec -it fyle_xero_web_app python manage.py migrate```
5. Create super-user ```docker exec -it fyle_xero_web_app python createsuperuser```
6. Access the application at [http://localhost:8000](http://localhost:8000)
7. To stop the containers do ```docker-compose down```

### Configure Fyle OAuth2.0
1. Open django-admin by visiting [http://localhost:8000/admin](http://localhost:8000/admin) and login using the superuser credentials 
2. First go to the **Sites** portion and set the domain name to ```localhost``` 
3. Setup Fyle allauth provider 
    1. Create a new record under **Social Applications**
    2. Select Fyle as provider and enter the your Fyle OAuth2.0 client_secret and client_id 
    3. Add your site to the Chosen sites on the bottom and click save.

Visit [http://localhost:8000](http://localhost:8000) to access the application

### Tests
To run the tests do
``` python manage.py test```