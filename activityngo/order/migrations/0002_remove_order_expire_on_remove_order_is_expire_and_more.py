# Generated by Django 4.2.1 on 2023-08-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='expire_on',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_expire',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='expire_on',
            field=models.DateTimeField(null=True, verbose_name='expire_on'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='is_expire',
            field=models.BooleanField(default=False, verbose_name='is_expire'),
        ),
    ]
