from modeltranslation.translator import translator, TranslationOptions
from apps.product.models import ProductVariant


class ProductVariantTranslationOptions(TranslationOptions):
    fields = ["other_detail"]

translator.register(ProductVariant)