from django.contrib import messages
from django.shortcuts import redirect
from oscar.apps.checkout.views import PaymentDetailsView


class PaymentDetailsView(PaymentDetailsView):
    def post(self, request, *args, **kwargs):
        # Posting to payment-details isn't the right thing to do.  Form
        # submissions should use the preview URL.
        basket_obj = self.request.basket
        shops = {}
        for line_item in basket_obj.all_lines():
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
            return redirect('/shops/')

        return super().post(request, *args, **kwargs)

    def render_preview(self, request, **kwargs):
        """
        Show a preview of the order.

        If sensitive data was submitted on the payment details page, you will
        need to pass it back to the view here so it can be stored in hidden
        form inputs.  This avoids ever writing the sensitive data to disk.
        """
        self.preview = True
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)