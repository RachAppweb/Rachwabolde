# Generated by Django 4.2 on 2023-06-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_commentandrating_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentandrating',
            name='adminresponse',
            field=models.TextField(blank=True, max_length=700, null=True),
        ),
    ]