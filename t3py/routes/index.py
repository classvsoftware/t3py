from typing import List

from t3py.interfaces.routes import T3Route
from .exit import exit_route

route_catalog: List[T3Route] = [
    exit_route,
    auth_check_route
]