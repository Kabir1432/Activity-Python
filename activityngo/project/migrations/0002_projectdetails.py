# Generated by Django 4.2.1 on 2023-07-26 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('mode', models.CharField(max_length=40, verbose_name='Project Mode')),
                ('beneficiary_in_society', models.CharField(max_length=300, verbose_name='beneficiary_in_society')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='projects_projectdetails', to='project.projectbasicdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
