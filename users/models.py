from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import EmailField


class UserManager(BaseUserManager):
    """
    Custom User manager
    """
    use_in_migrations = True

    def create_superuser(self, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        user = self.model(email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model derived from AbstractBaseUser
    """
    email = EmailField('email address',
                       help_text='Required. Valid email address '
                                 'of the user', unique=True,
                       null=False, blank=False)
    name = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField('Active Status', help_text=(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'), default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
