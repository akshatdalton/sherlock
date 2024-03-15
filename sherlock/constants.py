from enum import Enum
from typing import Final

CORRELATION_ID_NAME: Final = "X-Correlation-ID"


class IntegrationTypes(str, Enum):
    FASTAPI: Final = "fastapi"
    HTTPX: Final = "httpx"
    REQUESTS: Final = "requests"


class PluginTypes(str, Enum):
    SENTRY: Final = "sentry-sdk"
