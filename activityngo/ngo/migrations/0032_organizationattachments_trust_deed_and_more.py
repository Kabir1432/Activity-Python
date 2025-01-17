# Generated by Django 4.2.1 on 2023-08-07 09:32

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0031_alter_organizationattachments_franchise_certificate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationattachments',
            name='trust_deed',
            field=models.FileField(blank=True, null=True, upload_to=activityngo.utils.utils.get_trust_deed, verbose_name='Trust Deed / Sec 8 Document'),
        ),
        migrations.AlterField(
            model_name='organizationattachments',
            name='tagline',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Tagline'),
        ),
    ]
