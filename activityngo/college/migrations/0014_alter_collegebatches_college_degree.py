# Generated by Django 4.2.1 on 2023-09-01 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0013_rename_college_collegebatches_college_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegebatches',
            name='college_degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college_degree', to='college.collegedegree'),
        ),
    ]