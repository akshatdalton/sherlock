from typing import Any, Dict, MutableMapping, Tuple

import wrapt

from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header, set_correlation_id
from sherlock.integrations.integration import AbstractIntegration


class FastAPIIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.FASTAPI

    def __init__(self):
        module_path, func_name = "fastapi", "routing.get_request_handler"
        super().__init__(module_path=module_path, func_name=func_name)

    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        request = args[0]
        headers = dict(request.scope["headers"])
        return headers

    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        request = args[0]
        request.scope["headers"] = [(k, v) for k, v in request_headers.items()]
        new_args = (request,) + args[1:]
        return new_args, kwargs

    def extract_response_headers(self, response: Any) -> MutableMapping:
        pass

    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        pass

    def _patched_func(self, wrapped, instance, args, kwargs) -> Any:
        app = wrapped(*args, **kwargs)
        new_app = self._app_patcher(app)
        return new_app

    @wrapt.decorator
    async def _app_patcher(self, wrapped, instance, args, kwargs):
        request_headers = self.extract_request_headers(*args, **kwargs)
        if old_correlation_id := request_headers.get(CORRELATION_ID_NAME.lower(), None):
            set_correlation_id(old_correlation_id)

        correlation_id_header = get_correlation_id_header()
        request_headers.update(correlation_id_header)
        new_args, new_kwargs = self.update_args_and_kwargs_with_request_headers(
            request_headers, *args, **kwargs
        )
        return await wrapped(*new_args, **new_kwargs)
