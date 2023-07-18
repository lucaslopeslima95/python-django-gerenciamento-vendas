from django import template

register = template.Library()

@register.simple_tag
def calculate_value(quantity, price, decimal_places):
    value = quantity * float(price)
    formatted_value = "{:.{}f}".format(value, decimal_places)
    return formatted_value
