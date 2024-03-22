from typing import Any, Dict, MutableMapping, Tuple

from sherlock.constants import IntegrationTypes
from sherlock.integrations.integration import AbstractIntegration


class Urllib3Integration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.URLLIB3

    def __init__(self):
        module_path, func_name = "urllib3", "HTTPConnectionPool.urlopen"
        self._header_in_kwargs = True
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        self._header_in_kwargs = True
        request_header = kwargs.get("headers", None)
        if request_header is None:
            if len(args) >= 4:
                request_header = args[4]
                self._header_in_kwargs = False
            else:
                request_header = {}
        return request_header

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        if self._header_in_kwargs:
            kwargs["headers"].update(request_headers)
        else:
            updated_args = args[:4] + (request_headers,) + args[5:]
            args = updated_args
        return args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        return response.headers

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        response.headers.update(response_headers)
        return response
