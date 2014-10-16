from __future__ import unicode_literals

import logging
import pykka

from mopidy import backend

from .library import VKLibraryProvider
from .playlists import VKPlaylistsProvider
from .session import VKSession


logger = logging.getLogger(__name__)


class VKBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(VKBackend, self).__init__()
        self.config = config
        self.session = VKSession(config=self.config)
        self.library = VKLibraryProvider(backend=self)
        self.playback = backend.PlaybackProvider(audio=audio, backend=self)
        self.playlists = VKPlaylistsProvider(backend=self)

        self.uri_schemes = ['vkontakte']
