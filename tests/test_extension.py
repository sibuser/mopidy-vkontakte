from __future__ import unicode_literals

import mock
import unittest

from mopidy_vkontakte import Extension, actor as backend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[vkontakte]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('email =', config)
        self.assertIn('password =', config)
        self.assertIn('client_id = 4003293', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('email', schema)
        self.assertIn('password', schema)

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = Extension()
        ext.setup(registry)

        registry.add.assert_called_once_with('backend', backend_lib.VKBackend)
