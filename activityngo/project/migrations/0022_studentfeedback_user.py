# Generated by Django 4.2.5 on 2023-12-05 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0021_alter_project_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfeedback',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_feedback_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
