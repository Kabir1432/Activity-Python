# Generated by Django 4.2.5 on 2024-01-05 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_remove_order_transaction_id_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='activity_status',
            field=models.CharField(choices=[('incomplete', 'Incomplete'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancel', 'Cancel'), ('complete', 'Complete')], default='incomplete', max_length=30, verbose_name='Status'),
        ),
    ]
