import pytz
import datetime as date

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from flickrphotosync.photosync.models import Photo, PhotoSet, Collection
from flickrphotosync.photosync.flickr import Flickr

class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Imports photos from a photoset on Flickr'
    user = User.objects.get(pk=1)
    flickr = Flickr()

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, help='Retrieve all photosets'),
    )

    def handle(self, *args, **options):

        if options.get('all'):
            self.import_flickr_photosets()
        else:
            for photoset_id in args:
                try:
                    self.import_flickr_photosets(int(photoset_id))
                except PhotoSet.DoesNotExist:
                    raise CommandError('PhotoSet "{0}" does not exist'.format(photoset))

    def import_flickr_photosets(self, photoset_id=None):
        for photoset in self.flickr.get_photosets(photoset_id):
            set, set_created = self.save_photoset(photoset)
            if set.total != photoset.attrib['photos'] or set_created:
                for photo in self.flickr.get_photos_from_photoset(set.slug):
                    img, img_created = self.save_photo(set, photo)
                    if img_created:
                        set.total = set.total + 1
                        set.save()
            self.stdout.write('Successfully imported PhotoSet "{0}"'.format(photoset.find('title').text))

    def save_photoset(self, photoset):
        url = self.flickr.url + self.flickr.username.format(self.user.username)
        created_date = date.datetime.fromtimestamp(int(photoset.attrib['date_create']), tz=pytz.utc)
        modified_date = date.datetime.fromtimestamp(int(photoset.attrib['date_update']), tz=pytz.utc)
        set, created = PhotoSet.objects.get_or_create(
                            title=photoset.find('title').text,
                            slug=photoset.attrib['id'],
                            defaults={
                                'created_by': self.user,
                                'created_date': created_date,
                                'modified_by': self.user,
                                'modified_date': modified_date,
                                'farm': photoset.attrib['server'],
                                'primary': photoset.attrib['primary'],
                                'description': photoset.find('description').text,
                                'full_path': '{0}/sets/{1}'.format(url, photoset.attrib['id'])
                            }
                        )
        if created:
            print '==== Creating Photoset [{0}][{1}]'.format(set.title, set.slug)
            set.created_date = created_date
            set.modified_date = modified_date
            set.save()
        return set, created

    def save_photo(self, photoset, photo):
        photo = self.flickr.get_photo(photo.get('id'))
        title = photo.get('title', photo.get('photo_id'))
        ext = photo.get('type')
        type = Photo().get_type(ext.upper())
        img, created = Photo.objects.get_or_create(
                            title=title,
                            slug=photo.get('photo_id'),
                            photoset=photoset,
                            defaults={
                                'created_by': self.user,
                                'created_date': photo.get('taken'),
                                'modified_by': self.user,
                                'modified_date': date.datetime.now(pytz.utc),
                                'description': "{0}: {1}".format(photo.get('description', photoset.title), title),
                                'farm': photo.get('farm'),
                                'server': photo.get('server'),
                                'full_path': photo.get('full_path'),
                                'file_name': '{0}.{1}'.format(title, ext),
                                'type': type
                            }
                        )
        if created:
            print '==== Importing Photo [{0}][{1}]'.format(img.title, img.full_path)
            img.created_date = photo.get('taken')
            img.save()
        return img, created
