# Generated by Django 4.2.1 on 2023-08-22 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0011_remove_projectprice_project_type'),
        ('cart', '0013_remove_orderdetail_order_remove_orderdetail_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expire_on', models.DateTimeField()),
                ('is_expire', models.BooleanField(default=False, verbose_name='is_expire')),
                ('discount_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.discountcode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='order.order')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order_details', to='project.project')),
                ('project_price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_product_price_details', to='project.projectprice')),
            ],
        ),
    ]
