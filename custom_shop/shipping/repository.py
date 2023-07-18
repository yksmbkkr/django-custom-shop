from django.db import models
from oscar.apps.shipping import repository

from custom_shop.shipping import methods as shipping_methods

class UserTypeChoice(models.TextChoices):
    PROF = "PROFESSOR", "Staff"
    STUD = "STUDENT", "Student"

class Repository(repository.Repository):

    def get_available_shipping_methods(self, basket, user=None, shipping_addr=None, request=None, **kwargs):
        methods = (shipping_methods.SelfPickup(),)
        if user and user.user_type == UserTypeChoice.PROF:
            # Express is only available in the UK
            methods = (shipping_methods.SelfPickup(), shipping_methods.DepartmentDelivery())
        return methods