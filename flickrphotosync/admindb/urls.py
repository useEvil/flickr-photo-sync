from django.conf.urls import patterns, include, url

# Orders urls

urlpatterns = patterns(
    'admindb.views',
    url(r'^upload/', 'file_upload', name='file_upload')
)
