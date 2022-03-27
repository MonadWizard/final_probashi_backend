# Generated by Django 4.0.2 on 2022-03-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0014_alter_user_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.EmailField(blank=True, db_index=True, max_length=255, null=True, unique=True),
        ),
    ]
