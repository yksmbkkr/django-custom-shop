def on_order_placed(sender, order, user, **kwargs):
    from oscar.core.loading import get_class
    ShopOrderModel = get_class('catalogue.models', 'ShopOrder')
    shops = {}
    for line_item in order.lines.all():
        shop = line_item.product.categories.first().get_ancestors_and_self()[0]
        shops[shop.id] = shop

    for shop in shops:
        shop_order = ShopOrderModel(
            shop=shops[shop],
            order=order,
        )
        shop_order.save()