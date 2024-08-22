from django.contrib import admin
from apps.user.models import UserModel, AddressModel
# Register your models here.
admin.site.register([UserModel, AddressModel])