from django.db import models
import uuid
# Create your models here.



class Company(models.Model):
    PLAN_CHOICES = [
        ("free","FREE"),
        ("pro","PRO"),
        ("enterprice","ENTERPRICE")
    ]
    
    id=models.UUIDField(
        editable=False,
        primary_key=True,
        default=uuid.uuid4
    )
    
    name = models.CharField(
        max_length=230
    )
    slug=models.SlugField(
        max_length=230,
        unique=True
    )
    plan_type = models.CharField(max_length=30,choices=PLAN_CHOICES,default="free")
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='companies'
        indexes=[
            models.Index(fields=["slug"]),
            models.Index(fields=["plan_type"])
        ]
    def __str__(self):
        return self.name