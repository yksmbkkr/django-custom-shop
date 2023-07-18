from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from oscar.apps.catalogue.views import CatalogueView, ProductCategoryView, ProductDetailView
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie


class CatalogueView(CatalogueView):
    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['summary'] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        ctx.update(search_context)
        return ctx


class ProductCategoryView(ProductCategoryView):
    template_name = 'shop/category-menu-list.html'

    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        self.category = self.get_category()

        shop = self.category.get_ancestors_and_self()[0]
        from custom_shop.dashboard.utils import is_shop_accepting_orders
        if not is_shop_accepting_orders(shop):
            return redirect('/shops/')

        # Allow staff members so they can test layout etc.
        if not self.is_viewable(self.category, request):
            raise Http404()

        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect

        try:
            self.search_handler = self.get_search_handler(
                request.GET, request.get_full_path(), self.get_categories())
            response = super().get(request, *args, **kwargs)
        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_cart_action_bar'] = True
        context['inner_page_class'] = 'm-0 mt-5'
        return context


class ProductDetailView(ProductDetailView):

    def get(self, request, **kwargs):
        """
        Ensures that the correct URL is used before rendering a response
        """
        self.object = product = self.get_object()

        shop = self.object.categories.all()[0].get_ancestors_and_self()[0]
        from custom_shop.dashboard.utils import is_shop_accepting_orders
        from django.shortcuts import render, redirect

        if not is_shop_accepting_orders(shop):
            return redirect('/shops/')

        redirect = self.redirect_if_necessary(request.path, product)
        if redirect is not None:
            return redirect

        # Do allow staff members so they can test layout etc.
        if not self.is_viewable(product, request):
            raise Http404()

        response = super().get(request, **kwargs)
        self.send_signal(request, response, product)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_cart_action_bar'] = True
        return context


def test_view(request):
    return HttpResponse('TEST')

@ensure_csrf_cookie
def shops_list_view(request):
    return render(request, 'shop/shops-list.html')