# Generated by Django 4.2.1 on 2023-07-14 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
        ('entities', '0002_alter_branch_name_alter_degree_name_and_more'),
        ('college', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegedegree',
            name='college',
        ),
        migrations.RemoveField(
            model_name='collegedegree',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='collegeproject',
            name='college',
        ),
        migrations.RemoveField(
            model_name='collegeproject',
            name='college_branch',
        ),
        migrations.RemoveField(
            model_name='collegeproject',
            name='college_degree',
        ),
        migrations.AddField(
            model_name='college',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='college_branch', to='entities.branch'),
        ),
        migrations.AddField(
            model_name='college',
            name='degree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='college_degree', to='entities.degree'),
        ),
        migrations.AlterField(
            model_name='college',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='college_state', to='entities.state'),
        ),
        migrations.AlterField(
            model_name='college',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='college_university', to='university.university'),
        ),
        migrations.DeleteModel(
            name='CollegeBranch',
        ),
        migrations.DeleteModel(
            name='CollegeDegree',
        ),
        migrations.DeleteModel(
            name='CollegeProject',
        ),
    ]