from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
import logging

import front_end.login as flogin
import back_end.login as b_login
import back_end.users as b_users
import back_end.media as b_media
import front_end.page_layout as fpl
import front_end.user_list as ul
import front_end.home_page as home_page
import front_end.user_edit_page as uep

from entities.user import UserDTO_extend

app, rt = fast_app(hdrs=Theme.blue.headers(mode='light'))

logger = logging.getLogger('uvicorn.error')
token = None
home_server = None
current_user = None

@app.get('/')
def index(message = None):
    return flogin.get_login_page(message=message)

@app.post('/login')
def login(username : str, password : str, homeserver : str):
    global token, home_server
    logger.info(f'Username: {username}, Password: {"*" * len(password)}, Password Length: {len(password)}, Homeserver: {homeserver}')
    response = b_login.to(username, password, homeserver)
    if response.status_code == 200:
        token = response.json()['access_token']
        home_server = homeserver
        return RedirectResponse(url='/users', status_code=302)
    else:
        return index(message=response.text)

@app.get('/logout')
def logout():
    global token, home_server, current_user
    token = None
    home_server = None
    current_user = None
    return RedirectResponse(url='/', status_code=302)

@app.get('/users')
def users(next_token = None, limit : int = 10, guests : bool = False):
    global token, home_server
    logger.info(f'Make Get Request to /_synapse/admin/v2/users/?from={0 if next_token is None else next_token}&limit={limit}&guests={guests}')
    response = b_users.get_users_info(homeserver=home_server, token=token, next_token=next_token, limit=limit, guests=guests)
    return fpl.get_page_layout('Users', 'Users', ul.get_users_page(response), 'user')

@app.post('/users/create')
def user_create(user_id : str = None, displayname : str = None, password : str = None, user_type : str = None, admin : bool = False):
    global token, home_server
    logger.info(f'Make Post Request to /_synapse/admin/v2/users')
    print(user_id, displayname, password, user_type, admin)
    response = b_users.create_user(homeserver=home_server, token=token, user_id=user_id, displayname=displayname, password=password, user_type=user_type, admin=admin)
    print(response.text)
    return RedirectResponse(url='/users', status_code=302)

@app.get('/users/{user_id}')
def user(user_id : str):
    
    global token, home_server, current_user
    logger.info(f'Make Get Request to /_synapse/admin/v2/users/{user_id}')
    response = b_users.get_user_info_personal(user_id, homeserver=home_server, token=token)
    if isinstance(response, UserDTO_extend):
        current_user = response
    #TODO request user info
    page = uep.user_edit_page(user_id, 1, response)
    username = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + username + "\'", "User page", page, "user")

@app.post('/users/{user_id}/save')
def user_save(user_id : str, displayname : str = None, password : str = None, user_type : str = None, admin : bool = False, locked : bool = False, deactivated : bool = False):
    global token, home_server, current_user
    logger.info(f'Make Put Request to /_synapse/admin/v2/users/{user_id}')
    # print(user_type)
    responce = b_users.update_user_info(current_user, homeserver=home_server, token=token, id=user_id, displayname=displayname, password=password, admin=admin, locked=locked, deactivated=deactivated, user_type=user_type)
    # print(responce.text)
    current_user = None
    return RedirectResponse(url='/users/{user_id}', status_code=302)

