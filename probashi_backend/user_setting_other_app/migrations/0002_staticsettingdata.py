# Generated by Django 4.0.2 on 2022-03-09 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_setting_other_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticSettingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_industry_data', models.CharField(blank=True, max_length=255, null=True)),
                ('user_areaof_interest_data', models.CharField(blank=True, max_length=255, null=True)),
                ('user_interested_area_data', models.CharField(blank=True, max_length=255, null=True)),
                ('user_goal_data', models.CharField(blank=True, max_length=255, null=True)),
                ('consultancyservice_category_data', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'static_setting_data',
                'verbose_name_plural': 'static_setting_data',
                'db_table': 'static_setting_data',
            },
        ),
    ]