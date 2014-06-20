import os
import pytz
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection
from flickrphotosync.photosync.flickr import Flickr

class Command(BaseCommand):
    args = '<photodir photodir ...>'
    help = 'Rename photos from a local photo directory'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--prefix', action='store', dest='prefix', default=False, help='Prefix to add to file name'),
    )

    def handle(self, *args, **options):

        self.prefix = options.get('prefix')
        for photoset in args:
            try:
                self.get_photoset(int(photoset))
                self.stdout.write('Successfully Updated PhotoSet "{0}"'.format(photoset))
            except PhotoSet.DoesNotExist:
                raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def get_photoset(self, photoset_id):
        photoset = PhotoSet.objects.get(slug=photoset_id)
        print '==== Processing PhotoSet [{0}]'.format(photoset.title)
        for photo in photoset.photos.all():
            print '==== Renaming Photo [{0}]'.format(photo.title)
            size = self.flickr.get_photo_size(photo.slug, 'Original')
            photo.title = '{0}_{1}'.format(self.prefix, photo.title)
            photo.file_name = '{0}_{1}'.format(self.prefix, photo.file_name)
            photo.description = '{0}: {1}'.format(photoset.title, photo.title)
            photo.width = size.get('width', photo.width)
            photo.height = size.get('height', photo.height)
            photo.save()
            self.flickr.set_photo_info(photo)
