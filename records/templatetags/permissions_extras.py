from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Возвращает True, если пользователь состоит в группе с именем group_name."""
    return user.groups.filter(name=group_name).exists()
