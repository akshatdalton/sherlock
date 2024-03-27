from typing import Any, Dict, MutableMapping, Tuple

from sherlock.constants import IntegrationTypes
from sherlock.integrations.integration import AbstractIntegration


class HttpxIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.HTTPX

    def __init__(self):
        module_path, func_name = "httpx", "Client.send"
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        request = kwargs["request"]
        return request.headers

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        request = kwargs["request"]
        request.headers.update(request_headers)
        kwargs["request"] = request
        return args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        return response.headers

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        response.headers.update(response_headers)
        return response
