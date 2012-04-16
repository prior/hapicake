from utils.property import cached_property,is_cached,delete_cache
from utils.dict import mget,merge
from giftwrap import JsonExchange
from sanetime import ntime


class Settings(object):
    def __init__(self, hub, **kwargs):
        super(Settings, self).__init__()
        self.hub = hub
        self.sm = self.domains = self.all = False
        self.pending_creates = {}
        self.pending_deletes = set()

    def scope(self, **kwargs):
        for attr in ('sm','domains','all'):
            val = kwargs.get(attr,False)
            if is_cached(self,'_settings_ex') and getattr(self._settings_ex,attr) != val and val:
                self.refresh()
            setattr(self,attr,val)
        return self

    def refresh(self):
        delete_cache(self,'_settings_ex','_settings')
        return self

    @cached_property
    def _settings(self): return dict((s.name,s) for s in self._settings_ex.result)
    @cached_property
    def _settings_ex(self): return GetSettings(self.hub, self.sm, self.domains, self.all)

    def __getitem__(self, name): return self._settings.get(name,None)
    def __setitem__(self, name, value): 
        setting = Setting(self, name=name, value=value)
        self.pending_creates[setting.name] = setting
        self.pending_deletes.discard(setting.name)
        if is_cached(self,'_settings'): self._settings[setting.name] = setting
    def __delitem__(self, name):
        self.pending_deletes.add(name)
        self.pending_creates.pop(name,None)
        if is_cached(self,'_settings') and self._settings.get(name): del self._settings[name]

    def persist_changes(self):
        exchanges = []
        exchanges.extend([SetSetting(self.hub,setting) for setting in self.pending_creates.values()])
        exchanges.extend([DeleteSetting(self.hub,name) for name in self.pending_deletes])
        return all([ex.result for ex in JsonExchange.async_exchange(exchanges)])

    def __enter__(self): return self
    def __exit__(self, type, value, traceback): 
        if type is None: self.persist_changes()

    def __contains__(self, item): return item in self._settings
    def __len__(self): return len(self._settings)
    def __iter__(self): return iter(self._settings)


class Setting(object):
    def __init__(self, hub, **kwargs):
        super(Setting, self).__init__()
        self.hub = hub
        self.name = kwargs.get('name')
        self.value = kwargs.get('value')
        self.app_key = mget(kwargs,'app_key','appKey')
        self.created_at = ntime(ms=kwargs.get('createdAt')) or kwargs.get('created_at')
        self.updated_at = ntime(ms=kwargs.get('updatedAt')) or kwargs.get('updated_at')
        self.readonly = kwargs.get('readonly',False)
        hub_id = mget(kwargs,'hub_id','portal_id','portalId')
        if hub_id: 
            if not hub.id: hub.id = hub_id
            elif hub_id!=hub.id: raise Exception('wtf-- that shouldnt have happened -- hub.id=%s , hub_id=%s' % (hub.id, hub_id))

class SettingsExchange(JsonExchange):
    base_path = 'settings/v1'
    sub_path = 'settings'

    
class GetSettings(SettingsExchange):
    debug=True
    def __init__(self, auth, sm=False, domains=False, all=False, **kwargs):
        super(GetSettings, self).__init__(auth, **kwargs)
        self.sm = sm
        self.domains = domains
        self.all = all

    def params(self):
        p = {}
        if self.all: p['readOnly']='true'
        if self.sm: p['sm']='true'
        if self.domains: p['domains']='true'
        return p
    def process_data(self, data, response): 
        settings = []
        for item in data:
            if item['name'] == 'readOnly':
                for itemx in item['value']:
                    if itemx.get('value'):
                        settings.append(Setting(self.auth, **merge(itemx,readonly=True)))
            else:
                if item.get('value'):
                    settings.append(Setting(self.auth, **item))
        return settings


class SetSetting(SettingsExchange):
    def __init__(self, auth, setting, **kwargs):
        super(SetSetting, self).__init__(auth, **kwargs)
        self.setting = setting

    method = 'post'
    def params(self): return {'name':self.setting.name, 'value':self.setting.value}
    def process_response(self, response): return response.status_code == 201


class DeleteSetting(SettingsExchange):
    def __init__(self, auth, name, **kwargs):
        super(DeleteSetting, self).__init__(auth, **kwargs)
        self.name = name

    method = 'delete'
    def params(self): return {'name':self.name}
    def process_response(self, response): return response.status_code == 201



