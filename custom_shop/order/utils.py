from django.contrib import messages
from django.shortcuts import redirect
from oscar.apps.order.utils import OrderCreator
from django.utils.translation import gettext_lazy as _


class OrderCreator(OrderCreator):
    def place_order(self, basket, total,  # noqa (too complex (12))
                    shipping_method, shipping_charge, user=None,
                    shipping_address=None, billing_address=None,
                    order_number=None, status=None, request=None, surcharges=None, **kwargs):
        """
        Placing an order involves creating all the relevant models based on the
        basket and session data.
        """
        if basket.is_empty:
            raise ValueError(_("Empty baskets cannot be submitted"))

        shops = {}
        for line_item in basket.all_lines():
            shop = line_item.product.categories.first().get_ancestors_and_self()[0]
            shops[shop.id] = shop

        should_continue_flag = True

        from custom_shop.dashboard.utils import is_shop_accepting_orders
        for shop in shops:
            if not is_shop_accepting_orders(shops[shop]):
                should_continue_flag = False
                break

        if not should_continue_flag:
            messages.warning(request, 'This shop is not accepting orders.')
            return None

        return super().place_order(basket, total,  # noqa (too complex (12))
                    shipping_method, shipping_charge, user,
                    shipping_address, billing_address,
                    order_number, status, request, surcharges, **kwargs)