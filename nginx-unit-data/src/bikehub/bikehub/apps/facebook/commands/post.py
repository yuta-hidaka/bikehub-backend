
import facebook
from django.core.management.base import BaseCommand
import facebook

MAX_FOLLOW = 200


class Command(BaseCommand):
    def handle(self, **options):

        graph = facebook.GraphAPI(app_secret="58509599078ef68b0dcd09779fa5092b", version="2.12")
        print(graph)
        # api = Api(
        #     app_id="1502348186620726",
        #     app_secret="58509599078ef68b0dcd09779fa5092b",
        #     application_only_auth=True
        # )
