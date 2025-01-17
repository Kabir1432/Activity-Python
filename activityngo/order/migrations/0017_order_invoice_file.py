# Generated by Django 4.2.5 on 2023-09-22 05:36

import activityngo.utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_order_invoice_number_alter_order_status_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_file',
            field=models.FileField(null=True, upload_to=activityngo.utils.utils.get_order_invoice_path, verbose_name='Invoice file'),
        ),
    ]
