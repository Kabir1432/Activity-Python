# Generated by Django 4.2.1 on 2023-07-17 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subadmin',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
