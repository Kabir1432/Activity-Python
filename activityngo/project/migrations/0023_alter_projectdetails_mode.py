# Generated by Django 4.2.5 on 2024-01-12 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_studentfeedback_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetails',
            name='mode',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline'), ('online_and_offline', 'Online and Offline')], max_length=20),
        ),
    ]