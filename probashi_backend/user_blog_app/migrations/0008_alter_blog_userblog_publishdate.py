# Generated by Django 4.0.2 on 2022-03-14 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_blog_app', '0007_blog_userblog_publishdate_alter_blog_userid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='userblog_publishdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]