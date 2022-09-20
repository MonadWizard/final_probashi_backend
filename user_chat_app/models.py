from django.db import models


class ChatTable(models.Model):
    user_1 = models.CharField(max_length=20, db_index=True)
    user_2 = models.CharField(max_length=20, db_index=True)
    table_name = models.CharField(max_length=100)

    def __str__(self):
        return self.table_name




"""
makemigrations:
    ❯ python manage.py makemigrations user_chat_app           

migration:
    ❯ python manage.py migrate user_chat_app --database=probashi_chat
"""
