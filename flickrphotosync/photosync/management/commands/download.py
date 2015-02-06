import os, errno, sys, pytz, urllib
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from photosync.models import Photo, PhotoSet, Collection
from photosync.flickr import Flickr
from photosync.helpers import *


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Downloads photos from a photoset on Flickr'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
        make_option('--dry', action='store_true', dest='dry', default=False, help='Only do a dry run'),
        make_option('--backup', action='store_true', dest='backup', default=False, help='Set backup flag to True'),
        make_option('--directory', action='store', dest='directory', default=False, help='Match this directory'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['all', 'dry', 'backup', 'directory'])

        if options.get('all'):
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
        set = self.flickr.get_photoset(photoset.slug)
        if photoset.total < set.attrib['photos'] or self.backup:
            download_path = settings.PHOTO_DOWNLOAD_DIR.format(self.user.username)
            download_dir = os.path.join(download_path, photoset.title)
            self.make_directory(download_dir)
            for photo in photoset.photos.all():
                self.stdout.write('==== Downloading Photo [{0}]'.format(photo.file_name))
                if not self.dry and not os.path.isfile(photo.file_name):
                    size = self.flickr.get_photo_size(photo.slug)
                    photo_path = os.path.join(download_dir, photo.file_name)
                    print '==== photo_path [{0}]'.format(photo_path)
                    urllib.urlretrieve(size.get('source'), photo_path)

    def make_directory(self, path):
        try:
            os.makedirs(path)
            self.stdout.write('==== Creating Directory [{0}]'.format(path))
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                self.stdout.write('==== Directory already exists [{0}]'.format(path))
                pass
            else:
                raise CommandError('Processing Error "{0}"'.format(exc))
