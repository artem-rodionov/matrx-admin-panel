from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

def get_login_page(message = None):
    alert = None
    if message:
        alert = Alert(DivLAligned(UkIcon('triangle-alert'), 
                    P(message),),
                cls=AlertT.error)
    form = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
            alert if alert else "",
                DivCentered(cls='flex-1')(
                    Card(
                        DivVStacked(
                            H3("Welcome to Synapse-Admin")),
                            Form(method="post", action="/login")(
                    # Div(
                    #     Button("Choose Language", cls=(ButtonT.secondary, "w-full")),
                    #     DropDownNavContainer(
                    #         Li(A("Item 1",href=''),
                    #         Li(A("Item 2",href='')))
                    #         )
                    #     ),
                    # Label( 'Email',
                            Input(placeholder="Username", name="username", id="username", requires=True, cls="border-black"),
                        # ),
                            Input(type="password", placeholder="Password", name="password", id="password", requires=True, cls="border-black"),
                            Input(placeholder="Homeserver", name="homeserver", id="homeserver", requires=True, cls="border-black"),
                            Button(Span(cls="mr-2"), "Sign in", cls=(ButtonT.primary, "w-full"), type="submit", hx_attrs={"target":"body"}),
                        cls='space-y-6'
                        ),
                    cls="space-y-6 border-black border-2"
                )))
    
    return Title("Synapse-Admin"),Grid(form, gap=0,cls='h-screen')