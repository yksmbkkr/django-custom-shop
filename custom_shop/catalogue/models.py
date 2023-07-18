import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractCategory
from oscar.core.loading import get_class
from oscar.models.fields import NullCharField
from django.utils.translation import gettext_lazy as _


class Product(AbstractProduct):
    is_active = models.BooleanField(default=False)
    upc = NullCharField(
        _("UPC"), max_length=64, blank=True, null=True, unique=True, default=uuid.uuid4,
        help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))
    short_description = models.CharField('Short Description', max_length=300, null=False, blank=False, default='A food preparation.')


class Category(AbstractCategory):
    status = models.BooleanField(default=True, verbose_name='Enable Shop')
    order_limit = models.IntegerField(default=100)
    cutoff_hour = models.PositiveIntegerField(default=14, validators=[MinValueValidator(0), MaxValueValidator(23)])
    start_hour = models.PositiveIntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(23)])


class ShopOrder(models.Model):
    shop = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    order = models.ForeignKey(to=get_class('order.models', 'Order'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # order_status = models.CharField()

    def __str__(self):
        return f'{self.shop.name} - {self.order.number}'

    # class Meta:
    #     ordering = ('-created',)

from oscar.apps.catalogue.models import *  # noqa isort:skip
