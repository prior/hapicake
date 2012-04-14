from utils.dict import mpop
from . import Hub

def __new_init__(self, *args, **kwargs):
    self.env = (mpop(kwargs,'env','environment') or '').lower() in ('production','prod') and 'prod' or 'qa'
    self.__old_init__(*args, **kwargs)

Hub.__old_init__ = Hub.__init__
Hub.__init__ = __new_init__

Hub.domain = lambda self: 'api.hubapi.com' if self.env=='prod' else 'api.hubapiqa.com'
Hub.env_formal = property(lambda self: 'Production' if self.env=='prod' else 'QA')
