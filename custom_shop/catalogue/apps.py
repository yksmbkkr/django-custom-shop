import oscar.apps.catalogue.apps as apps
from django.urls import path


class CatalogueConfig(apps.CatalogueConfig):
    name = 'custom_shop.catalogue'

    def get_urls(self):
        from custom_shop.catalogue.views import shops_list_view
        urls = super().get_urls()
        urls = [
            path('', shops_list_view, name='shops-list')
        ] + urls
        return self.post_process_urls(urls)
