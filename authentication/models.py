from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.db import models, transaction


class CustomAccountManager(BaseUserManager):

    @transaction.atomic
    def create_user(self, email, first_name, last_name, password):
        """Creates and saves a User with the given email first_name, last_name."""
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Creates and saves a superuser with the given email, first_name, last_name."""
        user = self.create_user(email=email, first_name=first_name,
                                last_name=last_name, password=password,
                                )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether this user can access this admin site.',
        verbose_name='is staff'
    )
    is_active = models.BooleanField(
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        verbose_name='is active'
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=('Designates that this user has all permissions without '
                   'explicitly assigning them.'),
        verbose_name='is superuser'
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    last_login = models.DateTimeField('last login', blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.id}, {self.email}"

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-id',)
