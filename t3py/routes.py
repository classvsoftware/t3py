from dataclasses import dataclass
from enum import Enum, auto

from rich.console import Console, Group

from t3py.commands.check_identity import check_identity_handler
from t3py.commands.exit import exit_handler

console = Console()


class T3RouteName(Enum):
    CHECK_IDENTITY = auto()
    EXIT = auto()


@dataclass
class T3Route:
    name: T3RouteName
    description: str
    handler: function

    def run(self):
        console.clear()
        self.handler()


routes = [
    T3Route(
        name=T3RouteName.CHECK_IDENTITY,
        description="Check Identity",
        handler=check_identity_handler,
    ),
    T3Route(name=T3RouteName.EXIT, description="Exit", handler=exit_handler),
]
