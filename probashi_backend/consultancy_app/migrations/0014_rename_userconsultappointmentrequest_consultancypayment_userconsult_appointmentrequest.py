# Generated by Django 4.0.2 on 2022-04-10 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy_app', '0013_alter_userconsultappointmentrequest_consultancytimeschudile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consultancypayment',
            old_name='UserConsultAppointmentRequest',
            new_name='userConsult_AppointmentRequest',
        ),
    ]