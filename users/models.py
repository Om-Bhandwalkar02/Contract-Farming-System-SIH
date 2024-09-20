from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, contact, full_name, password=None, **extra_fields):
        if not contact:
            raise ValueError("The Phone Number must be set")
        user = self.model(contact=contact, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(contact, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):  # Added PermissionsMixin
    user_id = models.AutoField(primary_key=True)  # Primary key field

    # Using PhoneNumberField for contact, with the region set to India
    contact = PhoneNumberField(unique=True, region='IN')

    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=(('farmer', 'Farmer'), ('buyer', 'Buyer')))
    aadhar_number = models.CharField(max_length=12, unique=True)
    aadhar_certificate = models.FileField(upload_to='media/aadhar/')
    farmer_certificate = models.FileField(upload_to='media/certificates/', null=True, blank=True)
    buyer_certificate = models.FileField(upload_to='media/certificates/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['full_name', 'aadhar_number']

    objects = UserManager()

    def __str__(self):
        return str(self.contact)  # changes during contracts
