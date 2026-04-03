from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser if it does not exist"

    def handle(self, *args, **kwargs):
       
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

        if not User.objects.filter(email=email).exists():
            self.stdout.write("Creating superuser...")
            User.objects.create_superuser(
                username=email,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write("Superuser already exists")