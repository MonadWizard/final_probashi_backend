# Generated by Django 4.0.2 on 2022-03-01 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile_app', '0004_alter_user_socialaccount_and_about_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_education',
            old_name='user',
            new_name='userid',
        ),
        migrations.RenameField(
            model_name='user_experience',
            old_name='user',
            new_name='userid',
        ),
        migrations.RenameField(
            model_name='user_idverification',
            old_name='user',
            new_name='userid',
        ),
        migrations.RenameField(
            model_name='user_socialaccount_and_about',
            old_name='user',
            new_name='userid',
        ),
    ]