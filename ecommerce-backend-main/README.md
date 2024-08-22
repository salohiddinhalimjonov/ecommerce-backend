# Ecommerce

## Project Setup
### Create Virtual Environment
```virtualenv venv``

### Activate Virtual Environment
```source venv/bin/activate```

### Configure Environment files
```cp .env.example .env```

edit .env file and add your own credentials

### Install Dependencies
```pip install -r requirements.txt```

### Upload initial data
```
python manage.py migrate
make loaddata
```

### Elastic search and Database
```
docker-compose up -d
python manage.py search_index --rebuild
```

### Run project
```
python manage.py createsuperuser
python manage.py runserver
```
