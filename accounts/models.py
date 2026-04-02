
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .userManger import UserManager
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255, blank=True)

    username = None  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects= UserManager()  # type:ignore

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True
    )

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="member"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self):
        return self.email