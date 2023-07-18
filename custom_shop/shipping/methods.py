from decimal import Decimal as D

from django.utils.translation import gettext_lazy as _

from oscar.apps.shipping.methods import Base, Free
from oscar.core import prices


class DepartmentDelivery(Free):
    """
    This shipping method specifies that shipping is free.
    """
    code = 'department-delivery'
    name = _('Deliver to Department')


class SelfPickup(Free):
    """
    This is a special shipping method that indicates that no shipping is
    actually required (e.g. for digital goods).
    """
    code = 'self-pickup'
    name = _('Self Pickup')