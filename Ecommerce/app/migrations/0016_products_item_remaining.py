# Generated by Django 5.0.6 on 2024-06-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='item_remaining',
            field=models.IntegerField(default=1),
        ),
    ]
