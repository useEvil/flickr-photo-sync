import os, errno, sys, pytz
import datetime as date

from PIL import Image
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection
from flickrphotosync.photosync.flickr import Flickr
from flickrphotosync.photosync.helpers import *


class Command(BaseCommand):
    args = '<photodir photodir ...>'
    help = 'Upload photos from a local photo directory'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
        make_option('--dry', action='store_true', dest='dry', default=False, help='Only do a dry run'),
        make_option('--public', action='store_true', dest='public', default=0, help='Set privacy to public'),
        make_option('--validated', action='store_true', dest='validated', default=0, help='Validate photoset'),
        make_option('--replace', action='store_true', dest='replace', default=0, help='Replace photoset list with local file list'),
        make_option('--directory', action='store', dest='directory', default=False, help='Match this directory'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['all', 'dry', 'public', 'directory', 'validated', 'replace'])

        if self.all:
            photo_dir = settings.PHOTO_DIR.format(self.user.username)
            self.get_directory_listing(photo_dir)
        elif self.replace:
            for slug in args:
                try:
                    photoset = PhotoSet.objects.get(slug=slug)
                    self.stdout.write('==== Processing PhotoSet [{0}]'.format(photoset))
                    self.flickr.set_photoset_list(photoset)
                    self.stdout.write('Successfully Replaced PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(slug))
        elif self.validated:
            for slug in args:
                try:
                    photoset = PhotoSet.objects.get(slug=slug)
                    self.stdout.write('==== Processing PhotoSet [{0}]'.format(photoset))
                    for photo in photoset.photos.all():
                        img = self.flickr.get_photo(photo.slug)
                        try:
                            self.flickr.add_photo_to_photoset(photo, photoset)
                            self.stdout.write('==== Adding Photo to PhotoSet [{0}][{1}][{2}]'.format(photo, photoset.title, photoset.slug))
                        except Exception, e:
                            context = self.flickr.get_photo_context(photo)
                            self.stdout.write('==== Photo already in PhotoSet [{0}][{1}][{2}]'.format(photo, context.get('title'), context.get('photoset_id')))
                    self.stdout.write('Successfully Validated PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(slug))
        elif self.directory:
            try:
                self.get_directory_listing(self.directory)
                return
            except:
                pass
        else:
            for directory in args:
                try:
                    self.get_directory_listing(directory)
                    self.stdout.write('Successfully Uploaded PhotoSet Directory "{0}"'.format(directory))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet Directory "{0}" does not exist'.format(directory))

    def get_directory_listing(self, directory):
        for dirname, dirnames, filenames in os.walk(directory):
            skip_files_and_directories(dirnames, filenames)

            self.total = len(filenames)
            if self.total:
                photoset, set_created = self.get_photoset(dirname)
                if not self.dry:
                    primary = None
                    if photoset.total < self.total or set_created:
                        self.stdout.write('==== photoset [{0}][{1}][{2}]'.format(photoset, photoset.total, self.total))
                        for filename in filenames:
                            ext = os.path.splitext(filename)[1][1:]
                            ext_type = Photo().get_type(ext.upper())
                            if type(ext_type) is int:
                                photo, img_created, img_uploaded = self.save_photo(photoset, dirname, filename, set_created)
                                if not primary and set_created:
                                    try:
                                        primary = photo
                                        photoset.primary = primary.slug
                                        set = self.flickr.create_photoset(photoset)
                                        photoset.slug = set.get('photoset_id')
                                        photoset.full_path = set.get('url')
                                        photoset.total = photoset.total + 1
                                    except Exception, e:
                                        self.stdout.write('==== Failed to create PhotoSet [{0}]'.format(photoset))
                                elif img_created or img_uploaded or self.validated:
                                    try:
                                        self.flickr.add_photo_to_photoset(photo, photoset)
                                        photoset.total = photoset.total + 1
                                    except Exception, e:
                                        self.stdout.write('==== Failed to add Photo to PhotoSet [{0}][{1}]'.format(photo, photoset))
                                        self.stdout.write('==== Error [{0}]'.format(e))
                                else:
                                    pass
                                photoset.save()

    def get_photoset(self, dirname):
        dir = os.path.basename(dirname)
        if self.dry:
            try:
                photoset = PhotoSet.objects.get(title=dir)
            except:
                self.stdout.write('==== Photoset not found in database [{0}][{1}]'.format(dir, self.total))
            return None, None
        created_date = date.datetime.fromtimestamp(os.path.getctime(dirname), tz=pytz.utc)
        modified_date = date.datetime.fromtimestamp(os.path.getmtime(dirname), tz=pytz.utc)
        photoset, created = PhotoSet.objects.get_or_create(
                            title=dir,
                            defaults={
                                'created_by': self.user,
                                'created_date': created_date,
                                'modified_by': self.user,
                                'modified_date': modified_date,
                                'description': dir,
                            }
                        )
        if created:
            self.stdout.write('==== Creating Photoset [{0}][{1}]'.format(dirname, self.total))
            photoset.created_date = created_date
            photoset.modified_date = modified_date
            photoset.save()
        return photoset, created

    def save_photo(self, photoset, dirname, filename, set_created):
        full_path = os.path.join(dirname, filename)
        created_date = date.datetime.fromtimestamp(os.path.getctime(full_path), tz=pytz.utc)
        modified_date = date.datetime.fromtimestamp(os.path.getmtime(full_path), tz=pytz.utc)
        title = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1][1:]
        type = Photo().get_type(ext.upper())
        width, height = self.create_thumbnail(dirname, filename)
        uploaded = False
        created = False
        if set_created:
            photo = Photo.objects.create(
                        file_name=filename,
                        created_by=self.user,
                        created_date=created_date,
                        modified_by=self.user,
                        modified_date=modified_date,
                        title=title,
                        description="{0}: {1}".format(photoset.title, title),
                        type=type,
                        full_path=full_path,
                        width=width,
                        height=height,
                        photoset=photoset,
                    )
            created = True
        else:
            try:
                photo, created = Photo.objects.get_or_create(
                                file_name=filename,
                                defaults={
                                    'created_by': self.user,
                                    'created_date': created_date,
                                    'modified_by': self.user,
                                    'modified_date': modified_date,
                                    'title': title,
                                    'description': "{0}: {1}".format(photoset.title, title),
                                    'type': type,
                                    'full_path': full_path,
                                    'width': width,
                                    'height': height,
                                    'photoset': photoset,
                                }
                            )
            except Exception, e:
                self.stdout.write('==== Exception [{0}]'.format(e))
                self.stdout.write('==== filename [{0}]'.format(filename))
                return None, False, False
        # if photo is new or does not have a photo_id (slug) then upload it
        if created or not photo.slug:
            self.stdout.write('==== Uploading Photo [{0}]'.format(filename))
            try:
                photo_id = self.flickr.upload_photo(photo, self.public)
                uploaded = True
            except Exception, e:
                self.stdout.write('==== Failed to Upload Photo [{0}]'.format(filename))
                return None, False, False
            img = self.flickr.get_photo(photo_id)
            photo.full_path = img.get('full_path')
            photo.created_date = img.get('taken')
            photo.modified_date = modified_date
            photo.farm = img.get('farm')
            photo.server = img.get('server')
            photo.slug = photo_id
            photo.save()
        return photo, created, uploaded

    def create_thumbnail(self, dirname, filename, create=False):
        full_path = os.path.join(dirname, filename)
        image = Image.open(full_path)
        if create:
            self.stdout.write('==== Creating Thumbnail [{0}]'.format(filename))
            image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
        return image.size
