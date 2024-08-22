from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.user.managers import CustomUserManager


class AddressModel(models.Model):
    city = models.CharField(max_length=256, blank=True)
    district = models.CharField(max_length=256, blank=True)
    street = models.CharField(max_length=256, blank=True)
    building_number = models.IntegerField(null=True, blank=True)
    floor = models.IntegerField(null=True, blank=True)
    house_number = models.IntegerField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    comment_for_courier = models.TextField(blank=True)

    def __str__(self):
        return f"{self.city} {self.district}, {self.street}"


class UserModel(AbstractBaseUser, PermissionsMixin):
    MALE = 'male'
    FEMALE = 'female'
    gender_choices = (
        (MALE, MALE),
        (FEMALE, FEMALE)
    )

    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, choices=gender_choices)
    email = models.EmailField(blank=True)
    address = models.ForeignKey(AddressModel, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    admin_password = models.CharField(max_length=256, blank=True)
    objects = CustomUserManager()
    password = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            if not self.admin_password:
                return ValueError('Admin Password must be set!')
            else:
                self.admin_password = make_password(self.admin_password)
        super(UserModel, self).save(*args, **kwargs)


    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"






