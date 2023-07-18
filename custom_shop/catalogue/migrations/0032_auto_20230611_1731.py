# Generated by Django 3.2.19 on 2023-06-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0031_alter_product_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order_limit',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]