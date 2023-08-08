from django import template

register = template.Library()

# 템플릿 필터
@register.filter
def avg(value, arg):
    if arg==0:
        return 0
    return int((value / arg) * 100)
