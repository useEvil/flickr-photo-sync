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
    help = 'Upload photos from a local photo directory'
    flickr = Flickr()
    user = User.objects.get(pk=1)

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
        make_option('--public', action='store_true', dest='public', default=False, help='Set privacy to public'),
    )

    def handle(self, *args, **options):

        if options.get('all'):
            photo_dir = settings.PHOTO_DIR.format(self.user.username)
            self.get_directory_listing(photo_dir)
        else:
            for photoset in args:
                try:
                    self.get_directory_listing(photoset)
                    self.stdout.write('Successfully Uploaded PhotoSet "{0}"'.format(photoset))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def get_directory_listing(self, directory):
        for dirname, dirnames, filenames in os.walk(directory):
            for name in ['.DS_Store', '.localized', 'iPhoto Library', 'Aperture Library']:
                if name in filenames:
                    filenames.remove(name)
            for name in ['iChat Icons', 'iPhoto Library', 'Aperture Library.aplibrary']:
                if name in dirnames:
                    dirnames.remove(name)

            total = len(filenames)
            if total:
                photoset, set_created = self.get_photoset(dirname)
                primary = None
                if photoset.total != total or set_created:
                    for filename in filenames:
                        ext = os.path.splitext(filename)[1][1:]
                        ext_type = Photo().get_type(ext.upper())
                        if type(ext_type) is int:
                            photo, img_created = self.save_photo(photoset, dirname, filename)
                            if not primary and set_created:
                                primary = photo
                                photoset.primary = primary.slug
                                set = self.flickr.create_photoset(photoset)
                                photoset.slug = set.get('photoset_id')
                                photoset.full_path = set.get('url')
                            else:
                                self.flickr.add_photo_to_photoset(photo, photoset)
                            photoset.total = photoset.total + 1
                            photoset.save()

    def get_photoset(self, dirname):
        dir = os.path.basename(dirname)
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
            print '==== Creating Photoset [{0}]'.format(dirname)
            photoset.created_date = created_date
            photoset.modified_date = modified_date
            photoset.save()
        return photoset, created

    def save_photo(self, photoset, dirname, filename):
        full_path = os.path.join(dirname, filename)
        created_date = date.datetime.fromtimestamp(os.path.getctime(full_path), tz=pytz.utc)
        modified_date = date.datetime.fromtimestamp(os.path.getmtime(full_path), tz=pytz.utc)
        title = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1][1:]
        type = Photo().get_type(ext.upper())
        width, height = self.create_thumbnail(dirname, filename)
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
        if created or not photo.slug:
            print '==== Uploading Photo [{0}]'.format(filename)
            photo_id = self.flickr.upload_photo(photo, 1)
            img = self.flickr.get_photo(photo_id)
            photo.full_path = img.get('url')
            photo.created_date = img.get('taken')
            photo.modified_date = modified_date
            photo.slug = photo_id
            photo.save()
        return photo, created

    def create_thumbnail(self, dirname, filename, create=False):
        full_path = os.path.join(dirname, filename)
        print '==== Creating Thumbnail [{0}]'.format(full_path)
        image = Image.open(full_path)
        if create:
            image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
        return image.size
