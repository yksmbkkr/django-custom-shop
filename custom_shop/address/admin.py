from oscar.apps.address.admin import *  # noqa
from oscar.core.loading import get_class

UniversityDepartment = get_class('address.models', 'UniversityDepartment')
admin.site.register(UniversityDepartment)