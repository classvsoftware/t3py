

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Credentials:
    hostname: str
    username: str
    password: str
    otp: Optional[str] = None


@dataclass(frozen=True)
class APIAuthData:
    auth_mode: str
    has_t3_plus: bool
    username: str
    hostname: str
    access_token: str
    refresh_token: str