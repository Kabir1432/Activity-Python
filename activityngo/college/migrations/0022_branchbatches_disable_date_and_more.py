# Generated by Django 4.2.5 on 2023-10-12 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0021_alter_branchbatches_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchbatches',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collegedegree',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='degreebranch',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