@app.get('/users/{user_id}/email')
def user_get_3pids(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get 3pids for {user_id}')
    page = uep.user_edit_page(user_id, 2, current_user)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

@app.post('/users/{user_id}/email/save')
def user_save_3pid(user_id : str, medium_type : str = None, address : str = None):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get 3pids for {user_id}')
    current_user = b_users.update_user_info(current_user=current_user, homeserver=home_server, token=token, id=user_id,threepid=[medium_type, address])
    return RedirectResponse(url=f"/users/{user_id}/email", status_code=302)

@app.post('/users/{user_id}/email/delete')
def user_delete_3pid(user_id : str, medium : str = None, address : str = None):
    global token, home_server, current_user
    logger.info(f'Make Get Request to delete 3pid for {user_id}')
    current_user = b_users.delete_threepid(current_user=current_user, homeserver=home_server, token=token, id=user_id,threepid=[medium, address])
    return RedirectResponse(url=f"/users/{user_id}/email", status_code=302)

@app.get('/users/{user_id}/devices')
def user_get_devices(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get devices for {user_id}')
    content = b_users.get_user_info_devices(user_id, homeserver=home_server, token=token)
    page = uep.user_edit_page(user_id, 4, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

@app.get('/users/{user_id}/connections')
def user_get_connections(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get connections for {user_id}')
    content = b_users.get_user_info_connections(user_id, homeserver=home_server, token=token)
    page = uep.user_edit_page(user_id, 5, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

@app.get('/users/{user_id}/sso')
def user_get_sso(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get sso for {user_id}')
    #TODO get content
    content = None
    page = uep.user_edit_page(user_id, 3, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

@app.get('/users/{user_id}/media')
def user_get_media(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get media for {user_id}')
    content = b_users.get_user_info_media(user_id=user_id, homeserver=home_server, token=token)
    page = uep.user_edit_page(user_id, 6, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

@app.post('/users/{user_id}/media/quarantine')
def user_add_media_to_quarantine(user_id : str, media_id : str = None):
    global token, home_server, current_user
    logger.info(f'Make Post Request to quarantining media {media_id}')
    b_media.quarantining_media_by_id(homeserver=home_server ,token=token, media_id=media_id, user_id=user_id)
    return RedirectResponse(url=f"/users/{user_id}/media", status_code=302)

@app.post('/users/{user_id}/media/unquarantine')
def user_delete_media_from_quarantine(user_id : str, media_id : str = None):
    global token, home_server, current_user
    logger.info(f'Make Post Request to unquarantine media {media_id}')
    b_media.remove_media_form_quarantine_by_id(homeserver=home_server ,token=token, media_id=media_id, user_id=user_id)
    return RedirectResponse(url=f"/users/{user_id}/media", status_code=302)

@app.post('/users/{user_id}/media/protect')
def user_protect_media_from_quarantine(user_id : str, media_id : str = None):
    global token, home_server, current_user
    logger.info(f'Make Post Request to quarantining media {media_id}')
    b_media.protect_media_from_being_quarantied_by_id(homeserver=home_server ,token=token, media_id=media_id)
    return RedirectResponse(url=f"/users/{user_id}/media", status_code=302)

@app.post('/users/{user_id}/media/unprotect')
def user_unprotect_media_from_quarantine(user_id : str, media_id : str = None):
    global token, home_server, current_user
    logger.info(f'Make Post Request to unquarantine media {media_id}')
    b_media.unprotect_media_from_being_quarantied_by_id(homeserver=home_server ,token=token, media_id=media_id)
    return RedirectResponse(url=f"/users/{user_id}/media", status_code=302)

@app.delete('/users/{user_id}/media/delete')
def user_dewlete_media(user_id : str, media_id : str = None):
    global token, home_server, current_user
    logger.info(f'Make Delete Request to delete media {media_id}')
    b_media.delete_media_by_id(homeserver=home_server ,token=token, media_id=media_id, user_id=user_id)
    return RedirectResponse(url=f"/users/{user_id}/media", status_code=303)

@app.get('/users/{user_id}/rooms')
def user_get_rooms(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get rooms for {user_id}')
    content = b_users.get_user_info_rooms(user_id=user_id, homeserver=home_server, token=token)
    page = uep.user_edit_page(user_id, 7, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")


@app.get('/users/{user_id}/pushers')
def user_get_pushers(user_id : str):
    global token, home_server, current_user
    logger.info(f'Make Get Request to get pushers for {user_id}')
    content = b_users.get_user_info_pushers(user_id=user_id, homeserver=home_server, token=token)
    page = uep.user_edit_page(user_id, 8, content)
    user = b_users.parse_username_from_id(user_id)
    return fpl.get_page_layout("User : \'" + user + "\'", "User page", page, "user")

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5001, reload=True)
    # serve()