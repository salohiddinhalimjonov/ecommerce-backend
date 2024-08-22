from django.db import models
from apps.user.models import UserModel
from apps.product.models import ProductVariant
from apps.common.models import BaseModel


class OrderModel(BaseModel):
    NEW = 'new'
    PAID = 'paid'
    PACKAGING = 'packaging'
    DELIVER = 'deliver'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

    STRIPE = 'stripe'
    PAYPAL = 'paypal'
    CASH = 'cash'

    STATUS = (
        (NEW, NEW),
        (PAID, PAID),
        (PACKAGING, PACKAGING),
        (DELIVER, DELIVER),
        (DELIVERED, DELIVERED),
        (CANCELED, CANCELED)
    )
    PAYMENT_TYPE = (
        (STRIPE, STRIPE),
        (PAYPAL, PAYPAL),
        (CASH, CASH)
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS, default=NEW)
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPE, default=CASH)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    price_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    need_courier = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.phone_number} - {self.status} - {self.id}'


class OrderProduct(BaseModel):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.order.id} - {self.quantity}'



class OrderTransaction(BaseModel):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    CANCELED = 'canceled'
    PAYPAL = 'paypal'
    STRIPE = 'stripe'

    STATUS = (
        (PROCESSING, PROCESSING),
        (SUCCESS, SUCCESS),
        (CANCELED, CANCELED)
    )
    PAYMENT_TYPES = (
        (PAYPAL, PAYPAL),
        (STRIPE, STRIPE)
    )

    status = models.CharField(max_length=20, choices=STATUS, default=PROCESSING)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default=STRIPE)
    amount = models.DecimalField(max_digits=21, decimal_places=2)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255, null=True)
    paypal_id = models.CharField(max_length=255, null=True)




