# Generated by Django 5.0.6 on 2024-06-24 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart_uu_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='uu_id',
            new_name='uu_id1',
        ),
    ]
