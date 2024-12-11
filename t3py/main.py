import typer

from t3py.commands.identity import check_identity
from t3py.utils.auth import authenticate_or_error

app = typer.Typer()

def check_identity_option(api_auth_data):
    """Check the user's identity."""
    typer.echo("Checking identity...")
    check_identity(api_auth_data=api_auth_data)

def dummy_operation_1():
    """Perform a dummy operation."""
    typer.echo("Performing dummy operation 1...")


def dummy_operation_2():
    """Perform a dummy operation."""
    typer.echo("Performing dummy operation 2...")


def show_menu(api_auth_data):
    """Show a menu of options for the user to choose from."""
    while True:
        typer.echo("\nMain Menu:")
        typer.echo("1. Check Identity")
        typer.echo("2. Dummy Operation 1")
        typer.echo("3. Dummy Operation 2")
        typer.echo("4. Exit")

        choice = typer.prompt("Enter your choice", default="4")

        if choice == "1":
            check_identity_option(api_auth_data)
        elif choice == "2":
            dummy_operation_1()
        elif choice == "3":
            dummy_operation_2()
        elif choice == "4":
            typer.echo("Exiting the application. Goodbye!")
            break
        else:
            typer.echo("Invalid choice. Please try again.")


@app.command()
def main(
    hostname: str = typer.Option(..., help="The hostname of the Track and Trace Tools API (e.g., mo.metrc.com)."),
    username: str = typer.Option(..., help="Username for authentication with the Track and Trace Tools API."),
):
    """
    Authenticate with the Track and Trace Tools API and show a menu of options.
    """
    typer.echo("Authenticating...")
    api_auth_data = authenticate_or_error(hostname=hostname, username=username)
    typer.echo("Authentication successful!")

    show_menu(api_auth_data)