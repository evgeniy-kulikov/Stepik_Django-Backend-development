# Generated by Django 3.2.18 on 2023-03-30 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stripe_product_price_id',
        ),
    ]
