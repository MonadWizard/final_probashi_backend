# Generated by Django 4.0.2 on 2022-04-03 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0057_alter_phoneotp_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneotp',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 4, 5, 3, 3, 475686)),
        ),
    ]
