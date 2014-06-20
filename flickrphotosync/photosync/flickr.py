import pytz
import flickrapi
import datetime as date

from flickrapi.shorturl import url
from django.conf import settings
from django.core.cache import cache


class Flickr(object):

    api = None
    api_key = settings.FLICKR_API_KEY
    api_secret = settings.FLICKR_SECRET_KEY
    api_token = settings.FLICKR_AUTH_TOKEN
    api_token_secret = settings.FLICKR_AUTH_TOKEN_SECRET
    user_id = settings.FLICKR_USER_ID
    username = settings.FLICKR_USERNAME
    url = settings.FLICKR_URL

    def __init__(self):
        self.api = flickrapi.FlickrAPI(self.api_key, self.api_secret, cache=True)
        self.api.cache = flickrapi.SimpleCache(timeout=300, max_entries=200)

    def get_collections(self):
        sets = self.api.photosets.getList(user_id=self.user_id)
        for set in sets.find('collections'):
            yield set

    def get_photoset(self, photoset_id):
        sets = self.api.photosets.getInfo(photoset_id=photoset_id)
        return sets.find('photoset')

    def get_photosets(self, photoset_id=None):
        if photoset_id:
            yield self.get_photoset(photoset_id)
        else:
            sets = self.api.photosets.getList(user_id=self.user_id)
            for set in sets.find('photosets'):
                yield set

    def get_photos_from_photoset(self, slug):
        for photo in self.api.walk_set(slug):
            yield photo

    def get_photo(self, photo_id):
        result = self.api.photos.getInfo(photo_id=photo_id)
        image = result.find('photo')
        dates = image.find('dates')
        created_date = date.datetime.fromtimestamp(int(dates.attrib['posted']), tz=pytz.utc)
        modified_date = date.datetime.fromtimestamp(int(dates.attrib['lastupdate']), tz=pytz.utc)
        taken_date = date.datetime.strptime(dates.attrib['taken'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        photo = {
            'photo_id': photo_id,
            'title': image.find('title').text or photo_id,
            'description': image.find('description').text,
            'taken': taken_date,
            'created_date': created_date,
            'modified_date': modified_date,
            'type': image.attrib['originalformat'],
            'farm': image.attrib['farm'],
            'server': image.attrib['server'],
            'full_path': image.find(".//url[@type='photopage']").text,
        }
        return photo

    def get_photo_size(self, photo_id, label='Original'):
        result = self.api.photos.getSizes(photo_id=photo_id)
        query = ".//sizes/size[@label='{0}']".format(label)
        size = {
            'photo_id': photo_id,
            'width': result.find(query).attrib['width'],
            'height': result.find(query).attrib['height'],
            'source': result.find(query).attrib['source'],
            'url': result.find(query).attrib['url'],
        }
        return size

    def get_photo_url(self, slug):
        return url(slug)

    def set_photo_info(self, photo):
        result = self.api.photos.setMeta(photo_id=photo.slug, title=photo.title, description=photo.description)
        return result

    def create_photoset(self, photoset):
        params = {
            'title': photoset.title,
            'description': photoset.description,
            'primary_photo_id': photoset.primary
        }
        result = self.api.photosets.create(**params)
        photoset = result.find('photoset')
        set = {
            'photoset_id': int(photoset.attrib['id']),
            'url': photoset.attrib['url'],
        }
        return set

    def add_photo_to_photoset(self, photo, photoset):
        params = {'photo_id': photo.slug, 'photoset_id': photoset.slug}
        return self.api.photosets.addPhoto(**params)

    def upload_photo(self, photo, is_public=0):
        params = {
            'filename': photo.full_path,
            'title': photo.title,
            'description': photo.title,
            'is_public': is_public,
            'is_family': 1,
            'is_friend': 1
        }
        result = self.api.upload(**params)
        photoid = result.find('photoid').text
        return int(photoid)
