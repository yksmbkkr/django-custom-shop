from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from oscar.core.loading import get_class

from coreapp.models import UserTypeChoice


UniversityDepartment = get_class('address.models', 'UniversityDepartment')

class CustomProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        required=False,
        queryset=UniversityDepartment.objects.filter(is_active=True),
        help_text='Required, if user is not a student',
        empty_label='Please select a department.'
    )

    def __init__(self, user, *args, **kwargs):
        User = get_user_model()
        instance = User.objects.get(username=user.username)
        kwargs['instance'] = instance

        super().__init__(*args, **kwargs)

        # # Get profile field names to help with ordering later
        # profile_field_names = list(self.fields.keys())
        #
        # # Get user field names (we look for core user fields first)
        # core_field_names = set([f.name for f in User._meta.fields])
        # user_field_names = ['email']
        # for field_name in ('first_name', 'last_name'):
        #     if field_name in core_field_names:
        #         user_field_names.append(field_name)
        # user_field_names.extend(User._meta.additional_fields)
        #
        # # Store user fields so we know what to save later
        # self.user_field_names = user_field_names
        #
        # # Add additional user form fields
        # additional_fields = forms.fields_for_model(
        #     User, fields=user_field_names)
        # self.fields.update(additional_fields)

        # Ensure email is required and initialised correctly
        self.fields['email'].required = True
        self.fields['email'].disabled = True

        # Set initial values
        # for field_name in user_field_names:
        #     self.fields[field_name].initial = getattr(user, field_name)
        #
        # # Ensure order of fields is email, user fields then profile fields
        # self.fields.keyOrder = user_field_names + profile_field_names

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['user_type'] is UserTypeChoice.PROF and not cleaned_data['department']:
            self.add_error("department", "This field is required if user is not student.")

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'user_type', 'department']