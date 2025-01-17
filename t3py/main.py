import getpass
import json
from pathlib import Path

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from t3py.commands.identity import check_identity
from t3py.utils.auth import (
    generate_api_auth_data_or_error,
    generate_credentials_snapshot_or_exit,
)

app = typer.Typer()
console = Console()


def check_identity_option(api_auth_data):
    """Check the user's identity."""
    console.print("[bold cyan]Checking identity...[/bold cyan]")
    check_identity(api_auth_data=api_auth_data)


def dummy_operation_1():
    """Perform a dummy operation."""
    console.print("[bold green]Performing dummy operation 1...[/bold green]")


def dummy_operation_2():
    """Perform a dummy operation."""
    console.print("[bold green]Performing dummy operation 2...[/bold green]")


def show_menu(api_auth_data):
    """Show a menu of options for the user to choose from."""
    while True:
        console.clear()

        # TODO show auth state

        # Display a table for the menu
        table = Table(box=box.SIMPLE_HEAD)
        table.add_column("Option", style="bold")
        table.add_column("Description")
        table.add_row("1", "Check Identity")
        table.add_row("2", "Exit")

        # Wrap the table in a panel
        panel = Panel(
            table, title="t3py Main Menu", title_align="left", border_style="purple"
        )

        console.print(panel)

        # Prompt user for input
        choice = Prompt.ask(
            "[bold yellow]Enter your choice[/bold yellow]",
        )

        console.clear()

        if choice == "1":
            check_identity_option(api_auth_data)
        elif choice == "2":
            dummy_operation_1()
        elif choice == "3":
            dummy_operation_2()
        elif choice == "4":
            console.print("[bold red]Exiting the application. Goodbye![/bold red]")
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        console.print("\n")
        console.input(
            "[bold purple]Press any key to return to main menu.[/bold purple]"
        )

@app.command()
def main(
    hostname: str = typer.Option(
        None,
        "--hostname",
        "-h",
        help="The hostname where you log into Metrc (e.g., mo.metrc.com).",
    ),
    username: str = typer.Option(
        None, "--username", "-u", help="Username used to log into Metrc."
    ),
    credential_file: Path = typer.Option(
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
    """
    Authenticate with the Track and Trace Tools API and show a menu of options.
    """

    credentials_snapshot = generate_credentials_snapshot_or_exit(
        hostname=hostname, username=username, credential_file_path=credential_file
    )

    api_auth_data = generate_api_auth_data_or_error(
        credentials_snapshot=credentials_snapshot
    )

    console.clear()

    show_menu(api_auth_data)


if __name__ == "__main__":
    app()
