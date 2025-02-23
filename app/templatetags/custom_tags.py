from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def calculate_total(cart_items):
    total = 0
    for item in cart_items:
        total += item.product.offer_price * item.quantity
    return total