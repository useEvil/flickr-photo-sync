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
    help = 'Update photo meta info on Flickr and in database'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Update All Photos'),
        make_option('--size', action='store_true', dest='size', default=False, help='Update size info'),
        make_option('--meta', action='store_true', dest='meta', default=False, help='Update meta info'),
        make_option('--server', action='store_true', dest='server', default=False, help='Update meta info'),
        make_option('--empty', action='store_true', dest='empty', default=False, help='Update Photos with no size info'),
    )

    def handle(self, *args, **options):

        for key in ['size', 'meta', 'server', 'empty']:
            setattr(self, key, options.get(key))

        if options.get('empty'):
            photosets = Photo.objects.filter(width=0, height=0).values_list('photoset__slug', flat=True).distinct()
            for photoset in photosets:
                try:
                    self.get_photoset(photoset)
                    self.stdout.write('Successfully Updated PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))
        elif options.get('all'):
            photosets = PhotoSet.objects.all()
            for photoset in photosets:
                self.update_photos(photoset)
                self.stdout.write('Successfully Updated PhotoSet "{0}"'.format(photoset))
        else:
            for photoset in args:
                try:
                    self.get_photoset(photoset)
                    self.stdout.write('Successfully Updated PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def get_photoset(self, photoset_id):
        photoset = PhotoSet.objects.get(slug=photoset_id)
        print '==== Processing PhotoSet [{0}][{1}]'.format(photoset.title, photoset.slug)
        self.update_photos(photoset)

    def update_photos(self, photoset):
        for photo in photoset.photos.all():
            if self.server:
                server = self.flickr.get_photo(photo.slug)
                photo.farm = server.get('farm', photo.farm)
                photo.server = server.get('server', photo.server)
                photo.save()
                print '==== Updating Photo Server [{0}][{1}]'.format(photo.title, photo.server_info)
            if self.size:
                size = self.flickr.get_photo_size(photo.slug, 'Original')
                photo.width = size.get('width', photo.width)
                photo.height = size.get('height', photo.height)
                photo.save()
                print '==== Updating Photo Size [{0}][{1}]'.format(photo.title, photo.size)
            if self.meta:
                self.flickr.set_photo_info(photo)
                print '==== Updating Photo Meta [{0}]'.format(photo.title)
