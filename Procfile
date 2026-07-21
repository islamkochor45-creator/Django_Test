release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn DjangoInternetShops.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A DjangoInternetShops worker -l info
beat: celery -A DjangoInternetShops beat -l info
