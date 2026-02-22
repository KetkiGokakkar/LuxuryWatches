from django import template

register = template.Library()


@register.filter
def currency_inr(value):
    try:
        val = float(value)
        if val >= 10000000:
            return f"₹{val/10000000:.2f} Cr"
        elif val >= 100000:
            return f"₹{val/100000:.2f} L"
        else:
            return f"₹{val:,.0f}"
    except (ValueError, TypeError):
        return value


@register.filter
def star_range(value):
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_star_range(value):
    try:
        return range(5 - int(value))
    except (ValueError, TypeError):
        return range(5)


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
