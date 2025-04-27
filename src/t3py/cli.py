import asyncio
from pathlib import Path
from typing import Optional

import typer

from t3py.app import T3PyApp
from t3py.utils.auth import (
    generate_api_auth_data_or_error,
    generate_credentials_snapshot_or_exit,
)

# Define the CLI app
cli_app = typer.Typer()


@cli_app.command()
def main(
    hostname: Optional[str] = typer.Option(
        None,
        "--hostname",
        "-h",
        help="The hostname where you log into Metrc (e.g., mo.metrc.com).",
    ),
    username: Optional[str] = typer.Option(
        None, "--username", "-u", help="Username used to log into Metrc."
    ),
    credential_file: Optional[Path] = typer.Option(
        None,
        "--credential-file",
        "-c",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help=(
            "Path to a JSON file containing 'hostname', 'username', and 'password'. "
        ),
    ),
):
    """Authenticate with Track & Trace Tools API and launch the UI."""
    credentials_snapshot = generate_credentials_snapshot_or_exit(
        hostname=hostname, username=username, credential_file_path=credential_file
    )
    api_auth_data = generate_api_auth_data_or_error(
        credentials_snapshot=credentials_snapshot
    )
    asyncio.run(T3PyApp(api_auth_data=api_auth_data).run_async())


if __name__ == "__main__":
    cli_app()