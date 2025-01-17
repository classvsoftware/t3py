import getpass
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from t3py.commands.identity import check_identity
from t3py.utils.auth import authenticate_or_error

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
        # Display a table for the menu
        table = Table(title="Main Menu", title_style="bold magenta")
        table.add_column("Option", style="bold")
        table.add_column("Description")
        table.add_row("1", "Check Identity")
        table.add_row("2", "Dummy Operation 1")
        table.add_row("3", "Dummy Operation 2")
        table.add_row("4", "Exit")
        console.print(table)

        # Prompt user for input
        choice = Prompt.ask(
            "[bold yellow]Enter your choice[/bold yellow]",
            choices=["1", "2", "3", "4"],
            default="4",
        )

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


@app.command()
def main(
    hostname: str = typer.Option(
        None, help="The hostname where you log into Metrc (e.g., mo.metrc.com)."
    ),
    username: str = typer.Option(None, help="Username used to log into Metrc."),
    credential_file: Path = typer.Option(
        None,
        help="Path to a JSON file containing 'hostname', 'username', and 'password'.",
    ),
):
    """
    Authenticate with the Track and Trace Tools API and show a menu of options.
    """

    credentials = gather_credentials_or_error(hostname=hostname, username=username, credential_file=credential_file)


    api_auth_data = authenticate_or_error(
        credentials=credentials
    )
    
    show_menu(api_auth_data)
