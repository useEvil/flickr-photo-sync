import os
import sys
import pytz
import urllib
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection
from flickrphotosync.photosync.flickr import Flickr

class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Upload photos from a local photo directory'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
        make_option('--dry', action='store_true', dest='dry', default=False, help='Only do a dry run'),
        make_option('--public', action='store_true', dest='public', default=False, help='Set privacy to public'),
        make_option('--directory', action='store', dest='directory', default=False, help='Match this directory'),
    )

    def handle(self, *args, **options):

        for key in ['all', 'dry', 'public', 'directory']:
            option = options.get(key, None)
            if option:
                setattr(self, key, option)

        elif options.get('all'):
            photosets = PhotoSet.objects.all()
            for photoset in photosets:
                self.get_photoset(photoset)
                self.stdout.write('Successfully Downloaded Photos in PhotoSet "{0}"'.format(photoset))
        else:
            for photoset in args:
                try:
                    set = PhotoSet.objects.get(slug=photoset)
                    self.get_photoset(set)
                    self.stdout.write('Successfully Downloaded Photos in PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def get_photoset(self, photoset):
        self.stdout.write('==== Processing PhotoSet [{0}][{1}]'.format(photoset.title, photoset.slug))
        set in self.flickr.get_photoset(photoset.slug):
        if photoset.total < set.attrib['photos']:
            for photo in photoset.photos:
                size = self.flickr.get_photo_size(photo.slug):
                urllib.urlretrieve(size.get('source'), photo.file_name)

