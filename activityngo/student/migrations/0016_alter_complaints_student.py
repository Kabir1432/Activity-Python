# Generated by Django 4.2.5 on 2023-10-09 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_complaints_upload_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_complaints', to='student.studentdetails'),
        ),
    ]
