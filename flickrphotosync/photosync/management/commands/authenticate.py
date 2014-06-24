import os

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from flickrphotosync.photosync.flickr import Flickr


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Imports photos froma photoset on Flickr'
    flickr = Flickr()

    option_list = BaseCommand.option_list + (
        make_option('--verify', action='store_true', dest='verify', default=False, help='Verify FlickrAPI OAuth Tokens'),
        make_option('--oauth_token', action='store', dest='oauth_token', default=False, help='FlickrAPI OAuth Token'),
        make_option('--oauth_verifier', action='store', dest='oauth_verifier', default=False, help='FlickrAPI OAuth Verifier'),
        make_option('--perms', action='store', dest='perms', default="write", help='FlickrAPI OAuth Permissions'),
    )

    def handle(self, *args, **options):

        for key in ['verify', 'oauth_token', 'oauth_verifier', 'perms']:
            setattr(self, key, options.get(key))

        if options.get('verify'):
            auth_props = self.flickr.api.get_auth_tokens(self.oauth_verifier)
            self.stdout.write('==== auth_props [{0}]'.format(auth_props))
        else:
            self.flickr.api.authenticate_via_browser(perms=self.perms)
