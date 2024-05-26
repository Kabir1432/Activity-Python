# Generated by Django 4.2.5 on 2023-09-21 10:14

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_rename_firstname_contactusform_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Mobile Number')),
                ('visit_at', models.TextField(verbose_name='visit at')),
                ('filled_form_to_be_emailed_to', models.EmailField(max_length=254, verbose_name='Email')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]