# Generated by Django 4.2.1 on 2023-07-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0004_batches'),
    ]

    operations = [
        migrations.AddField(
            model_name='batches',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
