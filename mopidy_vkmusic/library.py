from __future__ import unicode_literals

import logging

from mopidy.backends import base
from mopidy.models import SearchResult

logger = logging.getLogger('mopidy.backends.vkmusic.library')


class VKLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(VKLibraryProvider, self).__init__(*args, **kwargs)

    def find_exact(self, **query):
        pass

    def search(self, **query):
        pass

    def lookup(self, uri):
        pass
