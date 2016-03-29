import datetime as date

from django.db import models

from mixins.models import ModifiedDate
from photosync.flickr import Flickr

# Create your models here.
class Collection(ModifiedDate):

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    total = models.PositiveIntegerField(blank=False, default=0)
    page = models.CharField(max_length=100)
    description = models.TextField(max_length=65000, blank=True, null=True)

    def __unicode__(self):
        return self.title


class PhotoSet(ModifiedDate):

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    full_path = models.CharField(max_length=1000)
#     local_path = models.CharField(max_length=1000)
    total = models.PositiveIntegerField(blank=False, default=0)
    farm = models.PositiveIntegerField(blank=False, default=0)
    server = models.PositiveIntegerField(blank=False, default=0)
    primary = models.PositiveIntegerField(blank=False, default=0)
    description = models.TextField(max_length=65000, blank=True, null=True)
    collection = models.ForeignKey(Collection, blank=True, null=True, related_name='photosets')

    def __unicode__(self):
        return '{0} [{1}]'.format(self.title, self.slug)

    def save(self, *args, **kwargs):
        if self.slug:
            Flickr().set_photoset_info(self)
        return super(PhotoSet, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Flickr().delete_photoset(self)
        for photo in self.photos.all():
            photo.delete(delete_set=True)
        return super(PhotoSet, self).delete(*args, **kwargs)


class Photo(ModifiedDate):

    IMAGE_TYPES = (
        (0, 'JPG'),
        (1, 'GIF'),
        (2, 'PNG'),
        (3, 'TIFF'),
    )

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    file_name = models.CharField(max_length=500)
    full_path = models.CharField(max_length=1000)
    width = models.PositiveIntegerField(blank=False, default=0)
    height = models.PositiveIntegerField(blank=False, default=0)
    type = models.PositiveIntegerField(blank=False, default=0, choices=IMAGE_TYPES)
    farm = models.PositiveIntegerField(blank=False, default=0)
    server = models.PositiveIntegerField(blank=False, default=0)
    description = models.TextField(max_length=65000, blank=True, null=True)
    photoset = models.ForeignKey(PhotoSet, related_name='photos')

    def __unicode__(self):
        return self.title

    @property
    def size(self):
        return '{0}x{1}'.format(self.width, self.height)

    @property
    def server_info(self):
        return '{0}-{1}'.format(self.farm, self.server)

    def save(self, *args, **kwargs):
        if self.slug:
            Flickr().set_photo_info(self)
        return super(Photo, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Flickr().delete_photo(self)
        if kwargs.get('delete_set', False) is False:
            self.photoset.total = self.photoset.total - 1
            self.photoset.save()
        else:
            del kwargs['delete_set']
        return super(Photo, self).delete(*args, **kwargs)

    def get_photo_size(self, label="Original"):
        data = Flickr().get_photo_size(self.slug, label)
        return data

    def get_type(self, type):
        d = dict(self.IMAGE_TYPES)
        for index, imagetype in d.iteritems():
            if imagetype == type:
                return index
        return None

    def set_permissions(self, is_public=0, is_friend=1, is_family=1):
        if self.slug:
            try:
                res = Flickr().set_permissions(self, is_public=is_public, is_friend=is_friend, is_family=is_family)
            except Exception, e:
                pass


class CopySettings(models.Model):

    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    full_path = models.CharField(max_length=1000)
    last_photo = models.PositiveIntegerField(blank=False, default=0)
    last_moive = models.PositiveIntegerField(blank=False, default=0)
    photo_name_format = models.CharField(max_length=100)
    movie_name_format = models.CharField(max_length=100)
    counter = models.PositiveIntegerField(blank=False, default=0)

    def __unicode__(self):
        return self.name

