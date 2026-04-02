from django.db import models

# Create your models here.
import uuid


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="documents"
    )

    uploaded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True
    )

    file_name = models.CharField(max_length=255)

    file = models.FileField(upload_to="documents/")

    status = models.CharField(
        max_length=20,
        choices=[
            ("uploaded", "Uploaded"),
            ("processing", "Processing"),
            ("ready", "Ready"),
            ("failed", "Failed"),
        ],
        default="uploaded"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "documents"
        indexes = [
            models.Index(fields=["company"]),
        ]