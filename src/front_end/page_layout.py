from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

def heading(title):
    return Div(cls="space-y-5")(
            Grid (H2(title),
                Button("Logout", cls=(ButtonT.secondary, "hover:bg-gray-600", "w-fit justify-self-end text-sm py-1 px-3"), hx_get="/logout", hx_push_url='true', hx_target='body')
            ),
            DividerSplit()
            )

sidebar = NavContainer(
    *map(lambda x: Li(A(x[0], href=x[1])), (("Users", "/users"), ("Rooms", "/rooms"), ("User's Media", "/media"),
                                         ("Reported Events", "/events"), ("Room directory", "/directory"),("Federation", "/federation"),
                                         ("Registration tokens", "/reg-tokens"))),
    cls=(NavT.secondary,"space-y-4 p-4 w-1/8"))

def FormLayout(title, *content, cls='mt-4'): return Container(cls=("mt-5 ml-1 mr-1", ContainerT.expand))(content)

def get_page_layout(title, message, content, type):
    return Title(title),Container(cls=("mt-5 ml-1 mr-1", ContainerT.expand))(
        heading(title),
        Div(cls=("flex gap-x-6"))(
            sidebar,
            FormLayout(title, content, cls='mt-4 w-full')
        )
    )