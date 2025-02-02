# Generated by Django 5.0.6 on 2024-06-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_cart_color_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='colors',
            field=models.ManyToManyField(blank=True, default='large', to='app.color'),
        ),
        migrations.AlterField(
            model_name='products',
            name='sizes',
            field=models.ManyToManyField(blank=True, default='meduim', to='app.size'),
        ),
    ]
