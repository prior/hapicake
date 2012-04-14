import os
import os.path
import json
from utils.property import cached_property
from utils.exception import Error
from .. import Hub

TEST_CREDS_FILENAME = 'creds.json'
COMMON_DISCLAIMER = """
Unittests rely on the existence of the file: '%s', and on it having valid credentials at least for the 'default' key.  See %s.example for what this file should look like.  
""" % (TEST_CREDS_FILENAME,TEST_CREDS_FILENAME)
PATHNAME = os.path.join(os.path.dirname(__file__), TEST_CREDS_FILENAME)

class TestError(Error): pass

class HubJukeBox(object):

    def __getitem__(self, key):
        try:
            return Hub(**self._hub_dict[key])
        except KeyError as err:
            msg = "%s doesn't appear to have a '%s' key, and these unittests rely the creds specified for that key.\n\n%s" % (key, TEST_CREDS_FILENAME, COMMON_DISCLAIMER)
            TestError(msg, err)._raise()

    @cached_property
    def default(self):
        if not os.path.exists(PATHNAME): return Hub(oauth_token = 'demooooo-oooo-oooo-oooo-oooooooooooo')
        return self.__getitem__('default')

    @cached_property
    def _hub_dict(self):
        try:
            raw_text = open(PATHNAME).read()
        except IOError as err:
            msg = "Unable to open '%s' for integration tests.\n\n%s" % (TEST_CREDS_FILENAME, COMMON_DISCLAIMER)
            TestError(msg, err)._raise()
        try:
            d = json.loads(raw_text)
        except ValueError as err:
            msg = "'%s' doesn't appear to be valid json!\n\n%s" % (TEST_CREDS_FILENAME, COMMON_DISCLAIMER)
            TestError(msg, err)._raise()
        return d


hub_jukebox = HubJukeBox()
