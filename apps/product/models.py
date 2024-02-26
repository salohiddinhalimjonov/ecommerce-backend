from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.common.utils import compress_image


class Brannd(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product/brand/%Y/%m/%d/', null=True, blank=True)

    def save(self, *args, **kwargs):
        image = self.image
        if image:
            if image.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.image = compress_image(image)
        super(Brannd, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Attribute(models.Model):
    title = models.CharField(max_length=256)
    category = models.ManyToManyField("Category")

    def __str__(self):
        return self.title


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.attribute.title} - {self.value}'


class Category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product/category/%Y/%m/%d/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    level = models.IntegerField(default=1)


    def save(self, *args, **kwargs):
        image = self.image
        if image:
            if image.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.image = compress_image(image)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product/product_main/%Y/%m/%d/', null=True, blank=True)
    price = models.DecimalField(max_digits=21, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_new = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        image = self.image
        if image:
            if image.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.image = compress_image(image)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    attribute_value = models.ManyToManyField(AttributeValue)
    other_detail = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()


    def __str__(self):
        return f'{self.product.title} - {self.quantity}'


class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/product_variant/%Y/%m/%d/')
    order = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        image = self.image
        if image:
            if image.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.image = compress_image(image)
        super(ProductVariantImage, self).save(*args, **kwargs)


class Discount(models.Model):
    product = models.ManyToManyField(Product)
    product_variant = models.ManyToManyField(ProductVariant)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    percent = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'{self.priduct.title} - {self.percent} - {self.id}'

