# Generated by Django 4.0.4 on 2022-05-25 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('received', 'Order Received'), ('processing', 'Order in Process'), ('shipped', 'Order Shipped'), ('cancelled', 'Order Cancelled')], default='received', max_length=10),
        ),
    ]