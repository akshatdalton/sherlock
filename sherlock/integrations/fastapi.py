from typing import Any, Dict, Tuple

import wrapt

from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header, set_correlation_id
from sherlock.integrations.integration import AbstractIntegration
from sherlock.utils import logger

try:
    from starlette.datastructures import MutableHeaders
except ImportError:
    pass


class FastAPIIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.FASTAPI

    def __init__(self):
        module_path, func_name = "fastapi", "routing.get_request_handler"
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> "MutableHeaders":
        request = args[0]
        headers = request.headers
        return headers.mutablecopy()

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: "MutableHeaders", *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        request = args[0]
        request.scope["headers"] = request_headers.raw
        new_args = (request,) + args[1:]
        return new_args, kwargs

    def extract_response_headers(self, response: Any) -> "MutableHeaders":
        return response.headers

    def update_response_with_response_headers(
        self, response_headers: "MutableHeaders", response: Any
    ) -> Any:
        response.raw_headers = response_headers.raw
        response._headers = response_headers
        return response

    def _patched_func(self, wrapped, instance, args, kwargs) -> Any:
        app = wrapped(*args, **kwargs)
        new_app = self._app_patcher(app)
        return new_app

    @wrapt.decorator
    async def _app_patcher(self, wrapped, instance, args, kwargs):
        try:
            request_headers = self.extract_request_headers(*args, **kwargs)
            if old_correlation_id := request_headers.get(CORRELATION_ID_NAME, None):
                set_correlation_id(old_correlation_id)

            correlation_id_header = get_correlation_id_header()
            request_headers.update(correlation_id_header)
            args, kwargs = self.update_args_and_kwargs_with_request_headers(
                request_headers, *args, **kwargs
            )
        except Exception as e:
            correlation_id_header = {}
            logger.warn(
                "Failed to extract request headers for function: %s, received error: %s",
                wrapped.__name__,
                str(e),
            )

        response = await wrapped(*args, **kwargs)

        try:
            response_headers = self.extract_response_headers(response)
            if CORRELATION_ID_NAME not in response_headers:
                response_headers.update(correlation_id_header)

            response = self.update_response_with_response_headers(
                response_headers, response
            )
        except Exception as e:
            logger.warn(
                "Failed to extract response headers for function: %s, received error: %s",
                wrapped.__name__,
                str(e),
            )

        return response
