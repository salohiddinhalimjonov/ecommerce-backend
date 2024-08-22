from django.contrib import admin
from apps.product.models import Attribute, AttributeValue, Category, Product, ProductVariant, ProductVariantImage, Discount
# Register your models here.
admin.site.register([Attribute, AttributeValue, Category, Product, ProductVariant, ProductVariantImage, Discount])