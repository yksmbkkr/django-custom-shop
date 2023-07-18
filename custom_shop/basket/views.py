from urllib import parse

from django import shortcuts
from oscar.apps.basket.views import BasketAddView

from custom_shop.dashboard.utils import is_shop_accepting_orders


class BasketAddView(BasketAddView):

    def post(self, request, *args, **kwargs):
        self.product = shortcuts.get_object_or_404(
            self.product_model, pk=kwargs['pk'])
        shop = self.product.categories.all()[0].get_ancestors_and_self()[0]

        if not is_shop_accepting_orders(shop):
            return shortcuts.redirect('/shops/')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        resp_url = super().get_success_url()
        uri = parse.urlparse(resp_url)
        qs = parse.parse_qs(uri.query)
        qs['action'] = 'product_added'
        qs['name'] = self.product.title
        resp_url = f'{uri.path}?{parse.urlencode(qs)}'
        return resp_url