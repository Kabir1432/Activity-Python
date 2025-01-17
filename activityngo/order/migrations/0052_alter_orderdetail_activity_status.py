# Generated by Django 4.2.5 on 2024-02-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0051_remove_orderdetail_activity_completed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='activity_status',
            field=models.CharField(choices=[('incomplete', 'Incomplete'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancel', 'Cancel'), ('complete', 'Complete'), ('approve_complete', 'Approve Complete')], default='incomplete', max_length=30, verbose_name='Status'),
        ),
    ]
