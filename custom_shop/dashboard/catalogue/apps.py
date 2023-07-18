import oscar.apps.dashboard.catalogue.apps as apps


class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'custom_shop.dashboard.catalogue'

    default_permissions = (['is_staff'], ['partner.dashboard_access', 'catalogue.add_product'], ['catalogue.add_product'],)
    permissions_map = {
        'catalogue-product': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
        'catalogue-product-create': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
        'catalogue-product-list': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
        'catalogue-product-delete': (['is_staff'], ),
        'catalogue-product-lookup': (['is_staff'], ['partner.dashboard_access'], ['catalogue.add_product'],),
        'stock-alert-list': (['is_staff'], ),
        'catalogue-class-list': (['is_staff'], ),
        'catalogue-class-create': (['is_staff'], ),
        'catalogue-class-update': (['is_staff'], ),
        'catalogue-class-delete': (['is_staff'], ),
    }
