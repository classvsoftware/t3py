from typing import Dict, Optional

import requests

from t3py.consts import BASE_URL, TIMEOUT_S, logger


def post_request(*, session: requests.Session, headers: Dict[str, str], url: str, data: Dict) -> requests.Response:
    """
    Make a POST request and return the response.
    """
    response = session.post(url=url, headers=headers, json=data, timeout=TIMEOUT_S)
    response.raise_for_status()
    return response


def get_request(*, session: requests.Session, url: str, headers: Dict[str, str]) -> requests.Response:
    """
    Make a GET request and return the response.
    """
    response = session.get(url=url, headers=headers, timeout=TIMEOUT_S)
    response.raise_for_status()
    return response
