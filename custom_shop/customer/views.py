from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from oscar.apps.customer.utils import get_password_reset_url
from oscar.apps.customer.views import PageTitleMixin, CustomerDispatcher, ProfileView

from custom_shop.customer.forms import CustomProfileForm


class ProfileView(ProfileView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile_fields'] = self.get_profile_fields(self.request.user)
        return ctx


class ProfileUpdateView(PageTitleMixin, generic.FormView):
    form_class = CustomProfileForm
    template_name = 'oscar/customer/profile/profile_form.html'
    page_title = _('Edit Profile')
    active_tab = 'profile'
    success_url = reverse_lazy('customer:profile-view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        User = get_user_model()
        # Grab current user instance before we save form.  We may need this to
        # send a warning email if the email address is changed.
        try:
            old_user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            old_user = None

        final_form = form.save(commit=False)
        final_form.is_profile_complete = True
        final_form.save()

        # We have to look up the email address from the form's
        # cleaned data because the object created by form.save() can
        # either be a user or profile instance depending whether a profile
        # class has been specified by the AUTH_PROFILE_MODULE setting.
        new_email = form.cleaned_data.get('email')
        if new_email and old_user and new_email != old_user.email:
            # Email address has changed - send a confirmation email to the old
            # address including a password reset link in case this is a
            # suspicious change.
            self.send_email_changed_email(old_user, new_email)

        messages.success(self.request, _("Profile updated"))
        return redirect(self.get_success_url())

    def send_email_changed_email(self, old_user, new_email):
        user = self.request.user
        extra_context = {
            'user': user,
            'reset_url': get_password_reset_url(old_user),
            'new_email': new_email,
            'request': self.request,
        }
        CustomerDispatcher().send_email_changed_email_for_user(old_user, extra_context)
