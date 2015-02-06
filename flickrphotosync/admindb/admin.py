from django.contrib import admin

from models import DbMaintenance


def _linkify(instance, link_name=None):
    if not link_name:
        link_name = instance.name
    return '<a href="{0}">{1}</a>'.format(instance.url, link_name)


class DbMaintenanceAdmin(admin.ModelAdmin):

    def exported_link(instance):
        return _linkify(instance.exported_file)
    exported_link.allow_tags = True


    list_display = ('id',exported_link,'imported_file',)
#     list_display_links = ('exported_file','imported_file',)
#     list_filter = ('',)
#     list_editable = ('tracking_number',)
    exclude = ('created_by','created_date','modified_by','modified_date','exported_file',)
    search_fields = ('exported_file','imported_file',)
    save_on_top = True


admin.site.register(DbMaintenance, DbMaintenanceAdmin)
