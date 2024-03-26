from abc import ABC, abstractmethod
from typing import Any, Dict, MutableMapping, Tuple

import wrapt

from sherlock import set_correlation_id
from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header


class AbstractIntegration(ABC):
    """
    Abstract class to implement integration for a library.
    This integration's job is to essentially patch the old
    method with the new defined method.

    In this package, it will be used to propagate correlation ID
    in request and response headers.

    You can use auxiliary function `update_request_headers` and
    `update_response_headers` function to update request and response
    headers.

    Patch is finally applied when `add_patch` of the abstract class
    is called.
    """

    @abstractmethod
    def __init__(self, module_path: str, func_name: str) -> None:
        self._module_path = module_path
        self._func_name = func_name

    @property
    @abstractmethod
    def integration_type(self) -> IntegrationTypes:
        """
        Returns integration types.
        """
        pass

    @abstractmethod
    def extract_request_headers(self, *args, **kwargs) -> MutableMapping:
        # may be, convert all args to kwargs
        pass

    @abstractmethod
    def update_args_and_kwargs_with_request_headers(
        self, request_headers: MutableMapping, *args, **kwargs
    ) -> Tuple[Tuple, Dict]:
        pass

    @abstractmethod
    def extract_response_headers(self, response: Any) -> MutableMapping:
        pass

    @abstractmethod
    def update_response_with_response_headers(
        self, response_headers: MutableMapping, response: Any
    ) -> Any:
        pass

    def add_patch(self) -> None:
        wrapt.wrap_function_wrapper(
            self._module_path, self._func_name, self._patched_func
        )

    def _patched_func(self, wrapped, instance, args, kwargs) -> Any:
        request_headers = self.extract_request_headers(*args, **kwargs)
        if old_correlation_id := request_headers.get(CORRELATION_ID_NAME, None):
            set_correlation_id(old_correlation_id)
        elif old_correlation_id := request_headers.get(
            CORRELATION_ID_NAME.lower(), None
        ):
            set_correlation_id(old_correlation_id)

        correlation_id_header = get_correlation_id_header()
        request_headers.update(correlation_id_header)
        new_args, new_kwargs = self.update_args_and_kwargs_with_request_headers(
            request_headers, *args, **kwargs
        )

        response = wrapped(*new_args, **new_kwargs)
        response_headers = self.extract_response_headers(response)
        if CORRELATION_ID_NAME not in response_headers:
            response_headers.update(correlation_id_header)

        new_response = self.update_response_with_response_headers(
            response_headers, response
        )
        return new_response
