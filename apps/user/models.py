from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('The Email field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class UserModel(AbstractBaseUser):
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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(selfself, app_label):
        return True




