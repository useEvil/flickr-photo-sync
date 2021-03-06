import os, errno, sys, pytz
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from photosync.models import Photo, PhotoSet, Collection
from photosync.flickr import Flickr
from photosync.helpers import *


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Rename photos from a local photo directory'
    flickr = Flickr()

    option_list = BaseCommand.option_list + (
        make_option('--prefix', action='store', dest='prefix', default=False, help='Prefix to add to file name'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['prefix'])

        for photoset in args:
            try:
                self.get_photoset(int(photoset))
                self.stdout.write('Successfully Updated PhotoSet "{0}"'.format(photoset))
            except PhotoSet.DoesNotExist:
                raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def get_photoset(self, photoset_id):
        photoset = PhotoSet.objects.get(slug=photoset_id)
        self.stdout.write('==== Processing PhotoSet [{0}]'.format(photoset.title))
        for photo in photoset.photos.all():
            self.stdout.write('==== Renaming Photo [{0}]'.format(photo.title))
            size = self.flickr.get_photo_size(photo.slug, 'Original')
            photo.title = '{0}_{1}'.format(self.prefix, photo.title)
            photo.file_name = '{0}_{1}'.format(self.prefix, photo.file_name)
            photo.description = '{0}: {1}'.format(photoset.title, photo.title)
            photo.width = size.get('width', photo.width)
            photo.height = size.get('height', photo.height)
            photo.save()
            self.flickr.set_photo_info(photo)
