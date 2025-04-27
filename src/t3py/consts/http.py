import logging

# Constants
BASE_URL = "https://api.trackandtrace.tools"
TIMEOUT_S = 20

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)