from datetime import datetime
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from apps.common.models import BaseModel
from apps.common.utils import compress_image
from apps.user.models import UserModel


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
    category = models.ManyToManyField("Category", related_name='attributes')

    def __str__(self):
        return self.title


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values_hi')
    value = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.attribute.title} - {self.value}'


class Category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product/category/%Y/%m/%d/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    level = models.IntegerField(default=1)


    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.image = compress_image(self.image)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    title = models.CharField(max_length=255)
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
    product = models.ManyToManyField(Product, related_name='discounts')
    product_variant = models.ManyToManyField(ProductVariant, related_name='discounts')
    name = models.CharField(max_length=100)
    amount = models.PositiveSmallIntegerField(null=True, blank=True)
    percent = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return self.name


# class ProductReview(BaseModel):
#     product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviews')
#     content = models.TextField(blank=True, null=True)
#     stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#
#     class Meta:
#         ordering = ['-created_datetime']
#         unique_together = ['product', 'user']
#         verbose_name = 'Product Review'
#         verbose_name_plural = 'Product Reviews'



@receiver(pre_save, sender=Discount)
def status(sender, instance, *args, **kwargs):
    today = date.today()
    if instance.start_date <= today <= instance.end_date:
        instance.is_active = True
    else:
        instance.is_active = False
