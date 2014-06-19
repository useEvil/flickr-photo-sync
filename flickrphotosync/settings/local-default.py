FLICKR_API_KEY = u''
FLICKR_SECRET_KEY = u''
FLICKR_AUTH_TOKEN = u''
FLICKR_AUTH_TOKEN_SECRET = u''
FLICKR_URL = 'https://www.flickr.com/photos/'
FLICKR_USER_ID = ''
FLICKR_USERNAME = ''
FLICKR_FILENAME = 'tokens/{0}.token'
FLICKR_THUMBNAILS = 'media/thumbnails'

PHOTO_DIR = '/Volumes/{0}/Pictures'
PHOTO_THUMB_SIZE = 128, 128

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/flickr-photo-sync-error.log',
        },
    },
    'loggers': {
        'flickrphotosync.photosync': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'flickrapi': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
