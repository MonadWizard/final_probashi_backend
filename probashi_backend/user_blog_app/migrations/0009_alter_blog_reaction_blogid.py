# Generated by Django 4.0.2 on 2022-03-15 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_blog_app', '0008_alter_blog_userblog_publishdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_reaction',
            name='blogid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_reaction', to='user_blog_app.blog'),
        ),
    ]