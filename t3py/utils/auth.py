import getpass
import sys
from dataclasses import dataclass
from typing import Optional, cast

import requests

from t3py.consts import BASE_URL, logger

from .http import get_request, post_request


@dataclass
class Credentials:
    hostname: str
    username: str
    password: str
    otp: Optional[str] = None
    

@dataclass
class APIAuthData:
    auth_mode: str
    has_t3_plus: bool
    username: str
    hostname: str
    access_token: str
    refresh_token: str

def obtain_api_auth_data_or_error(
    *, session: requests.Session, credentials: Credentials
) -> APIAuthData:
    """
    Obtain access token using provided credentials.
    """
    logger.info("Obtaining access token...")
    url = f"https://{credentials.hostname}/v2/auth/credentials"
    data = {
        "hostname": credentials.hostname,
        "username": credentials.username,
        "password": credentials.password,
    }
    if credentials.otp:
        data["otp"] = credentials.otp

    response = post_request(session=session, url=url, data=data)
    if response and "accessToken" in response:
        access_token = response["accessToken"]
        refresh_token = response["refreshToken"]
        
        logger.info("Retrieving identity...")
        url = f"{BASE_URL}/v2/auth/whoami"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        identity = get_request(session=session, url=url, headers=headers)
    
        if identity is None:
            raise ValueError("Identity cannot be None")

        return APIAuthData(
            auth_mode=cast(str, identity.get("authMode", "")),
            access_token=access_token,
            refresh_token=refresh_token,
            has_t3_plus=cast(bool, identity.get("hasT3Plus", False)),
            username=cast(str, identity.get("username", "")),
            hostname=cast(str, identity.get("hostname", ""))
        )

    raise Exception("Failed to obtain access token. Please check your credentials.")


def authenticate_or_error(*, hostname: str, username: str) -> APIAuthData:
    """
    Handle the authentication process with the T3 API.
    """
    password = getpass.getpass(prompt=f"Password for {hostname}/{username}: ")

    otp = None
    if hostname == "mi.metrc.com":
        otp = getpass.getpass(prompt="OTP: ")

    credentials = Credentials(
        hostname=hostname, username=username, password=password, otp=otp
    )

    with requests.Session() as session:
        api_auth_data = obtain_api_auth_data_or_error(session=session, credentials=credentials)
        if not api_auth_data:
            logger.error("Failed to authenticate.")
            sys.exit(1)
            
        return api_auth_data

