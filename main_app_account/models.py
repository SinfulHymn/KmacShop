from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.mail import send_mail

# this is the manager for the user model (the database)
class CustomAccountManager(BaseUserManager):
    # this is the manager for the CustomUser model
    # create_superuser is a method that creates a superuser
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
            
        return self.create_user(email, user_name, password, **other_fields)
    # create_user is a method that creates a user
    def create_user(self, email, user_name, password, **other_fields):
        # if the email is not provided, raise an error
        if not email:
            raise ValueError(_('You must provide an email address'))
        # this is the other_fields that are not required
        # check if email is formatted correctly
        email = self.normalize_email(email)
        # store the email and user_name in the database
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

# this is the model for the user
class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    # delivery address
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    # user status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # this is the manager for the CustomUser model
    objects = CustomAccountManager()

    # username is email
    USERNAME_FIELD = 'email'
    # required for admin
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']
    
    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name