from django.contrib import admin

from models import Photo, PhotoSet, Collection
from forms import PhotoSetForm

# Register your models here.
class PhotoAdmin(admin.ModelAdmin):

    # create a link for the student name
    def full_path_link(obj):
        return '<a href="%s" class="nowrap" style="font-weight: bold;font-size: 12px;" target="_photo">%s</a>' % (obj.full_path, obj.full_path)
    full_path_link.allow_tags = True
    full_path_link.short_description = "Full Path"

    list_display = ['title', 'slug', full_path_link, 'created_date']
    search_fields = ['title', 'file_name', 'slug']

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
    search_fields = ['title', 'slug']
    inlines = [PhotoInline]

class PhotoSetInline(admin.TabularInline):
    model = PhotoSet
    extra = 6
    verbose_name_plural = 'photosets'

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_date']
    search_fields = ['title', 'slug']
    inlines = [PhotoSetInline]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoSet, PhotoSetAdmin)
admin.site.register(Collection, CollectionAdmin)
