#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations phrasebook
python manage.py migrate

echo "Creating admin..."
python manage.py shell -c \
"from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('$ADMIN', '', '$PASSWORD')"
echo "Admin created"

echo "Generate messages..."
python manage.py makemessages -l ru --ignore templates/admin/index.html --ignore */settings.py
echo "Messages generated"
exec "$@"