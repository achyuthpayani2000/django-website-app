from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class App(models.Model):
    app_name = models.CharField(max_length=255)
    no_of_points = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.app_name
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and save a regular user with the given email and password
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a superuser with the given email and password
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password=models.CharField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    objects = CustomUserManager()
    username=models.CharField(unique=True)
    app=models.ManyToManyField(App)
    role=models.CharField(default='Admin')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name','password','role','email']

    def _str_(self):
        return self.username
    

### App Model
