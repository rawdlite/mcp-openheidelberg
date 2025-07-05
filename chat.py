import flet as ft
import asyncio
from client import MCPClient


async def main(page: ft.Page):
    client = MCPClient()
    chat = ft.Column()
    new_message = ft.TextField()
    progress_ring = ft.ProgressRing()

    async def send_click(e):
        page.add(progress_ring)
        progress_ring.value = None  # Indeterminate mode
        page.update()
        #await client.connect_to_server()
        response = await client.process_query(new_message.value)
        progress_ring.value = 1.0
        chat.controls.append(ft.Text(response))
        new_message.value = ""
        page.update()

    response = await client.connect_to_server()
    chat.controls.append(ft.Text(response))
    page.add(
        chat, ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=send_click)])
    )

ft.app(main)
