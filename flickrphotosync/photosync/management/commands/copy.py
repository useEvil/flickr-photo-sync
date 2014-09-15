import os, errno, sys, pytz, urllib, shutil
import re as regex
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection, CopySettings
from flickrphotosync.photosync.flickr import Flickr
from flickrphotosync.photosync.helpers import *


# dj copy --slug=dslr_64 --directory="Birthday-2014.07.27-Bree Nguyen-The Rinks"


class Command(BaseCommand):
    args = '<slug slug ...>'
    help = 'Copy photos from an SD Card to a local photo directory'
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--slug', action='store', dest='slug', default='dslr_64', help='Short Name of SD Card'),
        make_option('--directory', action='store', dest='directory', default=settings.PHOTO_DOWNLOAD_DIR, help='Copy to this directory'),
        make_option('--folder', action='store', dest='folder', default=False, help='Create Folder'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['slug', 'directory', 'folder'])

        try:
            self.settings = CopySettings.objects.get(slug=self.slug)
            self.set_config()
        except CopySettings.DoesNotExist:
            raise CommandError('Settings for "{0}" does not exist'.format(self.slug))

        try:
            self.get_directory_listing(self.card)
            self.settings.save()
            self.stdout.write('Successfully Copied Photos from Directory "{0}"'.format(self.card))
        except Exception, e:
            raise CommandError('Photo Directory "{0}" does not exist: {1}'.format(self.card, e))

    def get_directory_listing(self, card):
        directory = self.directory.format(self.user.username)
        to_folder = os.path.join(directory, self.folder)
        self.make_directory(to_folder)
        for dirname, dirnames, filenames in os.walk(card):
            skip_files_and_directories(dirnames, filenames)

            for filename in sorted(filenames):
                match = regex.search(r'(?P<type>IMG|MVI)_(?P<number>\d+)[.][JPG|MOV|AVI]', filename)
                if match:
                    current_number, to_filename = self.update_settings(match);

                    if self.number > current_number:
                        from_filename = os.path.join(dirname, filename)
                        to_filename = os.path.join(to_folder, to_filename.format(self.settings.counter, self.number))
                        shutil.copy2(from_filename, to_filename)
                        self.stdout.write('==== Copying Photo [{0}]'.format(to_filename))

    def set_config(self):
        self.card = self.settings.full_path
        self.config = {
            'IMG': {
                'to_filename': self.settings.photo_name_format,
                'current_number': self.settings.last_photo
            },
            'MVI': {
                'to_filename': self.settings.movie_name_format,
                'current_number': self.settings.last_moive
            },
        }

    def update_settings(self, match):
        self.number = int(match.group('number'))
        self.type = match.group('type')
        to_filename = self.config[self.type]['to_filename']
        current_number = self.config[self.type]['current_number']
        if self.type == 'IMG':
            self.settings.last_photo = self.number
        else:
            self.settings.last_moive = self.number
        return current_number, to_filename

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
