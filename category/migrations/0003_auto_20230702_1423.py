# Generated by Django 3.2 on 2023-07-02 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cat_image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]