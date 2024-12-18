import getpass
import sys
from dataclasses import dataclass
from typing import Optional, cast

import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

from t3py.consts import BASE_URL, logger

from .http import get_request, post_request

# Initialize Rich Console
console = Console()

@dataclass
class Credentials:
    hostname: str
    username: str
    password: str
    otp: Optional[str] = None

@dataclass
class APIAuthData:
    auth_mode: str
    has_t3_plus: bool
    username: str
    hostname: str
    access_token: str
    refresh_token: str

def obtain_api_auth_data_or_error(
    *, session: requests.Session, credentials: Credentials
) -> APIAuthData:
    """
    Obtain access token using provided credentials.
    """
    console.print("[bold cyan]Obtaining access token...[/bold cyan]")
    url = f"{BASE_URL}/v2/auth/credentials"
    user_credential_data = {
        "hostname": credentials.hostname,
        "username": credentials.username,
        "password": credentials.password,
    }
    if credentials.otp:
        user_credential_data["otp"] = credentials.otp

    headers = {
        "Content-Type": "application/json",
    }

    authentication_response = post_request(session=session, headers=headers, url=url, data=user_credential_data)
    authentication_data = authentication_response.json()
    if authentication_data and "accessToken" in authentication_data:
        access_token = authentication_data["accessToken"]
        refresh_token = authentication_data["refreshToken"]

        console.print("[bold green]Authentication successful! Retrieving identity...[/bold green]")
        url = f"{BASE_URL}/v2/auth/whoami"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        identity_response = get_request(session=session, url=url, headers=headers)
        identity_data = identity_response.json()

        if identity_data is None:
            raise ValueError("[bold red]Identity cannot be None[/bold red]")

        return APIAuthData(
            auth_mode=cast(str, identity_data.get("authMode", "")),
            access_token=access_token,
            refresh_token=refresh_token,
            has_t3_plus=cast(bool, identity_data.get("hasT3Plus", False)),
            username=cast(str, identity_data.get("username", "")),
            hostname=cast(str, identity_data.get("hostname", ""))
        )

    console.print("[bold red]Failed to obtain access token. Please check your credentials.[/bold red]")
    raise Exception("Failed to obtain access token. Please check your credentials.")

def authenticate_or_error(*, hostname: str, username: str) -> APIAuthData:
    """
    Handle the authentication process with the T3 API.
    """
    console.print(f"[bold yellow]Password required for {hostname}/{username}[/bold yellow]")
    password = getpass.getpass(prompt=Text("Password: ", style="bold yellow"))

    otp = None
    if hostname == "mi.metrc.com":
        console.print("[bold yellow]Enter OTP for additional verification.[/bold yellow]")
        otp = getpass.getpass(prompt=Text("OTP: ", style="bold yellow"))

    credentials = Credentials(
        hostname=hostname, username=username, password=password, otp=otp
    )

    with requests.Session() as session:
        try:
            api_auth_data = obtain_api_auth_data_or_error(session=session, credentials=credentials)
            console.print("[bold green]Authentication process completed successfully![/bold green]")
            return api_auth_data
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            logger.error("Failed to authenticate.")
            sys.exit(1)
