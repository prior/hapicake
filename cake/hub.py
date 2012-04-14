from utils.property import cached_property
from utils.dict import mget,merge
from giftwrap import Auth
from .settings import Settings

class Hub(Auth):
    domain = 'api.hubapi.com'

    def __init__(self, oauth_token=None, *args, **kwargs):
        super(Auth, self).__init__(*args,**kwargs)
        self.oauth_token = oauth_token
        
        #deprecated stuff
        self.id = mget(kwargs,'id','hub_id','portal_id','portalId')
        self.api_key = mget(kwargs,'api_key','hapi_key','hapiKey')

    def params(self): 
        if self.oauth_token: return {'access_token': self.oauth_token}
        return merge({'portalId':self.id},self.api_key and {'api_key':self.api_key} or {})


    @property  # printable env string
    def env_formal(self): return self.env=='prod' and 'Production' or 'QA'




    # settings shortcuts
    @cached_property
    def settings(self): return Settings(self)

    @property
    def company(self): return self.settings.scope(domains=True)['companyName'].value
    @property
    def cms_domain(self): return self.settings.scope(domains=True)['cmsPrimaryDomain'].value
    @property
    def app_domain(self): return self.settings.scope(domains=True)['primaryAppDomain'].value
    @property
    def timezone(self): return self.settings['hubspot:timezone'].value

