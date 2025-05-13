from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

from entities.user import UserDTO

user_list_columns = ["Checked", 'Avatar', 'User-ID', 'Displayname', 'Guest', 'Server Administrator', 'Deactivated', 'Locked', 'Erased', 'Creation timestamp', 'Actions']

def from_user_to_represent_dict(user : UserDTO):
    return {
        'Avatar': user.avatar_url,
        'User-ID': user.name,
        'Displayname': user.display_name,
        'Guest': ('✓' if user.is_guest else '❌'),
        'Server Administrator': ('✓' if user.is_admin else '❌'),
        'Deactivated': ('✓' if user.is_deactivated else '❌'),
        'Locked': ('✓' if user.is_locked else '❌'),
        'Erased': ('✓' if user.is_erased else '❌'),
        'Creation timestamp': user.creation_date,
        'Actions' : None
    }

def _Td(*args, cls='', **kwargs): return Td(*args, cls=cls, **kwargs)
def _Th(*args, cls='', **kwargs): return Th(*args, cls=cls, **kwargs)

def header_render(col):
    if col == 'Actions': 
        return _Th("",         expand=True)
    elif col == "Checked":
        return _Th(CheckboxX(), shrink=True)
    return Th(col,         expand=True)

current_user_id = ''

def body_cell_render(col, val):
    global current_user_id
    if col == 'User-ID':
        current_user_id = val
    if col == 'Actions':
        return _Td(task_dropdown())
    elif col == "Checked":
        return _Td(CheckboxX(), shrink=True)
    return _Td(val)

def task_dropdown():
    global current_user_id
    return Div(
                # A("Edit", href=f"/users/{current_user_id}", cls="uk-button uk-button-danger"),
                Button("Edit", cls=(ButtonT.secondary, "hover:bg-gray-600"), hx_get=f"/users/{current_user_id}", hx_push_url='true', hx_target='body')
            )

def user_list(users):
    user_dicts = list(map(lambda x: from_user_to_represent_dict(x), users))
    
    return Div(cls='mt-1')(
        Button("Create User", cls=(ButtonT.primary, "w-fit justify-self-end text-sm py-1 px-3"), data_uk_toggle="target: #my-modal", type="button"),
        Modal(
             Form(cls='space-y-5', id="form-container")(
                    LabelInput("User ID", type="text", placeholder="User ID", id="user_id", name="user_id"),
                    LabelInput("Displayname", type="text", placeholder="Display Name", id="displayname", name="displayname"),
                    LabelInput("Password" ,type="password", placeholder="Password", id="password", name="password"),
                    LabelSelect(
                        Option("Select type...", value="null", selected=True),
                        Option("Bot", value="bot"),
                        Option("Support", value="support"),
                        label="User Type", id="user_type", name="user_type"
                    ),
                    LabelSwitch("Server Administrator", id="admin", name="admin"),
                    #TODO Add some stuff
                    Button("Create", cls=(ButtonT.primary, "w-fit justify-self-end text-sm py-1 px-3"), hx_post="/users/create", hx_push_url='true', hx_target='body')
                ),
            header=ModalTitle("Create User"),
            # ModalBody(
               
            # ),
            footer=ModalCloseButton("Close", cls=(ButtonT.secondary, "hover:bg-gray-600")),
            id='my-modal'
        ),
        # Button("Open Modal",data_uk_toggle="target: #my-modal", type="button", cls=ButtonT.primary),
        # Modal(ModalTitle("Simple Test Modal"), 
        #       P("With some somewhat brief content to show that it works!", cls=TextPresets.muted_sm),
        #       footer=ModalCloseButton("Close", cls=ButtonT.primary),id='my-modal'),
        TableFromDicts(
            header_data=user_list_columns,
            body_data=user_dicts,
            header_cell_render=header_render,
            body_cell_render=body_cell_render,
            sortable=True
        )
    )

def get_users_page(users):
    content = Div(cls="space-y-5")(
        user_list(users)
    )
    return content