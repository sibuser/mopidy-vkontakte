from __future__ import unicode_literals

import os

from mopidy import config, ext

__doc__ = """An extension for playing music from VKontakte.

This extension enables you to play music from VKontakte web service.

See https://github.com/sibuser/mopidy-vkontakte for further instructions
of using this extension.

**Issues:**

https://github.com/sibuser/mopidy-vkontakte/issues

"""

__version__ = '0.1.2'


class Extension(ext.Extension):

    dist_name = 'Mopidy-VKontakte'
    ext_name = 'vkontakte'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['email'] = config.String()
        schema['password'] = config.Secret()
        schema['client_id'] = config.Secret()

        return schema

    def validate_config(self, config):
        if not config.getboolean('vkontakte', 'enabled'):
            return

    def get_backend_classes(self):
        from .actor import VKBackend
        return [VKBackend]
