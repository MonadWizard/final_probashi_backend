# Generated by Django 4.0.2 on 2022-04-07 20:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0075_alter_phoneotp_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneotp',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 8, 2, 40, 50, 434533)),
        ),
    ]
