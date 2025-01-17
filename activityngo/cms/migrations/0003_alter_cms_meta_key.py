# Generated by Django 4.2.1 on 2023-09-19 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_usermanual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cms',
            name='meta_key',
            field=models.CharField(choices=[('necessity', 'Necessity'), ('aicte_rules', 'AICTE Rules'), ('university_rules', 'University Rules'), ('implementation_method', 'Implementation Method'), ('our_team', 'Our Team'), ('terms_and_conditions', 'Terms and Conditions'), ('about_us', 'About US'), ('privacy_policy', 'Privacy Policy'), ('read_instructions', 'Read Instructions')], max_length=32, unique=True),
        ),
    ]
