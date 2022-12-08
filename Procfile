web: gunicorn -chdir kmachappy kmacshop.wsgi:application --bind
release: django-admin migrate --no-input && django-admin collectstatic --no-input