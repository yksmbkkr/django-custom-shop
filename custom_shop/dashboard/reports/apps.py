import oscar.apps.dashboard.reports.apps as apps


class ReportsDashboardConfig(apps.ReportsDashboardConfig):
    name = 'custom_shop.dashboard.reports'

    default_permissions = (['is_staff', ], ['partner.add_partner'], ['order.change_shippingaddress'])
