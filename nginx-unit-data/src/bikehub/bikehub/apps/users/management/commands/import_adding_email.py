from django.core.management.base import BaseCommand
import json
from users.models import CustomUser
from allauth.account.models import EmailAddress

class Command(BaseCommand):

    def handle(self, **options):
     print("adding Email")
     users = CustomUser.objects.all()

     for user in users:
         EmailAddress.objects.get_or_create(
             user= user,
             email= user.email,
             verified = True,
             primary = True
         )

