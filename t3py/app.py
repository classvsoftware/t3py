import asyncio
from typing import Optional

import httpx
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Label, Static

from t3py.commands.identity import check_identity

LATEST_VERSION_URL = "https://pypi.org/pypi/t3py/json"


class T3PyApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh", "Check Identity")]

    def __init__(self, api_auth_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_auth_data = api_auth_data
        self.user_identity = check_identity(api_auth_data)
        self.latest_version = None

    async def check_for_updates(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(LATEST_VERSION_URL)
                response.raise_for_status()
                latest_version = response.json()["info"]["version"]
                self.latest_version = latest_version
        except Exception:
            self.latest_version = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"Authenticated as: {self.user_identity}", classes="user-info")
        if self.latest_version:
            yield Static(
                f"[bold yellow]Update available: {self.latest_version}. Run `pip install --upgrade t3py`.[/bold yellow]"
            )
        yield Vertical(
            Button("Check Identity", id="check_identity"),
            Button("Quit", id="quit"),
        )
        yield Footer()

    def on_mount(self):
        self.call_later(self.check_for_updates)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "check_identity":
            self.notify("Checking Identity...", title="Status")
            check_identity(self.api_auth_data)
        elif event.button.id == "quit":
            self.exit()
