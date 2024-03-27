import inspect
from typing import Any, Dict, MutableMapping, Tuple

from sherlock.constants import IntegrationTypes
from sherlock.integrations.integration import AbstractIntegration


class Urllib3Integration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.URLLIB3

    def __init__(self):
        module_path, func_name = "urllib3", "HTTPConnectionPool.urlopen"
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        return kwargs.get("headers", {})

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        kwargs["headers"] = request_headers
        return args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        return response.headers

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        response.headers.update(response_headers)
        return response

    def _patched_func(self, wrapped, instance, args, kwargs) -> Any:
        args_converted_to_kwargs = self._convert_args_to_kwargs(args, wrapped)
        kwargs.update(args_converted_to_kwargs)
        args = ()
        return super()._patched_func(wrapped, instance, args, kwargs)

    @staticmethod
    def _convert_args_to_kwargs(args, func):
        func_signature = inspect.signature(func)
        param_names = [param.name for param in func_signature.parameters.values()]
        return {param_names[i]: arg for i, arg in enumerate(args)}
