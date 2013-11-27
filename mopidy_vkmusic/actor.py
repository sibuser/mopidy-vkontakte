from __future__ import unicode_literals

import logging
import pykka

from mopidy.backends import base

from .library import VKLibraryProvider
from .playlists import VKPlaylistsProvider
from .session import VKSession


logger = logging.getLogger('mopidy.backends.vkontakte.actor')


class VKBackend(pykka.ThreadingActor, base.Backend):

    def __init__(self, config, audio):
        super(VKBackend, self).__init__()
        self.config = config
        self.session = VKSession(config=self.config)
        self.library = VKLibraryProvider(backend=self)
        self.playback = VKPlaybackProvider(audio=audio, backend=self)
        self.playlists = VKPlaylistsProvider(backend=self)

        self.uri_schemes = ['vkontakte']


class VKPlaybackProvider(base.BasePlaybackProvider):

    def play(self, track):
        return super(VKPlaybackProvider, self).play(track)
