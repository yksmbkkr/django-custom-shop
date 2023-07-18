import datetime

from django import template
from django.utils import timezone
from oscar.core.loading import get_class


register = template.Library()


def today_order_for_shop(shop):
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
                                                 tzinfo=timezone.get_default_timezone()) - datetime.timedelta(days=1)
        previous_day_cut_off = timezone.localtime(previous_day_cut_off)
        shop_order_qs = shop_order_qs.filter(created__lt=cut_off_time, created__gte=previous_day_cut_off)
    else:
        shop_order_qs = shop_order_qs.filter(created__gte=cut_off_time)

    return shop_order_qs


def today_order_count_for_shop(shop):
    shop_order_qs = today_order_for_shop(shop)
    return shop_order_qs.count()


def is_shop_open(shop):
    CUT_OFF_HOUR = shop.cutoff_hour
    START_HOUR = shop.start_hour
    local_time = timezone.localtime(timezone.now())
    if START_HOUR > CUT_OFF_HOUR:
        cut_off_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                         tzinfo=timezone.get_default_timezone())
        cut_off_time = timezone.localtime(cut_off_time)
        start_time = datetime.datetime(local_time.year, local_time.month, local_time.day, START_HOUR, 0,
                                                      0,
                                                      tzinfo=timezone.get_default_timezone()) - datetime.timedelta(days=1)
        start_time = timezone.localtime(start_time)
    else:
        cut_off_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                         tzinfo=timezone.get_default_timezone())
        cut_off_time = timezone.localtime(cut_off_time)
        start_time = datetime.datetime(local_time.year, local_time.month, local_time.day, START_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone())
        start_time = timezone.localtime(start_time)

    return local_time >= start_time and local_time < cut_off_time


def is_shop_accepting_orders(shop):
    return shop.status and is_shop_open(shop) and shop.order_limit > today_order_count_for_shop(shop)