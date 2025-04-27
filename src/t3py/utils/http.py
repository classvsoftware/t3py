from typing import Dict

import httpx

from t3py.consts.http import BASE_URL, TIMEOUT_S, logger


def post_request(
    *, session: httpx.Client, headers: Dict[str, str], url: str, data: Dict
) -> httpx.Response:
    """
    Make a POST request and return the response.
    """
    response = session.post(url=url, headers=headers, json=data, timeout=TIMEOUT_S)
    response.raise_for_status()
    return response


def get_request(
    *, session: httpx.Client, url: str, headers: Dict[str, str]
) -> httpx.Response:
    """
    Make a GET request and return the response.
    """
    response = session.get(url=url, headers=headers, timeout=TIMEOUT_S)
    response.raise_for_status()
    return response
