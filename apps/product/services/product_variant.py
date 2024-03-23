from decimal import Decimal
from datetime import datetime


def calculate_discount_price(price, percent, amount):
    if percent is not None:
        return {
            "is_percent": True, "percent": percent,
            "new_price": price - (price * Decimal(percent / 100))
        }
    else:
        return {"is_percent": False, "amount": amount, "new_price": price - amount}


def get_price_with_discount(instance, user):
    today = datetime.now()

    product_variant_discounts = instance.discounts.filter(start_date__lte=today, end_date__gte=today)
    product_discounts = instance.product.discounts.filter(start_date__lte=today, end_date__gte=today)

    if product_variant_discounts.exists():
        discount = product_variant_discounts.first()
        return calculate_discount_price(instance.price(user), discount.percent, discount.amount)
    elif product_discounts.exists():
        discount = product_discounts.first()
        return calculate_discount_price(instance.price(user), discount.percent, discount.amount)
    else:
        return None
