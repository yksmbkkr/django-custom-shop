from django import forms
from oscar.core.loading import get_class


class ShopUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.widget_type == 'checkbox':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = get_class('catalogue.models', 'Category')
        fields = ['order_limit', 'start_hour', 'cutoff_hour', 'status']