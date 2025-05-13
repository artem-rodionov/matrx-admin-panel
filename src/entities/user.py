import datetime


class UserDTO:
    def __init__(self, name : str , guest : int, admin : int, user_type : str, deactivated : int,
                  erased : bool, shadow : int, display_name : str, avatar_url : str, creation_ts : int, locked : bool):
        self.name = name
        self.is_guest = guest
        self.is_admin = admin
        self.user_type = user_type
        self.is_deactivated = deactivated
        self.is_erased = erased
        self.is_shadow_banned = shadow
        self.display_name = display_name
        self.avatar_url = avatar_url
        self.creation_date = ts_to_date(creation_ts)
        self.is_locked = locked


class UserDTO_extend:
     def __init__(self, name : str, display_name : str, threepids : list , avatar_url : str,
                  guest : int, admin : int, deactivated : int, erased : bool, shadow : int, 
                  creation_ts : int, last_seen_ts : int, appservice_id : str, consent_server_notice_sent : bool, consent_version : str, 
                  consent_ts : int, external_ids : list, user_type : str,locked : bool, suspended : bool):
        self.name = name
        self.is_guest = guest
        self.is_admin = admin
        self.user_type = user_type
        self.is_deactivated = deactivated
        self.is_erased = erased
        self.is_shadow_banned = shadow
        self.display_name = display_name
        self.avatar_url = avatar_url
        self.creation_date = ts_to_date(creation_ts)
        self.is_locked = locked
        self.is_suspended = suspended
        self.last_seen_date = ts_to_date(last_seen_ts) if last_seen_ts is not None else None
        self.threepids = from_list_to_threepids(threepids)
        self.external_ids = from_list_to_external_ids(external_ids)
        self.consent_server_notice_sent = consent_server_notice_sent
        self.consent_version = consent_version
        self.consent_ts = ts_to_date(consent_ts) if consent_ts is not None else None
        self.appservice_id = appservice_id

class Threepid:
    def __init__(self, medium : str, address : str, added_at : int = None, validated_at : int = None):
        self.medium = medium
        self.address = address
        self.added_at = ts_to_date(added_at) if added_at is not None else None
        self.validated_at = ts_to_date(validated_at) if validated_at is not None else None

    def to_dict(self):
        return {
            "medium": self.medium,
            "address": self.address
        }

    def __str__(self):
        return f"Medium: {self.medium}, Address: {self.address}, Added at: {self.added_at}, Validated at: {self.validated_at}"
    
    def __ne__(self, other):
        if self.medium == other.medium and self.address == other.address:
            return False
        return True
    
class ExternalId:
    def __init__(self, auth_provider : str, external_id : str):
        self.auth_provider = auth_provider
        self.external_id = external_id

def from_list_to_threepids(threepids):
    threepid_list = []
    for threepid in threepids:
        threepid_list.append(Threepid(threepid['medium'], threepid['address'], threepid['added_at'], threepid['validated_at']))
    return threepid_list

def from_list_to_external_ids(external_ids):
    external_id_list = []
    for external_id in external_ids:
        external_id_list.append(ExternalId(external_id['auth_provider'], external_id['external_id']))
    return external_id_list

class PusherDTO():
    def __init__(self, app_display_name : str = None, app_id : str = None, data : dict = None, device_display_name : str = None, 
                 kind : str = None, lang : str = None, profile_tag : str = None, pushkey : str = None):
        self.app_display_name = app_display_name
        self.app_id = app_id
        self.data = data
        self.device_display_name = device_display_name
        self.kind = kind
        self.lang = lang
        self.profile_tag = profile_tag
        self.pushkey = pushkey

def ts_to_date(ts):
        date = datetime.datetime.fromtimestamp(ts / 1000)
        return date.strftime('%Y-%m-%d, %H:%M:%S')