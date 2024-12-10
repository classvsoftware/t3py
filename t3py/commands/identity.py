
from t3py.consts import logger
from t3py.utils.auth import APIAuthData


def check_identity(api_auth_data: APIAuthData):
    logger.info("You successfully authenticated with the T3 API")
    logger.info(
        f"The username '{api_auth_data.username}' {'is registered as a T3+ username and can use all API endpoints' if api_auth_data.has_t3_plus else 'is not registered and can only access free endpoints.'}"
    )
    logger.info("T3 API docs can be found at https://trackandtrace.tools/api")
