from django import template
from django.template.loader import select_template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_current_category_menu(context):
    if 'product' in context and context['product'] is not None:
        return context['product'].categories.all()[0].get_ancestors()[0].get_descendants().order_by('name')
    if 'category' in context and context['category'] is not None:
        return context['category'].get_ancestors_and_self()[0].get_descendants().order_by('name')
    else:
        return None