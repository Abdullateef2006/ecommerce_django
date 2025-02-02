# Generated by Django 5.0.6 on 2024-06-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_cart_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='colors',
            field=models.ManyToManyField(blank=True, to='app.color'),
        ),
        migrations.AddField(
            model_name='products',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='app.size'),
        ),
    ]
