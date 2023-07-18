from django import forms
from oscar.core.loading import get_model, get_class
from oscar.forms.mixins import PhoneNumberMixin

AbstractAddressForm = get_class('address.forms', 'AbstractAddressForm')
Country = get_model('address', 'Country')
UniversityDepartment = get_model('address', 'UniversityDepartment')

class ShippingAddressForm(PhoneNumberMixin, AbstractAddressForm):
    line3 = forms.ModelChoiceField(required=True, empty_label='Select Department', queryset=UniversityDepartment.objects.all(), label='Department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjust_country_field()
        self.fields['line4'].initial = 'PAU, Ludhiana'
        self.fields['state'].initial = 'Punjab'
        self.fields['postcode'].initial = '141027'
        self.fields['country'].initial = Country.objects.get(iso_3166_1_a2='IN')

    def adjust_country_field(self):
        countries = Country._default_manager.filter(
            is_shipping_country=True)

        # No need to show country dropdown if there is only one option
        if len(countries) == 1:
            self.fields.pop('country', None)
            self.instance.country = countries[0]
        else:
            self.fields['country'].queryset = countries
            self.fields['country'].empty_label = None

    class Meta:
        model = get_model('order', 'shippingaddress')
        fields = [
            'first_name', 'last_name', 'line3',
            'line1', 'line2', 'line4',
            'state', 'postcode', 'country',
            'phone_number', 'notes',
        ]
        labels = {
            'line1': 'Room Number/Name',
            'line2': 'Building/Wing',
            'line3': 'Department'
        }
        widgets = {
            'line4': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'postcode': forms.HiddenInput(),
            'country': forms.HiddenInput()
        }