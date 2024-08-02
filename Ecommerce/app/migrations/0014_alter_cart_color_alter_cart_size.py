# Generated by Django 5.0.6 on 2024-06-27 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_products_colors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='color',
            field=models.ForeignKey(default='red', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.color'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(default='meduim', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.size'),
        ),
    ]
