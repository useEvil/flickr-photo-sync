import os, errno, sys, pytz, urllib, shutil
import datetime as date

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.instagramapi import Instagram
from flickrphotosync.photosync.helpers import *


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Upload photos from a local photo directory'
    instagram = Instagram()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
        make_option('--weeks', action='store', dest='weeks', default=False, help='Number of weeks to go back'),
        make_option('--pages', action='store', dest='pages', default=5, help='Number of pages'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['all', 'weeks', 'pages'])

        if options.get('weeks'):
            self.instagram.weeks = options.get('weeks')

        if options.get('all'):
            self.get_collection()
            self.stdout.write('Successfully Downloaded Photos')
        else:
            for user_id in args:
                self.get_collection(user_id)
            self.stdout.write('Successfully Downloaded Photos for User "{0}"'.format(user_id))

    def get_collection(self, user_id=None):
        counter = 1
        media, next = self.instagram.get_collection(user_id)
        for photo in media:
            self.get_photo(photo)
        while next and counter < self.pages:
            media, next = self.instagram.get_next_with_url(next, user_id)
            for photo in media:
                self.get_photo(photo)
            counter += 1

    def get_photo(self, photo):
        url = photo.get_standard_resolution_url()
        filename = os.path.basename(url)
        location = '{0}/{1}'.format(settings.PHOTO_DOWNLOAD_DIR, filename)
        location = location.format(self.user.username)
        if not os.path.isfile(location):
            print '==== Downloading Photo [{0}]'.format(url)
            urllib.urlretrieve(url, location)
