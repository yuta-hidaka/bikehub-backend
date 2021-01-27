from apiclient.discovery import build
from apiclient.errors import HttpError
from django.conf import settings
from news.models import News

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = settings.YOUTUBE_ACCESS_TOKEN
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"
SOURCE_HREF = "https://www.youtube.com"


class youtube():

    def search(self, query='google', max_results=2, order='date'):
        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY
        )
        # Call the search.list method to retrieve results associated with the
        # specified Freebase topic.
        
        try:
            search_response = youtube.search().list(
                q=query,
                order=order,
                part="id,snippet",
                maxResults=max_results
            ).execute()
        except HttpError as e:
            print(e)

        return self._parse_as_news_entries(search_response.get("items", []))

    def _parse_as_news_entries(self, data_list=None) -> list:
        """Create data as rss entries.
        """
        response = []
        for data in data_list:
            response.append({
                'title': data['snippet']['title'],
                'summary': data['snippet']['description'],
                'featured_image': data['snippet']['thumbnails']['high']['url'],
                'video_id': data['id']['videoId'],
                'source': {
                    'title': data['snippet']['channelTitle'],
                    'href': f'{SOURCE_HREF}/channel/{data["snippet"]["channelId"]}'
                },
                'links': [{
                    'href': f'{SOURCE_HREF}/watch?v={data["id"]["videoId"]}'
                }]
            })

        return response
