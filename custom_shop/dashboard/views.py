import datetime
import json
from typing import List

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from oscar.apps.order.models import Order as IOrderModal
from oscar.core.loading import get_class

from custom_shop.catalogue.models import ShopOrder, Category, Product
from custom_shop.dashboard.forms import ShopUpdateForm

CategoryModel: Category = get_class('catalogue.models', 'Category')
ProductModel: Product = get_class('catalogue.models', 'Product')
ShopOrderModel: ShopOrder = get_class('catalogue.models', 'ShopOrder')
OrderModel: IOrderModal = get_class('order.models', 'Order')
UniversityDepartment = get_class('address.models', 'UniversityDepartment')


def shop_control(request, uid=None):
    if uid is None:
        shop_list = CategoryModel.objects.filter(depth=1)
        return render(request, 'shop/dashboard/shop.list.html', {'shop_list': shop_list})
    shop = get_object_or_404(CategoryModel, pk=uid)
    shop_form = ShopUpdateForm(instance=shop)
    if request.method == 'POST':
        shop_form = ShopUpdateForm(request.POST, instance=shop)
        if shop_form.is_valid():
            shop_form.save()
            messages.success(request, "Shop updated!")
            return redirect(reverse('dashboard:manage-shops'))
    print(shop_form.errors)
    return render(request, 'shop/dashboard/shop-update.html', {'shop_form': shop_form, 'shop': shop})


def order_overview(request, uid=None):
    shop_wise_order_count = ShopOrderModel.objects.values('shop__name', 'shop__id').annotate(
        total_count=Count('shop'))

    return render(request, 'shop/dashboard/order-overview.html', {'shops': shop_wise_order_count})


def order_list_filtered(request):
    query_params = request.GET.get('params', None)
    if not query_params:
        return redirect(reverse('dashboard:order-overview'))
    query_params = json.loads(query_params)
    try:
        shop_id = int(query_params['shopId'])
        shop: Category = CategoryModel.objects.get(id=shop_id)
    except CategoryModel.DoesNotExist:
        messages.error(request, "Invalid shop")
        return redirect(reverse('dashboard:order-overview'))
    except Exception as e:
        messages.error(request, "Invalid shop")
        return redirect(reverse('dashboard:order-overview'))

    shop_orders = ShopOrderModel.objects.all()
    query_filter = Q(shop=shop)

    CUT_OFF_HOUR = shop.cutoff_hour
    local_time = timezone.localtime(timezone.now())
    cut_off_time = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0, 0,
                                     tzinfo=timezone.get_default_timezone())
    cut_off_time = timezone.localtime(cut_off_time)

    # Get orders from past week
    if query_params['duration'] == 'week':
        cut_off_time = timezone.localtime(cut_off_time) - datetime.timedelta(
            days=7)
        query_filter &= Q(created__gte=cut_off_time)

    # Get orders from yesterday
    elif query_params['duration'] == 'yesterday':
        if local_time.hour < CUT_OFF_HOUR:
            previous_day_cut_off = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0,
                                                     0,
                                                     tzinfo=timezone.get_default_timezone()) - datetime.timedelta(
                days=2)
            previous_day_cut_off = timezone.localtime(previous_day_cut_off)
            cut_off_time = cut_off_time - datetime.timedelta(days=1)
            query_filter &= Q(created__lt=cut_off_time, created__gte=previous_day_cut_off)
        else:
            previous_day_cut_off = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0,
                                                     0,
                                                     tzinfo=timezone.get_default_timezone()) - datetime.timedelta(
                days=1)
            previous_day_cut_off = timezone.localtime(previous_day_cut_off)
            query_filter &= Q(created__lt=cut_off_time, created__gte=previous_day_cut_off)

    # Get today's orders by default
    else:
        if local_time.hour < CUT_OFF_HOUR:
            previous_day_cut_off = datetime.datetime(local_time.year, local_time.month, local_time.day, CUT_OFF_HOUR, 0,
                                                     0,
                                                     tzinfo=timezone.get_default_timezone()) - datetime.timedelta(
                days=1)
            previous_day_cut_off = timezone.localtime(previous_day_cut_off)
            query_filter &= Q(created__lt=cut_off_time, created__gte=previous_day_cut_off)
        else:
            query_filter &= Q(created__gte=cut_off_time)

    item_filter: List[int] = []
    department_filter: List[int] = []

    cat_list = shop.get_descendants_and_self()

    # Get orders for specific product
    if 'filterBy' in query_params and query_params['filterBy'] == 'item':
        item_filter.append(ProductModel.objects.filter(categories__in=cat_list)[:1][0].id)

    # Get orders for specific department
    elif 'filterBy' in query_params and query_params['filterBy'] == 'dept':
        department_filter.append(UniversityDepartment.objects.all()[:1][0].id)

    if 'filterDept' in query_params:
        for i in query_params['filterDept']:
            if i == '':
                continue
            try:
                department_filter.append(int(i))
            except:
                pass

    if 'filterItem' in query_params:
        for i in query_params['filterItem']:
            try:
                item_filter.append(int(i))
            except:
                pass

    if len(department_filter) > 0:
        query_filter &= Q(order__user__department_id=department_filter[0])
        if not 'filterDept' in query_params:
            query_params['filterDept'] = department_filter

    if len(item_filter) > 0:
        item_q = Q(order__lines__product_id=item_filter[0])
        for q in item_filter[1:]:
            item_q |= Q(order__lines__product_id=q)
        query_filter &= (item_q)

        if not 'filterItem' in query_params:
            query_params['filterItem'] = item_filter

    shop_orders = shop_orders.filter(query_filter)

    if len(item_filter) > 0:
        final_orders = []
        final_orders_dict = {}
        for order in shop_orders:
            final_orders_dict[order.order.id] = order
        final_orders = final_orders_dict.values()
    else:
        final_orders = shop_orders

    args = {
        'orders': final_orders,
        'filters': query_params,
        'shop': shop,
        'dept_list': UniversityDepartment.objects.all(),
        'items_list': ProductModel.objects.filter(categories__in=cat_list)
    }

    return render(request, 'shop/dashboard/order-list-filter.html', args)
