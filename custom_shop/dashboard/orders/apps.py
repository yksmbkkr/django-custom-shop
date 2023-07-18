import oscar.apps.dashboard.orders.apps as apps


class OrdersDashboardConfig(apps.OrdersDashboardConfig):
    name = 'custom_shop.dashboard.orders'

    default_permissions = (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] )
    permissions_map = {
        'order-list': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
        'order-stats': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
        'order-detail': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
        'order-detail-note': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
        'order-line-detail': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
        'order-shipping-address': (['is_staff',], ['order.change_shippingaddress'], ['partner.add_partner'] ),
    }
