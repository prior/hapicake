import unittest
from uuid import uuid4
from .hub_jukebox import hub_jukebox
#from .. import env

class SettingsTest(unittest.TestCase):

    def setUp(self): self.hub = hub_jukebox.default

    def tearDown(self): pass

    def test_shortcuts(self):
        self.assertEquals('google',self.hub.company)
        self.assertEquals('demohubapi.app6.hubspot.com',self.hub.app_domain)
        self.assertEquals('demo.hubapi.com',self.hub.cms_domain)
        self.assertEquals('Europe/London',self.hub.timezone)
        self.assertEquals(62515, self.hub.id)

    def test_crud(self): self._crud(u'unittest-%s'%str(uuid4()),str(uuid4()))
    
    @unittest.skip  # SKIPPING CUZ THIS FAILS!!!!  Apparently the settings api is not unicode enabled :(
    def test_unicode_crud(self): self._crud(u'unittest-\u2603-%s'%str(uuid4()),str(uuid4()))

    def _crud(self, key, value):
        if key in self.hub.settings:
            with self.hub.settings as s: del s[key]
            self.assertNotIn(key, self.hub.settings.refresh())
        with self.hub.settings as s: s[key]=value
        self.assertIn(key, self.hub.settings)
        self.assertEquals(value, self.hub.settings[key].value)
        self.assertIn(key, self.hub.settings.refresh())
        self.assertEquals(value, self.hub.settings[key].value)
        with self.hub.settings as s: del s[key]
        self.assertNotIn(key, self.hub.settings)
        self.assertNotIn(key, self.hub.settings.refresh())

