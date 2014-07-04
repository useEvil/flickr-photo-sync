from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Photo, PhotoSet, Collection, CopySettings
from forms import PhotoSetForm
from actions import delete_selected_from_flickr

# Register your models here.
class PhotoSetListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('PhotoSet')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = ''

    def lookups(self, request, model_admin):
        return (
            ('no_size_info', _('Missing Size Info')),
            ('no_server_info', _('Missing Server Info')),
            ('no_farm_info', _('Missing Farm Info')),
        )
    def queryset(self, request, queryset):
        query = request.GET.get('q') or ''
        if self.value() == 'no_size_info':
            results = Photo.objects.filter(width=0, height=0).values_list('photoset__slug', flat=True).distinct()
            return queryset.filter(slug__in=results).all()
        elif self.value() == 'no_server_info':
            results = Photo.objects.filter(server=0).values_list('photoset__slug', flat=True).distinct()
            return queryset.filter(slug__in=results).all()
        elif self.value() == 'no_farm_info':
            results = Photo.objects.filter(farm=0).values_list('photoset__slug', flat=True).distinct()
            return queryset.filter(slug__in=results).all()
        else:
            return queryset.all()


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
    search_fields = ['title', 'photoset__title', 'photoset__description', 'photoset__slug', 'file_name', 'slug']
    actions = [delete_selected_from_flickr]
    save_on_top = True


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

    list_display = ['id', 'title', 'total', full_path_link, 'created_date']
    list_editable = ['title']
    list_filter = [PhotoSetListFilter]
    search_fields = ['title', 'description', 'slug']
    actions = [delete_selected_from_flickr]
    inlines = [PhotoInline]
    save_on_top = True


class PhotoSetInline(admin.TabularInline):

    model = PhotoSet
    extra = 6
    verbose_name_plural = 'photosets'


class CollectionAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug', 'created_date']
    search_fields = ['title', 'description', 'slug']
    inlines = [PhotoSetInline]
    save_on_top = True

class CopySettingsAdmin(admin.ModelAdmin):

    list_display = ['name', 'last_photo', 'last_moive', 'counter']
    save_on_top = True


admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoSet, PhotoSetAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CopySettings, CopySettingsAdmin)
