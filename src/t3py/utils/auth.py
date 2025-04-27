import getpass
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, cast

import httpx
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

from t3py.consts.http import BASE_URL, logger
from t3py.interfaces.auth import APIAuthData, CredentialsSnapshot, StaticCredentials

from .http import get_request, post_request

# Initialize Rich Console
console = Console()


def metrc_hostname_uses_otp(*, hostname: str) -> bool:
    return hostname == "mi.metrc.com"


def obtain_api_auth_data_or_error(
    *, session: httpx.Client, credentials_snapshot: CredentialsSnapshot
) -> APIAuthData:
    """
    Obtain access token using provided credentials.
    """
    console.print("[bold cyan]Obtaining access token...[/bold cyan]")
    url = f"{BASE_URL}/v2/auth/credentials"
    user_credential_data = {
        "hostname": credentials_snapshot.hostname,
        "username": credentials_snapshot.username,
        "password": credentials_snapshot.password,
    }
    if credentials_snapshot.otp:
        user_credential_data["otp"] = credentials_snapshot.otp

    headers = {
        "Content-Type": "application/json",
    }

    authentication_response = post_request(
        session=session, headers=headers, url=url, data=user_credential_data
    )

    authentication_data = authentication_response.json()

    if authentication_data and "accessToken" in authentication_data:
        access_token = authentication_data["accessToken"]
        refresh_token = authentication_data["refreshToken"]

        console.print(
            "[bold green]Authentication successful! Retrieving identity...[/bold green]"
        )
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
            hostname=cast(str, identity_data.get("hostname", "")),
        )

    console.print(
        "[bold red]Failed to obtain access token. Please check your credentials.[/bold red]"
    )
    raise Exception("Failed to obtain access token. Please check your credentials.")


def gather_credentials_from_file_or_exit(
    *, credential_file_path: Path
) -> StaticCredentials:
    try:
        with open(credential_file_path, "r") as file:
            credential_file_data = json.load(file)
            hostname = credential_file_data.get("hostname")
            username = credential_file_data.get("username")
            password = credential_file_data.get("password")
            if not all([hostname, username, password]):
                raise ValueError(
                    "The JSON file must contain 'hostname', 'username', and 'password' fields."
                )
    except Exception as e:
        console.print(f"[bold red]Error reading credential file: {e}[/bold red]")
        raise typer.Exit(code=1)

    return StaticCredentials(hostname=hostname, username=username, password=password)


def gather_credentials_from_flags_and_cli_input_or_exit(
    *, hostname: Optional[str], username: Optional[str]
) -> StaticCredentials:

    if not hostname or not username:
        console.print(
            "[bold red]You must provide --hostname and --username if not using --credential-file.[/bold red]"
        )
        raise typer.Exit(code=1)

    console.print(
        f"[bold yellow]Password required for {hostname}/{username}[/bold yellow]"
    )
    password = getpass.getpass(prompt=f"Password for {hostname}/{username}: ")

    return StaticCredentials(hostname=hostname, username=username, password=password)


def gather_otp_from_cli_input_or_none(*, hostname: str) -> Optional[str]:
    otp = None
    if metrc_hostname_uses_otp(hostname=hostname):
        console.print(
            "[bold yellow]Enter OTP for additional verification.[/bold yellow]"
        )
        otp = getpass.getpass(prompt="OTP: ")

    return otp


def generate_credentials_snapshot_or_exit(
    *,
    hostname: Optional[str],
    username: Optional[str],
    credential_file_path: Optional[Path],
) -> CredentialsSnapshot:
    if credential_file_path:
        static_credentials = gather_credentials_from_file_or_exit(
            credential_file_path=credential_file_path
        )
    else:
        static_credentials = gather_credentials_from_flags_and_cli_input_or_exit(
            hostname=hostname, username=username
        )

    otp = gather_otp_from_cli_input_or_none(hostname=hostname)

    credentials_snapshot = CredentialsSnapshot(
        hostname=static_credentials.hostname,
        username=static_credentials.username,
        password=static_credentials.password,
        otp=otp,
    )

    return credentials_snapshot


def generate_api_auth_data_or_error(
    *, credentials_snapshot: CredentialsSnapshot
) -> APIAuthData:
    """
    Handle the authentication process with the T3 API.
    """
    console.print("[bold cyan]Authenticating...[/bold cyan]")

    with httpx.Client() as session:
        try:
            api_auth_data = obtain_api_auth_data_or_error(
                session=session, credentials_snapshot=credentials_snapshot
            )
            console.print(
                "[bold green]Authentication process completed successfully![/bold green]"
            )
            return api_auth_data
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            logger.error("Failed to authenticate.")
            sys.exit(1)