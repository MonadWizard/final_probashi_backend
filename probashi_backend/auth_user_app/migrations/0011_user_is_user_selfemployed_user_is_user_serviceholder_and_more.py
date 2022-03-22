# Generated by Django 4.0.2 on 2022-03-22 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0010_user_auth_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_user_selfemployed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_user_serviceholder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='user_company_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_currentdesignation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_office_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
