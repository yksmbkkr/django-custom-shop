from oscar.apps.checkout.views import PaymentMethodView


class PaymentMethodView(PaymentMethodView):
    def get(self, request, *args, **kwargs):
        # By default we redirect straight onto the payment details view. Shops
        # that require a choice of payment method may want to override this
        # method to implement their specific logic.
        return self.get_success_response()