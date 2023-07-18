from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_my_android_app(context):
    if 'my-android-app-flag' in context['request'].COOKIES:
        flag_value = context['request'].COOKIES['my-android-app-flag']
        return 'true' in flag_value
    return False