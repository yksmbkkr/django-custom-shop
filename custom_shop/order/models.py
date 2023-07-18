from django.db import models
from oscar.apps.address.abstract_models import AbstractShippingAddress
from oscar.core.loading import get_class

UniversityDepartment = get_class('address.models', 'UniversityDepartment')
ShippingAddress = get_class('order.models', 'ShippingAddress')

# class ShippingAddress(ShippingAddress):
#     department = models.ForeignKey(to=UniversityDepartment, limit_choices_to={"is_active": True},
#                                    on_delete=models.SET_NULL, null=True)

from oscar.apps.order.models import *  # noqa isort:skip