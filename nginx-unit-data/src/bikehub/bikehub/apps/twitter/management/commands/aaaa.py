
import facebook
from django.core.management.base import BaseCommand
from pyfacebook import Api


class Command(BaseCommand):
    def handle(self, **options):
        print('')

        api = Api(
            app_id="1502348186620726",
            app_secret="58509599078ef68b0dcd09779fa5092b",
            application_only_auth=True
        )
        print(api)
        # api = Api(
        #     app_id="1502348186620726",
        #     app_secret="58509599078ef68b0dcd09779fa5092b",
        #     application_only_auth=True
        # )
