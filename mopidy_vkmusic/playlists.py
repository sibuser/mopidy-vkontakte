from __future__ import unicode_literals

import logging

from mopidy.backends import base, listener
from mopidy.models import Playlist, Track, Artist

logger = logging.getLogger('mopidy.backends.vkontakte.playlists')


class VKPlaylistsProvider(base.BasePlaylistsProvider):

    def __init__(self, *args, **kwargs):
        super(VKPlaylistsProvider, self).__init__(*args, **kwargs)
        self.config = self.backend.config
        self._playlists = []
        self.all_lists = {}
        self.refresh()

    def create(self, name):
        pass

    def delete(self, uri):
        pass

    def _to_mopidy_track(self, song):
        return Track(
            uri=song['url'],
            name=song['title'],
            artists=[Artist(name=song['artist'].encode('utf-8'))],
            length=int(song['duration']) * 1000
        )

    def lookup(self, uri):
        return self.all_lists[uri]

    def _vk_playlist_to_mopidy(self, playlist):
        tracks = []
        logger.info(
            'Fetching a playlist "%s" from VKontakte'
            % playlist['title'])

        if playlist['title'] == 'all songs':
            songs = self.backend.library.get_all_songs()
        else:
            songs = self.backend.library.get_all_songs_from_album(
                playlist['album_id'])

        for song in songs:
            tracks.append(self._to_mopidy_track(song))

        return Playlist(
            uri='vkontakte:' + playlist['title'],
            name=playlist['title'],
            tracks=tracks
        )

    def refresh(self):
        self.all_lists['vkontakte:all songs'] = self._vk_playlist_to_mopidy(
            {'title': 'all songs'})

        self._playlists.append(self.all_lists['vkontakte:all songs'])

        vk_lists = self.backend.library.get_all_albums()
        for i in xrange(1, len(vk_lists)):
            title = 'vkontakte:' + vk_lists[i]['title']
            self.all_lists[title] = self._vk_playlist_to_mopidy(vk_lists[i])
            self._playlists.append(self.all_lists[title])

        logger.info(
            'Loaded' +
            ' {0} VKontakte playlist(s)'.format(len(self._playlists))
        )

        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
