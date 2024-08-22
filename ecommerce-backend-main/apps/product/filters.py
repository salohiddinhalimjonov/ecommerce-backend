from django.db.models import Sum
from django.db.models.functions import Coalesce
from django_filters.rest_framework import FilterSet
from django_filters import CharFilter, BooleanFilter, NumberFilter
from apps.product.models import ProductVariant


class ProductVariantFilter(FilterSet):
    min_price = CharFilter(method='get_price_gte', label='Price GTE')
    max_price = CharFilter(method='get_price_lte', label='Price LTE')
    #is_popular = BooleanFilter(method='get_is_popular', label='Is Popular')

    class Meta:
        model = ProductVariant
        fields = [
            'attribute_value',
            'product',
            'product__category',
            'attribute_value__value',
        ]

    def get_price_gte(self, queryset, name, value):
        # user = self.request.user
        # if user.is_authenticated:
        #     key = f'price_for_{user.user_type}__gte'
        #     filter = {key: value}
        #     return queryset.filter(**filter)
        return queryset.filter(price_for_private__gte=value)

    def get_price_lte(self, queryset, name, value):
        # user = self.request.user
        # if user.is_authenticated:
        #     key = f'price_for_{user.user_type}__lte'
        #     filter = {key: value}
        #     return queryset.filter(**filter)
        return queryset.filter(price_for_private__lte=value)

    # def get_is_popular(self, queryset, name, value):
    #     if value is True:
    #         queryset = queryset.annotate(
    #             total_quantity=Coalesce(Sum('order_products__quantity'), 0)
    #         ).order_by('-total_quantity')
    #     return queryset
