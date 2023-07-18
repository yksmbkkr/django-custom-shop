import uuid

from django.db import models
from oscar.apps.address.abstract_models import AbstractAddress

class UniversityDepartment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(AbstractAddress):
    department = models.ForeignKey(to=UniversityDepartment, limit_choices_to={"is_active": True}, on_delete=models.SET_NULL, null=True)


from oscar.apps.address.models import *  # noqa isort:skip
