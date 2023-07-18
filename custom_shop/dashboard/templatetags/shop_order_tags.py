import datetime

from django import template
from django.utils import timezone
from oscar.core.loading import get_class

from custom_shop.dashboard.utils import is_shop_accepting_orders

register = template.Library()


@register.simple_tag
def today_order_count_for_shop(shop):
    ShopOrderModel = get_class('catalogue.models', 'ShopOrder')
    CUT_OFF_HOUR = shop.cutoff_hour
    shop_order_qs = ShopOrderModel.objects.filter(shop=shop)
    local_time = timezone.localtime(timezone.now())
    cut_off_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone())
    cut_off_time = timezone.localtime(cut_off_time)
    if local_time.hour < CUT_OFF_HOUR:
        # TODO: handle time cutoff
        previous_day_cut_off = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone()) - datetime.timedelta(days = 1)
        previous_day_cut_off = timezone.localtime(previous_day_cut_off)
        shop_order_qs = shop_order_qs.filter(created__lt=cut_off_time, created__gte=previous_day_cut_off)
    else:
        shop_order_qs = shop_order_qs.filter(created__gte=cut_off_time)
    return shop_order_qs.count()


@register.simple_tag
def shop_accepting_orders(shop):
    CategoryModel = get_class('catalogue.models', 'Category')
    try:
        shop = CategoryModel.objects.get(id=shop.id)
    except CategoryModel.DoesNotExist:
        return False
    return is_shop_accepting_orders(shop)