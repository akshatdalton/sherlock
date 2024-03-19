from typing import Any, Dict, MutableMapping, Tuple

from sherlock.constants import IntegrationTypes
from sherlock.integrations.integration import AbstractIntegration


class RequestsIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.REQUESTS

    def __init__(self):
        module_path, func_name = "requests", "Session.send"
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        request = args[0]
        return request.headers

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        request = args[0]
        request.headers.update(request_headers)
        new_args = (request,) + args[1:]
        return new_args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        return response.headers

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        response.headers.update(response_headers)
        return response
