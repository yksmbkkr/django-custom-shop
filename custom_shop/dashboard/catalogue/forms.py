from oscar.apps.dashboard.catalogue import forms as base_forms

class ProductForm(base_forms.ProductForm):

    class Meta(base_forms.ProductForm.Meta):
        fields = [
            'title', 'is_active', 'short_description', 'upc', 'description', 'is_public', 'is_discountable', 'product_options', 'structure', 'slug', 'meta_title',
            'meta_description']