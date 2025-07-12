import flet as ft
import asyncio
from server.config import Config
from client import ChatClient

DEVMODE = False


async def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )
    #set page theme mode
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "OPENheidelberg MCP Client"
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    config = Config().get('client')
    client = ChatClient(config).client
    chat = ft.Column()
    new_message = ft.TextField()
    new_message.bgcolor = ft.Colors.LIGHT_BLUE_50
    new_message.color = ft.Colors.BLACK
    progress_ring = ft.ProgressRing()
    
    def toggle_devmode(e):
        global DEVMODE
        DEVMODE = not DEVMODE

    async def send_click(e):
        query = new_message.value
        chat.controls.append(ft.Text(f"Q: {query}"))
        page.add(progress_ring)
        progress_ring.visible = True
        progress_ring.value = None  # Indeterminate mode
        page.update()
        if DEVMODE:
            response = "You are in Dev Mode"
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

    try:
        response = await client.connect_to_server()
    except asyncio.CancelledError:
        raise
    chat.controls.append(ft.Text(response))
    button = ft.ElevatedButton("Send", on_click=send_click)
    usage = ft.Text("You can ask me everything\n"
                    "Popular Questions are:\n"
                    "- Who is a member of Openheidelberg?\n"    
                    "- What tasks is currently worked on?\n"
                    "- What are the next Events"    
                    )
    dev_switch = ft.Switch(label="Dev Mode", on_change=toggle_devmode)
    #button.bgcolor = ft.colors.BLUE
    page.add(
        chat,
        ft.Container(
            content=ft.Row(controls=[new_message, button]),
            bgcolor=ft.Colors.GREY_100,
            padding=15,
            alignment=ft.alignment.center,
            height=100,
            width=500,
        ),
        ft.Container(
            content=usage,
            bgcolor=ft.Colors.GREY_50,
            padding=10,
            width=500,
        ),           
        ft.Container(
            content=dev_switch,
            bgcolor=ft.Colors.GREY_50,
            padding=10,
            width=500,
        ),        
    )


ft.app(main)
