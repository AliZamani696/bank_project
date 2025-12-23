from re import A
from django.db import models, transaction
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.fields import related
from django.db.models.query_utils import tree
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_("email is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))] 
        )
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name='balance_cannot_be_negative'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.account_number}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'واریز'),
        ('WITHDRAW', 'برداشت'),
        ('TRANSFER', 'انتقال'),
    )

    transaction_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    sender = models.ForeignKey(Account,on_delete=models.PROTECT,related_name="sent_transactions",null=True,blank=True)
    receiver = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='received_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} to {self.receiver.account_number}"

