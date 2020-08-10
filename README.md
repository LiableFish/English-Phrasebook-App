# English-Phrasebook-App
Test task for backend Junior-developer by [Doubletapp](https://doubletapp.ai/).

## Using:
- django
- rest-framework
- postgresql
- gunicorne
- nginx
- docker-compose

## Development
```
$ docker-compose up -d --build
```
## Production
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```
To apply migrations:
```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
````
To collect static files
```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
To create superuser
```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```


# TODO
- Create tests
- Deal with app translation
