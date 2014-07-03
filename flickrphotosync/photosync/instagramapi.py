import pytz
import time
import datetime as date

from instagram.client import InstagramAPI
from django.conf import settings
from django.core.cache import cache


class Instagram(object):

    api = None
    api_access_token = settings.INSTAGRAM_ACCESS_TOKEN
    user_id = settings.INSTAGRAM_GET_USER
    weeks = settings.INSTAGRAM_WEEKS
    min_timestamp = int(time.time()) - date.timedelta(weeks=weeks).total_seconds()

    def __init__(self):
        self.api = InstagramAPI(access_token=self.api_access_token)

    def get_collection(self, user_id=None):
        if not user_id:
            user_id = self.user_id
        return self.api.user_recent_media(user_id=user_id, count=1000, min_timestamp=int(self.min_timestamp))

    def get_next_with_url(self, url=None, user_id=None):
        if not user_id:
            user_id = self.user_id
        return self.api.user_recent_media(user_id=user_id, with_next_url=url)
