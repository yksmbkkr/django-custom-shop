import uuid

from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView


class ProductCreateUpdateView(ProductCreateUpdateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.creating:
            self.initial['upc'] = uuid.uuid4()