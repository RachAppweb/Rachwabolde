# Generated by Django 4.2 on 2023-06-06 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_remove_orderproduct_color_remove_orderproduct_size_and_more'),
        ('cart', '0004_remove_cartitem_variations_alter_cartitem_cart_and_more'),
        ('store', '0004_variation_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Variation',
        ),
    ]