# Generated by Django 4.2 on 2023-06-05 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variation_variation_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
