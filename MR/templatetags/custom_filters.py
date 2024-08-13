from django import template

register = template.Library()

@register.filter
def calculate_total_quantity(items):
    return sum(item.quantity for item in items)

@register.filter
def calculate_total_no_of_unit(items):
    return sum(item.no_of_unit for item in items)

@register.filter
def filter_by_month(items, month):
    return items.filter(MR_no__MR_date__month=month)

@register.filter
def filter_by_branch(items, branch):
     return items.filter(MR_no__branch=branch)