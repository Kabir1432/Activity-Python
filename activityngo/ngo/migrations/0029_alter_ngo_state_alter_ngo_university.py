# Generated by Django 4.2.1 on 2023-08-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_batches_disable_date'),
        ('university', '0003_university_disable_date'),
        ('ngo', '0028_alter_ngo_state_alter_ngo_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngo',
            name='state',
            field=models.ManyToManyField(blank=True, to='entities.state'),
        ),
        migrations.AlterField(
            model_name='ngo',
            name='university',
            field=models.ManyToManyField(blank=True, to='university.university'),
        ),
    ]
