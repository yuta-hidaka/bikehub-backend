
import facebook
from django.conf import settings


def post(message, link):
    access_token = settings.FACEBOOK_ACCESS_TOKEN
    graph = facebook.GraphAPI(access_token=access_token)
    graph.put_object(
        parent_object='me',
        connection_name='feed',
        message=message,
        link=link
    )
