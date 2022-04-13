from django.db import models

class ChatTable(models.Model):
    user_1 = models.CharField(max_length=20, db_index=True)
    user_2 = models.CharField(max_length=20, db_index=True)
    table_name = models.CharField(max_length=100)

# class chatTable(models.Model):
#     userid = models.CharField(max_length=20)
#     message = models.TextField()
#     date_time = models.DateTimeField(auto_now_add=True)
    # is_deleted = models.BooleanField(default=False)
    # is_seen = models.BooleanField(default=False)



'''
makemigrations:
    ❯ python manage.py makemigrations user_chat_app           

migration:
    ❯ python manage.py migrate user_chat_app --database=probashi_chat
'''