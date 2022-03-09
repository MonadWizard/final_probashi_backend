# Generated by Django 4.0.2 on 2022-03-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_setting_other_app', '0003_rename_user_areaof_interest_data_staticsettingdata_user_areaof_experience_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticsettingdata',
            name='consultancyservice_category_data',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='staticsettingdata',
            name='user_areaof_experience_data',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='staticsettingdata',
            name='user_goal_data',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='staticsettingdata',
            name='user_industry_data',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='staticsettingdata',
            name='user_interested_area_data',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]