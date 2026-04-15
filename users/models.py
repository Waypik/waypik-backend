# imports the models module from django.db package
from django.db import models
# imports used when creating custom user model
# allows for overriding the default User model to fit specific needs(eg; email auth instead of username for login)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone=None, email=None, password=None, **extra_fields):
        """
        Create and save a regular user.
        Requires either phone (for phone-based auth) or email (for social auth).
        """
        if not phone and not email:
            raise ValueError("Either phone number or email is required")

        # Normalize email if provided
        if email:
            email = self.normalize_email(email)

        user = self.model(phone=phone, email=email, **extra_fields)

        # Set password (will be hashed automatically)
        if password:
            user.set_password(password)
        else:
            # For social auth users, set an unusable password
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.SUPERADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone=phone, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "Super Admin"
        ADMIN = "ADMIN", "Transport Admin"
        DRIVER = "DRIVER", "Driver"
        PASSENGER = "PASSENGER", "Passenger"

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PASSENGER
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone} ({self.role})"
