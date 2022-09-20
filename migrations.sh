python manage.py makemigrations auth_user_app
python manage.py migrate auth_user_app
python manage.py makemigrations consultancy_app
python manage.py migrate consultancy_app
python manage.py makemigrations social_auth
python manage.py migrate social_auth
python manage.py makemigrations user_blog_app
python manage.py migrate user_blog_app
python manage.py makemigrations user_connection_app
python manage.py migrate user_connection_app
python manage.py makemigrations user_profile_app
python manage.py migrate user_profile_app
python manage.py makemigrations user_setting_other_app
python manage.py migrate user_setting_other_app

python manage.py makemigrations
python manage.py migrate
