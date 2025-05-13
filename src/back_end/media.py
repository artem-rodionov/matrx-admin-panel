import requests as req

from back_end.users import parse_server_from_id

def quarantining_media_by_id(homeserver = 'https://matrix.org', token = '', media_id : str = None, user_id : str = None):
    servername = parse_server_from_id(user_id=user_id)
    response = req.post(
        url=homeserver + '/_synapse/admin/v1/media/quarantine/' + servername + '/' + media_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    

def remove_media_form_quarantine_by_id(homeserver = 'https://matrix.org', token = '', media_id : str = None, user_id : str = None):
    servername = parse_server_from_id(user_id=user_id)
    response = req.post(
        url=homeserver + '/_synapse/admin/v1/media/unquarantine/' + servername + '/' + media_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    
def protect_media_from_being_quarantied_by_id(homeserver = 'https://matrix.org', token = '', media_id : str = None, user_id : str = None):
    response = req.post(
        url=homeserver + '/_synapse/admin/v1/media/protect/' + media_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    
def unprotect_media_from_being_quarantied_by_id(homeserver = 'https://matrix.org', token = '', media_id : str = None, user_id : str = None):
    response = req.post(
        url=homeserver + '/_synapse/admin/v1/media/unprotect/' + media_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response
    
def delete_media_by_id(homeserver = 'https://matrix.org', token = '', media_id : str = None, user_id : str = None):
    servername = parse_server_from_id(user_id=user_id)
    response = req.delete(
        url=homeserver + '/_synapse/admin/v1/media/' + servername + '/' + media_id,
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    if response.status_code != 200:
        return response