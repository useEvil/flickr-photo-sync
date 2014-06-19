import os

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from flickrphotosync.photosync.flickr import Flickr


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Imports photos froma photoset on Flickr'
    flickr = Flickr()

    option_list = BaseCommand.option_list + (
        make_option('--flickrapi', action='store_true', dest='flickrapi', default=False, help='Use FlickrAPI'),
        make_option('--flickr_api', action='store_true', dest='flickr_api', default=False, help='Use Flickr_API'),
        make_option('--verify', action='store_true', dest='verify', default=False, help='Verify FlickrAPI OAuth Tokens'),
        make_option('--oauth_token', action='store', dest='oauth_token', default=False, help='FlickrAPI OAuth Token'),
        make_option('--oauth_verifier', action='store', dest='oauth_verifier', default=False, help='FlickrAPI OAuth Verifier'),
    )

    def handle(self, *args, **options):
        if options['verify']:
            auth_props = self.flickr.api.get_auth_tokens(options['oauth_verifier'])
            print '==== auth_props [{0}]'.format(auth_props)
        else:
            auth_props = self.flickr.api.get_authentication_tokens("write")
            auth_url = auth_props['auth_url']

            # Store this token in a session or something for later use in the next step.
            oauth_token = auth_props['oauth_token']
            oauth_token_secret = auth_props['oauth_token_secret']
            print '==== oauth_token [{0}]'.format(oauth_token)
            print '==== oauth_token_secret [{0}]'.format(oauth_token_secret)
            print 'Connect with Flickr via: {0}'.format(auth_url)
