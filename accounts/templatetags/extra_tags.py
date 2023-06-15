from django import template

register = template.Library()


@register.filter(name="addstr")
def addstr(arg1, arg2) -> str:
    return str(arg1) + str(arg2)
