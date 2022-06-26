import random
import string

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        username = username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    # username = None

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    POSITIONS = (
        ('senior', 'senior'),
        ('registerer', 'registerer'),
        ('investigator', 'investigator'),
        ('complaint', 'complaint'),
        ('Admin', 'Admin'),

    )
    #
    # NATION = (
    #     ('TANZANIA', 'TANZANIA'),
    #     ('KENYA', 'KENYA'),
    #
    # )
    phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                    "'0.....'. Up to 10 digits allowed.")

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        null=True, blank=True
    )
    first_name = models.CharField(max_length=100, null=True, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    last_name = models.CharField(max_length=100, null=True, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True,null=True,unique=True)  # validators
    # should be a list
    sex = models.CharField(choices=GENDER, max_length=1, null=True, blank=True)
    title = models.CharField(choices=POSITIONS, max_length=40, null=False, default=" ")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser
    residency = models.ForeignKey('District', on_delete=models.CASCADE, null=True,blank=True)
    station = models.ForeignKey('Station', on_delete=models.CASCADE, null=True, related_name="user_staff_station")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    def __str__(self):
        return "{0}-{1}-({2})".format(self.first_name, self.last_name,self.station)


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Complainant(models.Model):
    code = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user_complainant")
    registered_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if len(self.code) < 4:
            self.code = id_generator()

        return super(Complainant, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Complainant"
        verbose_name_plural = "Complainant"

    def __str__(self):
        return "{0}".format(self.code)
