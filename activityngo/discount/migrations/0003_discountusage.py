# Generated by Django 4.2.1 on 2023-08-23 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discount', '0002_discount_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('used_at', models.DateTimeField(auto_now_add=True)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.discount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'discount')},
            },
        ),
    ]
