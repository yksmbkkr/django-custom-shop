import oscar.apps.dashboard.partners.apps as apps


class PartnersDashboardConfig(apps.PartnersDashboardConfig):
    name = 'custom_shop.dashboard.partners'
    default_permissions = (['is_staff'], ['partner.add_partner'] )
