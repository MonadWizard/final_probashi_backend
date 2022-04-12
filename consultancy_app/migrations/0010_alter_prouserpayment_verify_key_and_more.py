# Generated by Django 4.0.2 on 2022-04-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy_app', '0009_prouserpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prouserpayment',
            name='verify_key',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prouserpayment',
            name='verify_sign_sha2',
            field=models.TextField(blank=True, null=True),
        ),
    ]
