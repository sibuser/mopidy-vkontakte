from __future__ import unicode_literals

import unittest

from mopidy_vkmusic import Extension, actor as backend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[vkontakte]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('email', schema)
        self.assertIn('password', schema)

    def test_get_backend_classes(self):
        ext = Extension()

        backends = ext.get_backend_classes()

        self.assertIn(backend_lib.VKBackend, backends)
