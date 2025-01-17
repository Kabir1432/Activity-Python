# Generated by Django 4.2.1 on 2023-08-16 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('tag', models.CharField(blank=True, max_length=32, null=True, verbose_name='Notification Tag')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Notification Title')),
                ('message', models.CharField(blank=True, max_length=128, null=True, verbose_name='Notification Message')),
                ('model_id', models.IntegerField(blank=True, null=True, verbose_name='Model Id')),
                ('is_public', models.BooleanField(default=False, verbose_name='Is Public')),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
