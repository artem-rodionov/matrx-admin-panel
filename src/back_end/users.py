import requests as req

from entities.user import UserDTO, UserDTO_extend, Threepid, PusherDTO
from entities.connection import Connection, Device
from entities.media import MediaDTO

def get_users_info(homeserver = 'https://matrix.org', token = '', next_token = None, limit = 10, guests = False):
    response = req.get(
        url=homeserver + '/_synapse/admin/v2/users?from=' + ('0' if next_token is None else next_token) + '&limit=' + str(limit) + '&guests=' + ('false' if not guests else 'true'),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    response = parse_to_userDTO(response)
    return response

def get_user_info_personal(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v2/users/' + user_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    response = parse_to_userDTO_extend(response)
    return response

def parse_username_from_id(user_id):
    username = user_id.split("@")[1].split(":")[0]
    return username

def parse_server_from_id(user_id):
    servername = user_id.split("@")[1].split(":")[1]
    return servername

def parse_to_userDTO(response):
    users = []
    for user in response.json()['users']:
        users.append(
            UserDTO(
                user['name'],
                user['is_guest'],
                user['admin'],
                user['user_type'],
                user['deactivated'],
                user['erased'],
                user['shadow_banned'],
                user['displayname'],
                user['avatar_url'],
                user['creation_ts'],
                user['locked']
            )
        )
    return users

def parse_to_userDTO_extend(response):
    return UserDTO_extend(
        response.json()['name'],
        response.json()['displayname'],
        response.json()['threepids'],
        response.json()['avatar_url'],
        response.json()['is_guest'],
        response.json()['admin'],
        response.json()['deactivated'],
        response.json()['erased'],
        response.json()['shadow_banned'],
        response.json()['creation_ts'],
        response.json()['last_seen_ts'],
        response.json()['appservice_id'],
        response.json()['consent_server_notice_sent'],
        response.json()['consent_version'],
        response.json()['consent_ts'],
        response.json()['external_ids'],
        response.json()['user_type'],
        response.json()['locked'],
        response.json()['suspended']
    )


def update_user_info(current_user : UserDTO_extend, homeserver = 'https://matrix.org', token = '', id : str = None, displayname : str = None, user_type : str = None, password : str = None, admin : bool = False, locked : bool = False, deactivated : bool = False, erased : bool = False, threepid : list = None):
    response = req.put(
        url=homeserver + '/_synapse/admin/v2/users/' + id,
        headers={
            'Authorization': 'Bearer ' + token
        },
        json={
            **({'password': password} if password is not None or password != '' else {}),
            **({'displayname': displayname} if displayname is not None else {}),
            **({'user_type': user_type} if user_type is not None or user_type != '' else {'user_type' : None}),
            **({'admin': admin} if admin is not None or admin != '' else {}),
            **({'locked': locked} if locked is not None or locked != '' else {}),
            **({'deactivated': deactivated} if deactivated is not None or deactivated != '' else {}),
            **({'threepids': [pid.to_dict() for pid in (current_user.threepids if current_user.threepids is not None else []) + [Threepid(threepid[0], threepid[1])]]})
        }
    )
    if response.status_code != 200:
        return response
    
    response = get_user_info_personal(id, homeserver=homeserver, token=token)
    return response

def delete_threepid(current_user : UserDTO_extend, homeserver = 'https://matrix.org', token = '', id : str = None, threepid : list = None):
    threepid_del = Threepid(threepid[0], threepid[1])
    new_threepids = []
    for threepid in current_user.threepids:
        if threepid != threepid_del:
            new_threepids.append(threepid)
    response = req.put(
        url=homeserver + '/_synapse/admin/v2/users/' + id,
        headers={
            'Authorization': 'Bearer ' + token
        },
        json={
            **({'threepids': [pid.to_dict() for pid in new_threepids]})
        }
    )

    if response.status_code != 200:
        return response
    response = get_user_info_personal(id, homeserver=homeserver, token=token)
    return response

def create_user(homeserver = 'https://matrix.org', token = '', user_id : str = None, displayname : str = None, password : str = None, user_type : str = None, admin : bool = False):
    response = req.put(
        url=homeserver + '/_synapse/admin/v2/users/' + user_id,
        headers={
            'Authorization': 'Bearer ' + token
        },
        json={
            'displayname': displayname,
            'password': password,
            'user_type': user_type if user_type is not None and user_type != 'null' else None,
            'admin': admin
        }
    )
    if response.status_code != 200:
        return response
    
def get_user_info_connections(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v1/whois/' + user_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    
    response = parse_to_user_connections(response.json())
    return response

def get_user_info_devices(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v2/users/' + user_id + '/devices',
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    
    response = parse_to_user_devices(response.json())
    return response

def parse_to_user_connections(response):
    connections = []
    devices = response['devices']
    for device in devices.values():
        for session in device['sessions']:
            for connection in session['connections']:
                connections.append(Connection(connection['ip'], connection['last_seen'], connection['user_agent']))

    return connections

def parse_to_user_devices(response):
    devices = []
    for device in response['devices']:
        devices.append(Device(device['device_id'], device['display_name'], device['last_seen_ip'], device['last_seen_user_agent'], device['last_seen_ts'], device['user_id']))

    return devices

def get_user_info_media(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v1/users/' + user_id + '/media',
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    response = parse_to_user_media(response.json())
    return response

def parse_to_user_media(responce):
    media_list = []
    for media in responce['media']:
        media_list.append(MediaDTO(
            media['created_ts'],
            media['last_access_ts'],
            media['media_id'],
            media['media_length'],
            media['media_type'],
            media['quarantined_by'],
            media['safe_from_quarantine'],
            media['upload_name']
        ))
    return media_list

def get_user_info_rooms(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v1/users/' + user_id + '/joined_rooms',
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    response = parse_rooms_id(response.json())
    return response

def parse_rooms_id(responce):
    rooms_id = []
    for id in responce['joined_rooms']:
        rooms_id.append(id)
    return rooms_id

def get_user_info_pushers(user_id, homeserver = 'https://matrix.org', token = ''):
    response = req.get(
        url=homeserver + '/_synapse/admin/v1/users/' + user_id + '/pushers',
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    response = parse_to_user_pushers(response.json())
    return response

def parse_to_user_pushers(responce):
    pushers = []
    for pusher in responce['pushers']:
        print(pusher)
        pushers.append(
            PusherDTO(
                pusher['app_display_name'],
                pusher['app_id'],
                pusher['data'],
                pusher['device_display_name'],
                pusher['kind'],
                pusher['lang'],
                pusher['profile_tag'],
                pusher['pushkey']
            )
        )
    return pushers