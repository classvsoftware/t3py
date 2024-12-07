"""Console script for t3py."""
import t3py

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for t3py."""
    console.print("Replace this message by putting your code into "
               "t3py.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
