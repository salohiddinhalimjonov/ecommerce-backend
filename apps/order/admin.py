from django.contrib import admin
from apps.order.models import OrderModel, OrderProduct, OrderTransaction
# Register your models here.
admin.site.register([OrderModel, OrderProduct, OrderTransaction])

