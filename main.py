import flet as ft
import asyncio
from server.config import Config
from client import ChatClient

DEVMODE = False
client = None

async def main(page: ft.Page):
    global client    
    config = Config().get('client')
    client = ChatClient(config).client
    progress_ring = ft.ProgressRing()
    progress_ring.visible = False

    async def send_click(e):
        query = new_message.value
        chat.controls.append(ft.Text(f"Q: {query}"))
        page.add(progress_ring)
        progress_ring.visible = True
        progress_ring.value = None  # Indeterminate mode
        page.update()
        if DEVMODE:
            response = f"You are in Dev Mode {dir(client.config.get('model'))}"
        else:
            try:
                response = await client.process_query(query)
            except asyncio.CancelledError:
                response = "Request cancelled."
                progress_ring.visible = False
                page.update()
                raise
        progress_ring.value = 1.0
        chat.controls.append(ft.Text(response))
        progress_ring.visible = False
        new_message.value = ""
        page.update()

    async def radiogroup_changed(e):
        global client
        t.value = f"Model is  {e.control.value}"
        config['model'] = e.control.value
        client = ChatClient(config).client
        try:
            response = await client.connect_to_server()
        except asyncio.CancelledError:
            raise
        chat.controls.append(ft.Text(response))
        page.views.pop()
        page.go("/")
        page.update()

    rg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="llama3.2", label="Llama3.2"),
                ft.Radio(value="qwen3", label="Qwen3"),
                ft.Radio(value="mistral-nemo", label="Mistral"),
                ft.Radio(value="claude-3-sonnet-20240229", label="Claude 3"),
                ft.Radio(value="claude-4-sonnet", label="Claude 4"),
            ]
        ),
        on_change=radiogroup_changed,
    )

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
    )
    #set page theme mode
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "OPENheidelberg MCP Client"
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    
    chat = ft.Column()
    t = ft.Text()
    button = ft.ElevatedButton("Send", on_click=send_click)
    button.bgcolor = ft.Colors.BLUE
    new_message = ft.TextField()
    new_message.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
    new_message.color = ft.Colors.BLACK
    usage = ft.Text("You can ask me everything\n"
                    "Popular Questions are:\n"
                    "- Who is a member of Openheidelberg?\n"    
                    "- What tasks is currently worked on?\n"
                    "- What are the next Events"    
                    )
    main_view = ft.View(
        "/",
        [
            ft.Container(
                content=ft.Text("Openheidelberg Chatbot"), 
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=15,
                alignment=ft.alignment.center,
                ),
            chat,
            progress_ring,
            ft.Container(
                content=ft.Row(controls=[new_message, button]),
                #bgcolor=ft.Colors.GREY_100,
                padding=15,
                alignment=ft.alignment.center,
                height=100,
                width=500,
            ),
            usage,
            ft.ElevatedButton("Settings", on_click=lambda _: page.go("/settings")),
        ],
    )
    main_view.scroll = ft.ScrollMode.AUTO
    
    
    def toggle_devmode(e):
        global DEVMODE
        DEVMODE = not DEVMODE

    dev_switch = ft.Switch(label="Dev Mode", on_change=toggle_devmode)

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.scroll = ft.ScrollMode.AUTO
        page.views.append(
            main_view
        )
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        ft.Container(
                            content=ft.Text("Settings"), 
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            padding=15,
                            alignment=ft.alignment.center,
                        ),
                        rg,
                        ft.Text("Select the model you want to use:"),
                        dev_switch,
                        ft.ElevatedButton("Back", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    # def go_settings(e):
    #     page.route = "/settings"
    #     page.update()

    page.on_route_change = route_change
    #page.add(ft.ElevatedButton("Settings", on_click=go_settings))
    page.views.append(main_view)
    page.update()
    # page.add(
    #     ft.AppBar(title=ft.Text("Openheidelberg Chatbot"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
    #     chat,
    #     ft.Container(
    #         content=ft.Row(controls=[new_message, button]),
    #         bgcolor=ft.Colors.GREY_100,
    #         padding=15,
    #         alignment=ft.alignment.center,
    #         height=100,
    #         width=500,
    #     ),
    #     ft.Container(
    #         content=usage,
    #         bgcolor=ft.Colors.GREY_50,
    #         padding=10,
    #         width=500,
    #     ),           
    #     ft.Container(
    #         content=dev_switch,
    #         bgcolor=ft.Colors.GREY_50,
    #         padding=10,
    #         width=500,
    #     ),        
    # )


ft.app(main, view=ft.AppView.WEB_BROWSER)
