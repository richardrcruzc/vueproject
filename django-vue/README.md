### Setup Database
python manage.py makemigrations
python manage.py migrate

### Create admin account
python manage.py createsuperuser

### Init DB
python manage.py loaddata init_data

### Run
python manage.py runserver 0:8000