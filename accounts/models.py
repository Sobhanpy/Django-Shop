from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            """
            Create and save a user with the given email and password.
            """
            if not email:
                raise ValueError("The Email must be set")
            if not password:
                raise ValueError("Password is required")
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email, password=None, **extra_fields):
            """
            Create and save a SuperUser with the given email and password.
            """
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("type", "admin")
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)
            extra_fields.setdefault("is_verified", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError("Superuser must have is_staff=True.")
            if extra_fields.get("is_superuser") is not True:
                raise ValueError("Superuser must have is_superuser=True.")
            if extra_fields.get("is_verified") is not True:
                raise ValueError("Superuser must have is_verified=True.")
            if extra_fields.get("type") != "admin":
                raise ValueError("Superuser must have type='admin'")
            return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email


def validate_mobile(value):
    if value and Profile.objects.filter(mobile=value).exists():
        raise ValidationError('این شماره قبلا استفاده شده است')

def validate_idcode(value):
    if value and Profile.objects.filter(id_code=value).exists():
        raise ValidationError('این کد ملی قبلا استفاده شده است')


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birthday = models.DateField(null=True, blank=True)
    # fro varification phone number with regex 
    mobile_validator = RegexValidator(
        regex=r'^09\d{9}$',
        message='شماره موبایل باید با 09 شروع شود، شامل فقط اعداد باشد و 11 رقم داشته باشد.',
    )
    mobile = models.CharField(
        max_length=11, validators=[mobile_validator], unique=True
    )
    id_code_validator = RegexValidator(
        regex=r'^\d{10}$',
        message=' کد ملی باید 10 کارکتر عددی باشد و تکراری نباشد',
    )
    id_code = models.CharField(
        max_length=10, validators=[id_code_validator], unique=True
    )
    phone_validator = RegexValidator(
        regex=r'^0[1-8]\d{9}$',
        message='تلفن ثابت باید با 0 و پیش شماره شهرستان باشد و 11 رقم داشته باشد',
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
    )
    card_number_validator = RegexValidator(
        regex=r'^\d{16}$', message='شماره کارت باید 16 کارکتر عددی باشد'
    )
    card_number = models.CharField(
        max_length=16,
        validators=[card_number_validator],
        default='0000000000000000',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def get_addresses(self):
        return self.addresses.all()

    def get_orders(self):
        return self.orders.all()

    def last_address(self):
        return self.addresses.all()[0]


class Province(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=20)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class UserAddress(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='addresses',
    )
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete_address = models.CharField(max_length=250)
    postal_code_validator = RegexValidator(
        regex=r'^[1-9]\d{9}$', message='کد پستی باید 10 کارکتر عددی باشد'
    )
    postal_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[postal_code_validator],
    )
    receiver = models.CharField(max_length=50, default="خودم")

    def __str__(self):
        return (
            str(self.profile.user.email)
            + ' - '
            + str(self.city.name)
            + ' - '
            + str(self.province.name)
        )

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
        ordering = ['-created_at']
