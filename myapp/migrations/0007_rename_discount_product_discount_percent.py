# Generated by Django 4.0.4 on 2022-05-05 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_product_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount',
            new_name='discount_percent',
        ),
    ]