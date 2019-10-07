# Fyle Xero Integration Web App
This repository is home to the **Fyle Xero Integration Web App**.

## Description
*Fyle Xero Integration Web App* is a Django application that enables export of settlements from Fyle to Xero.

### Development setup

1. Install the project dependencies by running `pip install -r requirements.txt`in a python environment of your choice
2. Rename the file ```.env.template``` to ```.env``` and customize it accordingly
3. Run ```python manage.py migrate``` to populate your database
4. Run ```python manage.py createsuperuser``` and follow the instructions to create an superuser 
5. Run ```python manage.py runserver``` to start the server on localhost

### Configure Fyle OAuth2.0
1. Open django-admin by visiting [http://localhost:8000/admin](http://localhost:8000/admin) and login using the superuser credentials 
2. First go to the **Sites** portion and set the domain name to ```localhost``` 
3. Setup Fyle allauth provider 
    1. Create a new record under **Social Applications**
    2. Select Fyle as provider and enter the your Fyle OAuth2.0 client_secret and client_id 
    3. Add your site to the Chosen sites on the bottom and click save.

Visit [http://localhost:8000](http://localhost:8000) to access the application

### synchronization
To perform synchronization [Redis](https://redis.io/) is required

1. Start a Redis server by downloading and running it as mentioned [here](https://redis.io/topics/quickstart)
 or use the docker run command 

```Docker run -p 6379:6379 --name=redis redis```

2. Once Redis is up and running, start a Django Q cluster with 
```
python manage.py qcluster
```


 
 

