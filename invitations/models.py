from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Invitation(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    company= models.ForeignKey('companies.Company',on_delete=models.CASCADE,related_name="invitations")
    
    created_by = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    
    
    token = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at= models.DateTimeField()
    
    def is_valid(self):
        return not self.is_used and self.expires_at>timezone.now()
    
    class Meta:
        db_table="invitations"
    
    def __str__(self):
        return str(self.token)