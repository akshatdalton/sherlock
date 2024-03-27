from typing import Any, Dict, MutableMapping, Tuple

from sherlock.constants import IntegrationTypes
from sherlock.integrations.integration import AbstractIntegration


class AWSLambdaIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.AWS_LAMBDA

    def __init__(self, module_path: str, func_name: str) -> None:
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        event = kwargs["event"]
        request_header = event.get("headers", {})
        return request_header

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        event = kwargs["event"]
        event["headers"] = request_headers
        kwargs["event"] = event
        return args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        response_headers = response.get("headers", {})
        return response_headers

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        response["headers"] = response_headers
        return response
