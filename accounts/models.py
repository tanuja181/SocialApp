from django.db import models

from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager

from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

from autoslug import AutoSlugField


class CustomAccountManager(BaseUserManager):
    def create_user(self, email,phone ,username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not phone:
            raise ValueError("users must have phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone,username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30)
    phone_regex             = RegexValidator(regex=r'^\+?1?\d{9,14}$', message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone                   = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username','email']

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

class ConnectionReuest(models.Model):

    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class Connections(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    connections =models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.user.email

