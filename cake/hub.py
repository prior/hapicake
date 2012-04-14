from utils.property import cached_property
from utils.dict import mget
from utils.obj import nchain
from giftwrap import Auth
from .settings import Settings

class Hub(Auth):
    domain = 'api.hubapi.com'

    def __init__(self, oauth_token=None, *args, **kwargs):
        super(Auth, self).__init__(*args,**kwargs)
        self.oauth_token = oauth_token
        
        #deprecated stuff
        self.api_key = mget(kwargs,'api_key','hapi_key','hapiKey')  # avaible for legacy usage
        self.id = mget(kwargs,'id','hub_id','portal_id','portalId')  # id only required for global api_keys

    def params(self): 
        if self.oauth_token: return {'access_token': self.oauth_token}
        return {'portalId':self.id, 'hapikey':self.api_key}






    # settings shortcuts
    @cached_property
    def settings(self): return Settings(self)

    @property
    def company(self): return nchain(self.settings.scope(domains=True)['companyName'],'value')
    @property
    def cms_domain(self): return nchain(self.settings.scope(domains=True)['cmsPrimaryDomain'],'value')
    @property
    def app_domain(self): return nchain(self.settings.scope(domains=True)['primaryAppDomain'],'value')
    @property
    def timezone(self): return nchain(self.settings['hubspot:timezone'],'value')




