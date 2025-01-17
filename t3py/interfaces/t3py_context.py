from dataclasses import dataclass
from typing import TypedDict

from t3py.interfaces.auth import APIAuthData

@dataclass
class T3pyContext():
    api_auth_data: APIAuthData