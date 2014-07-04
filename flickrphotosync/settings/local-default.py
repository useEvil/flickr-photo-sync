import base64

FLICKR_API_KEY = u''
FLICKR_SECRET_KEY = u''
FLICKR_AUTH_TOKEN = u''
FLICKR_AUTH_TOKEN_SECRET = u''
FLICKR_URL = 'https://www.flickr.com/photos/'
FLICKR_USER_ID = ''
FLICKR_USERNAME = ''
FLICKR_FILENAME = 'tokens/{0}.token'
FLICKR_THUMBNAILS = 'media/thumbnails'

INSTAGRAM_CLIENT_ID = u''
INSTAGRAM_CLIENT_SECRET = u''
INSTAGRAM_ACCESS_TOKEN = u''
INSTAGRAM_GET_USER = ''
INSTAGRAM_WEEKS = 52

PHOTO_DIR = '/Volumes/{0}/Pictures'
PHOTO_DOWNLOAD_DIR = '/Volumes/{0}/Downloads/Images'
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
