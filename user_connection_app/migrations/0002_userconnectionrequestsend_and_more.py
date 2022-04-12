# Generated by Django 4.0.2 on 2022-03-13 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_connection_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConnectionRequestSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_connection_accept', models.BooleanField(default=False)),
                ('is_connection_reject', models.BooleanField(default=False)),
                ('connection_request_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='connection_request_to', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_consultant',
            name='user',
        ),
        migrations.DeleteModel(
            name='user_consult_appointment',
        ),
        migrations.DeleteModel(
            name='User_consultant',
        ),
    ]
