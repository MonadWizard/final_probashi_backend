# Generated by Django 4.0.2 on 2022-03-27 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0018_phoneotp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phoneotp',
            name='user',
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='user_callphone',
            field=models.CharField(db_index=True, default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phoneotp',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 19, 45, 7, 838882)),
        ),
    ]