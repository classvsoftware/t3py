
from t3py.consts import logger
from t3py.utils.auth import APIAuthData
from rich.console import Console

console = Console()

def check_identity(api_auth_data: APIAuthData):
    console.print("[bold cyan]Checking identity...[/bold cyan]")
    
    console.print("You successfully authenticated with the T3 API")
    console.print(
        f"The username '{api_auth_data.username}' {'is registered as a T3+ username and can use all API endpoints' if api_auth_data.has_t3_plus else 'is not registered and can only access free endpoints.'}"
    )
    console.print("T3 API docs can be found at https://trackandtrace.tools/api")
