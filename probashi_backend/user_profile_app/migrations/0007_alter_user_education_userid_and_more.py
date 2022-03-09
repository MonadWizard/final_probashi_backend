# Generated by Django 4.0.2 on 2022-03-07 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile_app', '0006_alter_user_idverification_user_verify_passportphoto_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_education',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_educationdata', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_experience',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_experiencedata', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_idverification',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_idverificationdata', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_socialaccount_and_about',
            name='userid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_socialaboutdata', to=settings.AUTH_USER_MODEL),
        ),
    ]