import typer

from t3py.commands.identity import check_identity
from t3py.utils.auth import authenticate_or_error

app = typer.Typer()


@app.command()
def main(
    hostname: str = typer.Option(..., help="The hostname of the Track and Trace Tools API (e.g., mo.metrc.com)."),
    username: str = typer.Option(..., help="Username for authentication with the Track and Trace Tools API."),
):
    """
    Authenticate with the Track and Trace Tools API.
    """
    api_auth_data = authenticate_or_error(hostname=hostname, username=username)
    
    check_identity(api_auth_data=api_auth_data)
    


if __name__ == "__main__":
    app()
