from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()
# Create your models here.
import uuid

class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title or 'Chat'}"

class QueryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatRoom = models.ForeignKey(ChatRoom,null=True,blank=True,on_delete=models.CASCADE)
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="queries"
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True
    )

    question = models.TextField()

    response = models.TextField()

    tokens_used = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "query_logs"
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["created_at"]),
        ]