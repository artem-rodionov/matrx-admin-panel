from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

from entities.user import UserDTO_extend, Threepid, PusherDTO
from entities.connection import Connection, Device
from entities.media import MediaDTO

def _Td(*args, cls='', **kwargs): return Td(*args, cls=cls, **kwargs)
def _Th(*args, cls='', **kwargs): return Th(*args, cls=cls, **kwargs)

def header_render_threepid(col):
    if col == 'Actions': 
        return _Th("",         expand=True)
    return Th(col,         expand=True)


def body_cell_render_threepid(col, val):
    if col == 'Actions':
        return _Td(get_button_delete_medium(val))
    return _Td(val)

def body_cell_render_media(col, val):
    if col == 'Quarantine':
        return _Td(get_button_quarantine(val))
    elif col == 'Safe from quarantine':
        return _Td(get_button_protect_from_quarantine(val))
    elif col == 'Delete':
        return _Td(get_button_delete_media(val))
    return _Td(val)

def get_button_delete_medium(val):
    unpack = val.split(",")
    return Button("Delete", cls=(ButtonT.destructive, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{unpack[0]}/email/delete?medium={unpack[1]}&address={unpack[2]}", hx_push_url='true', hx_target='body')

def get_button_delete_media(val):
    return Button("Delete", cls=(ButtonT.destructive, "w-fit justify-self-end text-sm py-1 px-3"), hx_delete=f"/users/{val[1]}/media/delete?media_id={val[0]}", hx_push_url='true', hx_target='body')

def get_button_protect_from_quarantine(val):
    button = None
    if val[3]:
        button = Button("❌", cls=(ButtonT.ghost, "w-fit justify-self-end text-sm py-1 px-3"))
    elif val[0]:
        button = Button("Make unsafe", cls=(ButtonT.destructive, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{val[2]}/media/unprotect?media_id={val[1]}", hx_push_url='true', hx_target='body')
    else:
        button = Button("Make safe", cls=(ButtonT.default, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{val[2]}/media/protect?media_id={val[1]}", hx_push_url='true', hx_target='body')
    return button

def get_button_quarantine(val):
    button = None
    if val[3]:
        button = Button("❌", cls=(ButtonT.ghost, "w-fit justify-self-end text-sm py-1 px-3"))
    elif val[0]:
        button = Button("Remove from quarantine", cls=(ButtonT.destructive, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{val[2]}/media/unquarantine?media_id={val[1]}", hx_push_url='true', hx_target='body')
    else:
        button = Button("Add to quarantine", cls=(ButtonT.default, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{val[2]}/media/quarantine?media_id={val[1]}", hx_push_url='true', hx_target='body')
    return button

def get_user_info_form(user_id, content : UserDTO_extend = None):
    return Div (cls="space-y-5 mt-1")(
            Form (cls='space-y-5')(
            
            LabelInput("User ID" ,type="text", placeholder="User ID", value=user_id, disabled=True),
            LabelInput("Displayname", type="text", placeholder="Display Name", value=content.display_name, id="displayname", name="displayname"),
            LabelInput("Password" ,type="password", placeholder="Password", id="password", name="password"),
            Small("Changing password will log user out of all sessions."),
            LabelSelect(
                Option("Select type...", value="null", selected=True if content.user_type is None else False),
                Option("Bot", value="bot", selected=True if content.user_type == "bot" else False),
                Option("Support", value="support", selected=True if content.user_type == "support" else False),
                label="User Type", id="user_type", name="user_type"
            ),
            LabelSwitch("Server Administrator", id="admin", name="admin", checked=True if content.is_admin else False),
            LabelSwitch("Locked", id="locked", name="locked", checked=True if content.is_locked else False),
            LabelSwitch("Deactivated", id="deactivated", name="deactivated", checked=True if content.is_deactivated else False),
            Small("You must provide a password to re-activate an account."),
            LabelSwitch("Erased", checked=True if content.is_erased else False, disabled=True),
           # Text("Creation timestamp: ", content.creation_date), TODO: trouble with timestamp
            Grid(
                Button("Save", cls=(ButtonT.primary, "w-full"), hx_post=f"/users/{user_id}/save", hx_push_url='true', hx_target='body'),
                Button("Delete", cls=(ButtonT.destructive, "w-full"), hx_get=f"/users/{user_id}/delete"),
            )
        )
    )

def from_user_to_represent_dict_threepid(pid : Threepid, user_id : str = None):
    return {
        'Medium': pid.medium,
        'Address': pid.address,
        'Added at': pid.added_at,
        'Validated at': pid.validated_at,
        'Actions': user_id + "," + pid.medium + "," + pid.address
    }

def from_devices_to_represent_dict(dev : Device):
    return {
        'Device ID' : dev.device_id,
        'Device name' : dev.display_name,
        'IP address' : dev.last_seen_ip,
        'Timestamp' : dev.last_seen
    }

def from_connection_to_represent_dict(con : Connection):
    return {
        'IP': con.ip,
        'Last seen': con.last_seen,
        'User agent': con.user_agent
    }

def from_media_to_represent_dict(media : MediaDTO, user_id: str = None):
    quarantine = True if media.quarantined_by is not None else False
    return {
        'Media ID': media.media_id,
        'Created': media.created_ts,
        'Last access': media.last_access_ts,
        'File Size (bytes)': media.media_length,
        'Type': media.media_type,
        'File upload name': media.upload_name,
        'Quarantined by': media.quarantined_by,
        'Quarantine': [quarantine, media.media_id, user_id, media.safe_from_quarantine],
        'Safe from quarantine': [media.safe_from_quarantine, media.media_id, user_id, quarantine],
        'Delete': [media.media_id, user_id]
    }

def from_rooms_to_represent_dict(room):
    return {
        'Room ID': room
    }

def from_pushers_to_represent_dict(pusher : PusherDTO):
    return {
        'App display name': pusher.app_display_name,
        'App ID': pusher.app_id,
        'Data': pusher.data, 
        'Device display name': pusher.device_display_name, 
        'Kind': pusher.kind, 
        'Lang': pusher.lang, 
        'Profile tag': pusher.profile_tag, 
        'Pushkey': pusher.pushkey
    }


def get_user_email_form(user_id, content : UserDTO_extend = None):
    header_data = ["Medium", "Address", "Added at", "Validated at", "Actions"]
    threepid_represented_dict = list(map(lambda x: from_user_to_represent_dict_threepid(x, user_id), content.threepids))
    for pid in content.threepids:
        print(pid)
    table = None
    if len(threepid_represented_dict) != 0:
        table =  TableFromDicts(
            header_data=header_data,
            body_data=threepid_represented_dict,
            header_render=header_render_threepid,
            body_cell_render=body_cell_render_threepid 
        )
    return Div (cls="space-y-5 mt-1")(
            Button("Add Medium", cls=(ButtonT.primary, "w-fit justify-self-end text-sm py-1 px-3"), data_uk_toggle="target: #my-modal", type="button"),
        Modal(
             Form (cls='space-y-5')(
                LabelSelect(
                    Option("Email", value="email"),
                    Option("Phone", value="msisdn"),
                    label="Medium", placeholder="Select type...", id="medium_type", name="medium_type"
                ),
                LabelInput("Address", type="text", placeholder="", id="address", name="address"),
                Button("Create", cls=(ButtonT.primary, "w-fit justify-self-end text-sm py-1 px-3"), hx_post=f"/users/{user_id}/email/save", hx_push_url='true', hx_target='body')
            ),
            header=ModalTitle("Create User"),
            # ModalBody(
               
            # ),
            footer=ModalCloseButton("Close", cls=(ButtonT.secondary, "hover:bg-gray-600")),
            id='my-modal'
        ),
        table
    )

def get_user_devices_form(user_id, content : list = None):
    header_data = ["Device ID", "Device name", "IP address", "Timestamp", "Actions"]
    body_data = list(map(lambda x: from_devices_to_represent_dict(x), content))
    return Div (cls="space-y-5 mt-1")(
            TableFromDicts(
                header_data=header_data,
                body_data=body_data
            )
    )

def get_user_connections_form(user_id, content : list = None):
    header_data = ["IP", "Last seen", "User agent"]
    body_data = list(map(lambda x: from_connection_to_represent_dict(x), content))
    return Div(cls="space-y-5 mt-1") (
            TableFromDicts(
                header_data=header_data,
                body_data=body_data
            )
    )

def get_user_media_form(user_id, content : list = None):
    header_data = ["Media ID", "Created", "Last access", "File Size (bytes)", "Type", "File upload name", "Quarantined by", "Quarantine", "Safe from quarantine", "Delete"]
    body_data = list(map(lambda x: from_media_to_represent_dict(x, user_id), content))
    return Div(cls="space-y-5 mt-1") (
            TableFromDicts(
                header_data=header_data,
                body_data=body_data,
                body_cell_render=body_cell_render_media
            )
    )

def get_user_sso_form(user_id, content : list = None):
    return Div()

def get_user_rooms_form(user_id, content : list = None):
    header_data = ["Room ID"]
    body_data = list(map(lambda x: from_rooms_to_represent_dict(x), content))
    return Div(cls="space-y-5 mt-1") (
            TableFromDicts(
                header_data=header_data,
                body_data=body_data
                # body_cell_render=body_cell_render_media
            )
    )

def get_user_pushers_form(user_id, content : list = None):
    header_data = ["App display name", "App ID", "Data", "Device display name", "Kind", "Lang", "Profile tag", "Pushkey"]
    body_data = list(map(lambda x: from_pushers_to_represent_dict(x), content))
    return Div(cls="space-y-5 mt-1") (
            TableFromDicts(
                header_data=header_data,
                body_data=body_data
                # body_cell_render=body_cell_render_media
            )
    )

def user_edit_page(user_id, command, content = None):
    body = None
    if command == 1:
        body = get_user_info_form(user_id, content)
    elif command == 2:
        body = get_user_email_form(user_id, content)
    elif command == 3:
        body = get_user_sso_form(user_id, content)
    elif command == 4:
        body = get_user_devices_form(user_id, content)
    elif command == 5:
        body = get_user_connections_form(user_id, content)
    elif command == 6:
        body = get_user_media_form(user_id, content)
    elif command == 7:
        body = get_user_rooms_form(user_id, content)
    elif command == 8:
        body = get_user_pushers_form(user_id, content)
    return Div(cls='space-y-5')(
            TabContainer(
                Li(A("User", href=f"/users/{user_id}"), cls="uk-active" if command == 1 else ""),
                Li(A("EMAIL / PHONE", href=f"/users/{user_id}/email"), cls="uk-active" if command == 2 else ""),
                Li(A("SSO", href=f"/users/{user_id}/sso"), cls="uk-active" if command == 3 else "#"),
                Li(A("Devices", href=f"/users/{user_id}/devices"), cls="uk-active" if command == 4 else "#"),
                Li(A("Connections", href=f"/users/{user_id}/connections"), cls="uk-active" if command == 5 else "#"), 
                Li(A("Media", href=f"/users/{user_id}/media"), cls="uk-active" if command == 6 else "#"), 
                Li(A("Rooms", href=f"/users/{user_id}/rooms"), cls="uk-active" if command == 7 else "#"), 
                Li(A("Pushers", href=f"/users/{user_id}/pushers"), cls="uk-active" if command == 8 else "#"),
            ),
        body
    )