# Generated by Django 4.2.1 on 2023-08-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_expire_on_remove_order_is_expire_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Discount amount'),
        ),
        migrations.AddField(
            model_name='order',
            name='gst_charges',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='GST charges'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='order number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total amount'),
        ),
    ]
