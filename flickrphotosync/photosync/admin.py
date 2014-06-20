from django.contrib import admin

from models import Photo, PhotoSet, Collection
from forms import PhotoSetForm

# Register your models here.
class PhotoAdmin(admin.ModelAdmin):

    # create a link for the photo on flickr
    def full_path_link(obj):
        return '<a href="{0}" class="nowrap" style="font-weight: bold;font-size: 12px;" target="_photo">{1}</a>'.format(obj.full_path, obj.full_path)
    full_path_link.allow_tags = True
    full_path_link.short_description = "Full Path"

    def size_info(obj):
        return '{0}x{1}'.format(obj.width, obj.height)
    size_info.allow_tags = True
    size_info.short_description = "Size"

    def server_info(obj):
        return '{0}-{1}'.format(obj.farm, obj.server)
    server_info.allow_tags = True
    server_info.short_description = "Farm-Server"

    list_display = ['title', 'photoset', 'slug', size_info, server_info, full_path_link, 'created_date']
    search_fields = ['title', 'photoset__title', 'photoset__description', 'file_name', 'slug']

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    verbose_name_plural = 'photos'
    fields = ('title', 'slug', 'file_name', 'width', 'height', 'type')

class PhotoSetAdmin(admin.ModelAdmin):

    # create a link for the student name
    def full_path_link(obj):
        return '<a href="%s" class="nowrap" style="font-weight: bold;font-size: 12px;" target="_photo">%s</a>' % (obj.full_path, obj.slug)
    full_path_link.allow_tags = True
    full_path_link.short_description = "Slug"

    list_display = ['title', 'total', full_path_link, 'created_date']
    search_fields = ['title', 'description', 'slug']
    inlines = [PhotoInline]

class PhotoSetInline(admin.TabularInline):
    model = PhotoSet
    extra = 6
    verbose_name_plural = 'photosets'

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_date']
    search_fields = ['title', 'description', 'slug']
    inlines = [PhotoSetInline]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoSet, PhotoSetAdmin)
admin.site.register(Collection, CollectionAdmin)
