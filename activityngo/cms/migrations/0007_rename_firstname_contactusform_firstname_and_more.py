# Generated by Django 4.2.1 on 2023-09-20 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_contactusform_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactusform',
            old_name='firstName',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='contactusform',
            old_name='lastName',
            new_name='lastname',
        ),
    ]
