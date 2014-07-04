import os
import sys
import pytz
import shutil
import re as regex
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection, CopySettings
from flickrphotosync.photosync.flickr import Flickr

class Command(BaseCommand):
    args = '<slug slug ...>'
    help = 'Copy photos from an SD Card to a local photo directory'
    user = User.objects.get(pk=1)
    slug = None
    card = None
    type = None
    number = None
    settings = None
    directory = settings.PHOTO_DOWNLOAD_DIR

    option_list = BaseCommand.option_list + (
        make_option('--slug', action='store', dest='slug', default=False, help='Short Name of SD Card'),
        make_option('--directory', action='store', dest='directory', default=False, help='Copy to this directory'),
    )

    def handle(self, *args, **options):

        for key in ['slug', 'directory']:
            option = options.get(key, None)
            if option:
                setattr(self, key, option)

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
        for dirname, dirnames, filenames in os.walk(card):
            for filename in filenames:
                for name in ['.DS_Store', '.localized', '.THM']:
                    if name in filename:
                        filenames.remove(filename)
            for dirname in dirnames:
                for name in ['MISC', 'CANONMSC']:
                    if name in dirname:
                        dirnames.remove(dirname)

            for filename in filenames:
                match = regex.search(r'(?P<type>IMG|MVI)_(?P<number>\d+)[.][JPG|MOV|AVI]', filename)
                if match:
                    current_number, to_filename = self.update_settings(match);

                    if self.number > current_number:
                        from_filename = os.path.join(dirname, filename)
                        to_filename = os.path.join(directory, to_filename.format(self.settings.counter, self.number))
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
