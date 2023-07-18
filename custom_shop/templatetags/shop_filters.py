import datetime


from django import template
from oscar.core.loading import get_class
from django.utils import timezone

from custom_shop.catalogue.models import Category

register = template.Library()

CategoryModel: Category = get_class('catalogue.models', 'Category')


@register.filter
def shop_today_duration(value):
    shop: Category = CategoryModel.objects.none()
    try:
        shop = CategoryModel.objects.get(id=value)
    except CategoryModel.DoesNotExist:
        return ''

    CUT_OFF_HOUR = shop.cutoff_hour
    local_time = timezone.localtime(timezone.now())
    if local_time.hour < CUT_OFF_HOUR:
        end_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                         tzinfo=timezone.get_default_timezone())
        end_time = timezone.localtime(end_time)

        start_time = end_time - datetime.timedelta(days = 1)
    else:
        start_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone())
        start_time = timezone.localtime(start_time)

        end_time = start_time + datetime.timedelta(days=1)

    return f'{start_time.strftime("%b %d, %Y, %H:%M")} - {end_time.strftime("%b %d, %Y, %H:%M")}'


@register.filter
def shop_yesterday_duration(value):
    shop: Category = CategoryModel.objects.none()
    try:
        shop = CategoryModel.objects.get(id=value)
    except CategoryModel.DoesNotExist:
        return ''

    CUT_OFF_HOUR = shop.cutoff_hour
    local_time = timezone.localtime(timezone.now())
    if local_time.hour < CUT_OFF_HOUR:
        end_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                         tzinfo=timezone.get_default_timezone())
        end_time = timezone.localtime(end_time)

        start_time = end_time - datetime.timedelta(days = 2)
        end_time = timezone.localtime(end_time) - datetime.timedelta(days = 1)
    else:
        end_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone())
        end_time = timezone.localtime(end_time)

        start_time = end_time - datetime.timedelta(days=1)

    return f'{start_time.strftime("%b %d, %Y, %H:%M")} - {end_time.strftime("%b %d, %Y, %H:%M")}'
