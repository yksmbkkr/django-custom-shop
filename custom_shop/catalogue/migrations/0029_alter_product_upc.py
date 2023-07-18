# Generated by Django 3.2.19 on 2023-05-31 18:47

from django.db import migrations
import oscar.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0028_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=oscar.models.fields.NullCharField(default=uuid.uuid4, help_text='Universal Product Code (UPC) is an identifier for a product which is not specific to a particular  supplier. Eg an ISBN for a book.', max_length=64, unique=True, verbose_name='UPC'),
        ),
    ]