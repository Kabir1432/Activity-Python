# Generated by Django 4.2.1 on 2023-08-09 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_project_number_of_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetails',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='projects_details', to='project.project'),
        ),
    ]