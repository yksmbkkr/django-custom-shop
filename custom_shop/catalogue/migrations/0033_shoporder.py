# Generated by Django 3.2.19 on 2023-06-11 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20230527_2114'),
        ('catalogue', '0032_auto_20230611_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogue.category')),
            ],
        ),
    ]
