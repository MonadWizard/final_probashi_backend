# Generated by Django 4.0.2 on 2022-03-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0003_alter_user_user_durationyear_abroad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
    ]
