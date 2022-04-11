# Generated by Django 4.0.2 on 2022-04-11 11:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0083_alter_phoneotp_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendsuggation',
            name='localtion',
        ),
        migrations.AddField(
            model_name='friendsuggation',
            name='location',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='friendsuggation',
            name='goals',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='friendsuggation',
            name='interest',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
    ]
