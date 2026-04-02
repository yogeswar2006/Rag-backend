from django.db import models

# Create your models here.

    # for later (project)
    
# class SlackIntegration(models.Model):
#     company = models.OneToOneField(
#         "companies.Company",
#         on_delete=models.CASCADE
#     )

#     slack_team_id = models.CharField(max_length=100, unique=True)

#     bot_access_token = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "slack_integrations"