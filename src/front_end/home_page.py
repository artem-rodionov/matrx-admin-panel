from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

import front_end.user_list as ul

def heading(title):
    return Div(cls="space-y-5")(
            H2(title),
            DividerSplit())


sidebar = NavContainer(
    *map(lambda x: Li(A(x)), ("Users", "Rooms", "User's Media", "Reported Events", "Room directory", "Federation", "Registration tokens")),
    uk_switcher="connect: #component-nav; animation: uk-animation-fade",
    cls=(NavT.secondary,"space-y-4 p-4 w-1/8"))

def FormLayout(title, *content, cls='space-y-3 mt-4'): return Container(cls=("mt-5 ml-1 mr-1", ContainerT.expand))(Form(*content, cls=cls))

def users_page(users):
    content = Div(cls="space-y-5")(
        ul.user_list(users)
    )

    return FormLayout("Users", *content)

def rooms_page():
    return

def user_media_page():
    return

def reported_events_page():
    return

def room_directory_page():
    return

def federation_page():
    return

def registration_tokens_page():
    return

def home_page(command, content):
    return Title("Home Page"),Container(cls=("mt-5 ml-1 mr-1", ContainerT.expand))(
        heading(command),
        Div(cls=("flex gap-x-6"))(
            sidebar,
                Ul(id="component-nav", cls="uk-switcher w-full")(
                    Li(cls="uk-active")(users_page(content),
                    *map(Li, [rooms_page(), user_media_page(), reported_events_page(), room_directory_page(), federation_page(), registration_tokens_page()])
                    )
                )
        )
    )