from django.db.models import Min
from rest_framework.exceptions import ValidationError

from apps.product.models import ProductVariant



def has_product_variant_in_products(attrs):
    products = attrs.get('products')
    product_variants = attrs.get('product_variants')

    product_variant_ids = []
    is_duplicated = False

    if products is not None:
        for product in products:
            product_variant_ids += product.productvariant_set.values_list('id', flat=True)
    if product_variants is not None:
        for product_variant in product_variants:
            if not product_variant.id in product_variant_ids:
                product_variant_ids.append(product_variant.id)
            else:
                is_duplicated = True

    return is_duplicated, product_variant_ids



def check_discount_date(attrs):
    start_date = attrs.get('start_date')
    end_date = attrs.get('end_date')

    if end_date < start_date:
        raise ValidationError(detail="start_date must be less than end_date")



def percent_or_amount(attrs):
    percent = attrs.get('percent')
    amount = attrs.get('amount')

    if (percent is None and amount is None) or (percent is not None and amount is not None):
        raise ValidationError(detail="percent or amount must be set")

    if percent is not None:
        if not 0 <= percent <= 100:
            raise ValidationError(detail="percent must be between 0 and 100")

    return


def check_product_variant_is_duplicated(attrs):
    is_duplicated, _ = has_product_variant_in_products(attrs)
    if is_duplicated:
        raise ValidationError(detail="product_variant is duplicated")



def check_discount_product_variant(attrs):
    product_variants = attrs.get('product_variants')
    products = attrs.get('products')
    start_date = attrs.get('start_date')
    end_date = attrs.get('end_date')

    if product_variants is not None:
        for product_variant in product_variants:
            if product_variant.discounts.filter(
                    is_active=True, start_date__gte=start_date, end_date__lte=end_date).exists():
                raise ValidationError(detail="discount in product_variant is already exists")

    if products is not None:
        for product in products:
            if product.discounts.filter(
                    is_active=True, start_date__gte=start_date, end_date__lte=end_date).exists():
                raise ValidationError(detail="discount in product is already exists")



def check_price(attrs):
    amount = attrs.get('amount', 0)
    _, product_variant_ids = has_product_variant_in_products(attrs)
    min_price = ProductVariant.objects.filter(
        id__in=product_variant_ids).aggregate(
        min_price=Min(f'price_for_private')
    )
    if min_price.get('min_price') is not None and amount is not None:
        if amount > min_price.get('min_price'):
            raise ValidationError(detail={
                "message": "amount must be less than min_price",
                "min_price": min_price.get('min_price')
            })



def discount_validators(request, attrs):
    check_discount_date(attrs)
    percent_or_amount(attrs)
    check_product_variant_is_duplicated(attrs)
    check_price(attrs)
    if request.method == "POST":
        check_discount_product_variant(attrs)


