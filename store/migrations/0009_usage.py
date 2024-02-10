# Generated by Django 4.2 on 2023-06-23 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_banners_is_availabel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=700)),
                ('screen', models.ImageField(upload_to='stor/usage')),
            ],
        ),
    ]