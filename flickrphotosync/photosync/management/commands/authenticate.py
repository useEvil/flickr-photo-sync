import os

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from photosync.flickr import Flickr
from photosync.helpers import *


class Command(BaseCommand):
    args = '<photoset photoset ...>'
    help = 'Imports photos froma photoset on Flickr'
    flickr = Flickr()

    option_list = BaseCommand.option_list + (
        make_option('--verify', action='store_true', dest='verify', default=False, help='Verify FlickrAPI OAuth Tokens'),
        make_option('--oauth_token', action='store', dest='oauth_token', default=False, help='FlickrAPI OAuth Token'),
        make_option('--oauth_verifier', action='store', dest='oauth_verifier', default=False, help='FlickrAPI OAuth Verifier'),
        make_option('--perms', action='store', dest='perms', default="delete", help='FlickrAPI OAuth Permissions'),
    )

    def handle(self, *args, **options):

        set_options(self, options, ['verify', 'oauth_token', 'oauth_verifier', 'perms'])

        if options.get('verify'):
            auth_props = self.flickr.api.get_auth_tokens(self.oauth_verifier)
            self.stdout.write('==== auth_props [{0}]'.format(auth_props))
        else:
            self.flickr.api.authenticate_via_browser(perms=self.perms)
