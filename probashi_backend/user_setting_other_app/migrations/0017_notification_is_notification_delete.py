# Generated by Django 4.0.2 on 2022-04-03 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_setting_other_app', '0016_staticsettingdata_digitalservice_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_notification_delete',
            field=models.BooleanField(default=False),
        ),
    ]