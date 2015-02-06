from import_export import resources

from mixins.models import ModifiedDate
from photosync.models import PhotoSet, Photo, CopySettings


class PhotoSetResource(resources.ModelResource):

    class Meta:
        model = PhotoSet


class PhotoResource(resources.ModelResource):

    class Meta:
        model = Photo


class CopySettingsResource(resources.ModelResource):

    class Meta:
        model = CopySettings
