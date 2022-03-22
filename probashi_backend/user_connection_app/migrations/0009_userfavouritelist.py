# Generated by Django 4.0.2 on 2022-03-17 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_connection_app', '0008_alter_userfavoutirerequestsend_favourite_request_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavouriteList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourite_request_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friend_user_data', to=settings.AUTH_USER_MODEL)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='login_user_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]