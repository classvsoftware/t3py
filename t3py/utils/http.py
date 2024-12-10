import requests
from typing import Dict, Optional
from t3py.consts import BASE_URL, TIMEOUT_S, logger


def post_request(*, session: requests.Session, url: str, data: Dict) -> Optional[Dict]:
    """
    Make a POST request and return the JSON response, or None on failure.
    """
    try:
        response = session.post(url=url, json=data, timeout=TIMEOUT_S)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"POST request failed: {e}")
        return None


def get_request(*, session: requests.Session, url: str, headers: Dict[str, str]) -> Optional[Dict]:
    """
    Make a GET request and return the JSON response, or None on failure.
    """
    try:
        response = session.get(url=url, headers=headers, timeout=TIMEOUT_S)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GET request failed: {e}")
        return None
