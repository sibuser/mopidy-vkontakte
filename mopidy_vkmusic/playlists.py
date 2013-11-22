from __future__ import unicode_literals

import logging

from mopidy.backends import base, listener
from mopidy.models import Playlist, Track

logger = logging.getLogger('mopidy.backends.vkmusic.playlists')


class VKPlaylistsProvider(base.BasePlaylistsProvider):

    def __init__(self, *args, **kwargs):
        super(VKPlaylistsProvider, self).__init__(*args, **kwargs)
        self.config = self.backend.config
        self._playlists = []
        self.refresh()

    def create(self, name):
        pass

    def delete(self, uri):
        pass

    def _to_mopidy_track(self, song):
        return Track(
            uri=song['url'],
            name=song['title'],
            # artists=song['artist'].encode('utf-8'),
            length=int(song['duration']),
            bitrate=320)

    def lookup(self, uri):
        logger.debug('Resolving with %s', 'VKontakte')

        self.backend.session.get_all_songs()
        if uri:
            logger.info('Fetching a playlist %s from VKontakte' % uri)

            tracks = []

            for track in self.backend.session.get_all_songs():
                tracks.append(self._to_mopidy_track(track))
            return Playlist(
                uri='vkmusic:mylist',
                name='Music from VKontakte',
                tracks=tracks
            )
        else:
            return []

    def refresh(self):
        exp = self.lookup('vkontakte')
        self._playlists.append(exp)
        logger.info('Loaded %d VKontakte playlist(s)', len(self._playlists))
        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
