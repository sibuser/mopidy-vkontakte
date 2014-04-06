from __future__ import unicode_literals

import logging
import collections
import urllib

from mopidy import backend, models
from mopidy.models import SearchResult

logger = logging.getLogger(__name__)


class VKLibraryProvider(backend.LibraryProvider):
    root_directory = models.Ref.directory(
        uri='vkontakte:directory',
        name='VKontakte'
    )

    def __init__(self, *args, **kwargs):
        super(VKLibraryProvider, self).__init__(*args, **kwargs)
        self.vfs = {'vkontakte:directory': collections.OrderedDict()}

    def generate_folders(self, lists):
        """
        Generates root folders wit names of your playlist
        """
        for name in lists:
            name = name.split(':')[1]
            self.add_to_vfs(self.new_folder(name.capitalize(), [name]))

    def new_folder(self, name, path):
        return models.Ref.directory(
            uri=self.generate_uri(path),
            name=name
        )

    def add_to_vfs(self, _model):
        self.vfs['vkontakte:directory'][_model.uri] = _model

    def tracklist_to_vfs(self, track_list):
        vfs_list = collections.OrderedDict()
        for temp_track in track_list:
            if hasattr(temp_track, 'uri'):
                vfs_list[temp_track.name] = models.Ref.track(
                    uri=temp_track.uri,
                    name=temp_track.name
                )
        return vfs_list.values()

    def browse(self, uri):

        if not self.vfs.get(uri):
            return self.tracklist_to_vfs(
                self.backend.playlists.all_lists['vkontakte:' +
                                                 uri.split(':')[2]].tracks)
        return self.vfs.get(uri, {}).values()

    def search(self, **query):
        if not query:
            return
        search_query = ' '.join(query.values()[0]['uri'])
        logger.info('Resolving Vkontakte for \'%s\'', search_query)
        if 'vk:' in search_query[0:3]:
            songs = self._search(search_query)
            tracks = []
            for song in songs[1:]:
                tracks.append(self.backend.playlists._to_mopidy_track(song))
            return SearchResult(
                uri='vkontakte:search',
                tracks=tracks
            )
        else:
            logger.info('Searching Vkontakte in playlists for \'%s\'',
                        search_query)

    def lookup(self, uri=None):
        return self.backend.playlists.all_lists

    def _search(self, query):
        return self.backend.session.call_api('audio.search', [
            ('q', query),
            ('auto_complete', 1),
            ('count', 170),
            ('performer_only1', 1)])

    def get_all_songs_from_album(self, album_id):
        return self.get_all_songs([('album_id', album_id)])

    def get_all_albums(self):
        return self.backend.session.call_api('audio.getAlbums')

    def get_all_songs(self, album_id=[]):
        if album_id:
            return self.backend.session.call_api(
                'audio.get', album_id)
        else:
            return self.backend.session.call_api('audio.get')

    def generate_uri(self, path):
        return 'vkontakte:directory:%s' % urllib.quote('/'.join(path))
