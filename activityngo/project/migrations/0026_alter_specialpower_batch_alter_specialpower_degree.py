# Generated by Django 4.2.5 on 2024-02-13 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0027_alter_collegeusers_branch_alter_collegeusers_degree'),
        ('project', '0025_alter_project_minimum_number_of_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialpower',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_special_power', to='college.degreebranch'),
        ),
        migrations.AlterField(
            model_name='specialpower',
            name='degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='degree_special_power', to='college.collegedegree'),
        ),
    ]
