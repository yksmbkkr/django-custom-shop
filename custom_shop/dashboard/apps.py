import oscar.apps.dashboard.apps as apps
from django.urls import path, include



class DashboardConfig(apps.DashboardConfig):
    name = 'custom_shop.dashboard'

    permissions_map = {
        'index': (['is_staff'], ['partner.dashboard_access'], ['coreapp.can_view_oms']),
        'order-overview': (['is_staff'], ['partner.dashboard_access'], ['catalogue.view_shoporder'],),
        'order-filter': (['is_staff'], ['partner.dashboard_access'], ['catalogue.view_shoporder'],),
        'manage-shops': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
        'update-shop': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
    }

    def get_urls(self):
        from django.contrib.auth import views as auth_views
        from custom_shop.dashboard.views import shop_control, order_overview, order_list_filtered

        urls = [
            path('', self.index_view.as_view(), name='index'),
            path('catalogue/', include(self.catalogue_app.urls[0])),
            path('reports/', include(self.reports_app.urls[0])),
            path('orders/', include(self.orders_app.urls[0])),
            path('users/', include(self.users_app.urls[0])),
            path('pages/', include(self.pages_app.urls[0])),
            path('partners/', include(self.partners_app.urls[0])),
            path('offers/', include(self.offers_app.urls[0])),
            path('ranges/', include(self.ranges_app.urls[0])),
            path('reviews/', include(self.reviews_app.urls[0])),
            path('vouchers/', include(self.vouchers_app.urls[0])),
            path('comms/', include(self.comms_app.urls[0])),
            path('shipping/', include(self.shipping_app.urls[0])),
            path('login/', self.login_view.as_view(), name='login'),
            path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
            path('manage-shops/', shop_control, name='manage-shops'),
            path('manage-shops/<int:uid>/', shop_control, name='update-shop'),
            path('order-views/overview/', order_overview, name='order-overview'),
            path('order-views/filter/', order_list_filtered, name='order-filter')
        ]
        return self.post_process_urls(urls)
