# Generated by Django 4.0.2 on 2022-03-15 08:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_connection_app', '0004_userconnectionrequestsend_connection_request_note'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserConnectionRequestSend',
            new_name='UserFavoutireRequestSend',
        ),
    ]
