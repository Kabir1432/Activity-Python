# Generated by Django 4.2.1 on 2023-08-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_batches_disable_date'),
        ('university', '0003_university_disable_date'),
        ('ngo', '0027_alter_ngo_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngo',
            name='state',
            field=models.ManyToManyField(blank=True, null=True, to='entities.state'),
        ),
        migrations.AlterField(
            model_name='ngo',
            name='university',
            field=models.ManyToManyField(blank=True, null=True, to='university.university'),
        ),
    ]
