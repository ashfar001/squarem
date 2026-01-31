from django import template
from decimal import Decimal
import re

register = template.Library()


@register.filter(name='indian_currency')
def indian_currency(value):
    """
    Format number in Indian currency format with commas.
    Example: 118000 -> 1,18,000
    """
    try:
        value = Decimal(str(value))
        # Handle negative numbers
        negative = value < 0
        value = abs(value)
        
        # Split into integer and decimal parts
        value_str = str(int(value))
        
        # Indian number system: first 3 digits from right, then groups of 2
        if len(value_str) <= 3:
            formatted = value_str
        else:
            # Last 3 digits
            last_three = value_str[-3:]
            # Remaining digits
            remaining = value_str[:-3]
            # Group remaining digits in pairs from right
            pairs = []
            while len(remaining) > 2:
                pairs.insert(0, remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                pairs.insert(0, remaining)
            
            formatted = ','.join(pairs) + ',' + last_three
        
        if negative:
            formatted = '-' + formatted
            
        return formatted
    except (ValueError, TypeError, AttributeError):
        return value


@register.filter(name='rupees')
def rupees(value):
    """
    Format number as Indian Rupees with ₹ symbol.
    Example: 118000 -> ₹ 1,18,000
    """
    formatted = indian_currency(value)
    return f'₹ {formatted}'
