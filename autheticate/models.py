from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class CustomUserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
GENDER_OPTIONS = [
    ('MALE', 'male'),
    ('FEMALE', 'female')
]


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default = uuid.uuid4, primary_key= True, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    profile_picture  = models.ImageField(upload_to="profile/", null= True, blank=True)
    address = models.TextField(null = True, blank = True)
    gender= models.CharField(max_length=6, choices=GENDER_OPTIONS)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email 
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            "access_token": str(refresh.access_token),
            "refresh_token" : str(refresh)
        }