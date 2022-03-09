# Generated by Django 4.0.2 on 2022-02-28 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo_code_data',
            fields=[
                ('promo_code', models.CharField(db_index=True, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('promo_code_point', models.IntegerField(default=0)),
                ('promo_code_status', models.BooleanField(default=False)),
                ('promo_code_start_date', models.DateField(blank=True, null=True)),
                ('promo_code_end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_mail_notification_enable', models.BooleanField(default=True)),
                ('user_monthly_newsleter_enable', models.BooleanField(default=True)),
                ('user_reward_point', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Facing_trouble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_problem_message', models.TextField(blank=True, null=True)),
                ('user_problem_photo_path', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]