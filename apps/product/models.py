from django.db import models
from apps.common.utils import upload
from apps.common.models import BaseModel



class Attribute(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.attribute.title} - {self.value}'


class Category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='priduct/category/%Y/%m/%d/')
    parent = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Product(BaseModel):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to=upload)
    is_new = models.BooleanField(default=False)

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
    image = models.ImageField(upload_to=upload)
    order = models.IntegerField(default=1)


class Discount(models.Model):
    product = models.ManyToManyField(Product)
    product_variant = models.ManyToManyField(ProductVariant)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    percent = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'{self.priduct.title} - {self.percent} - {self.id}'

