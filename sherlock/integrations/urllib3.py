from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import (
    get_correlation_id,
    get_correlation_id_header,
    set_correlation_id,
)
from sherlock.integrations.integration import AbstractIntegration

try:
    from urllib3 import HTTPConnectionPool
except ImportError:
    pass


class Urllib3Integration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.URLLIB3

    def __init__(self) -> None:
        old_send = HTTPConnectionPool.urlopen

        def new_urlopen(*args, **kwargs):
            header_in_kwargs = True
            request_header = kwargs.get("headers", None)
            if request_header is None:
                if len(args) >= 4:
                    request_header = args[4]
                    header_in_kwargs = False
                else:
                    request_header = {}

            old_correlation_id = request_header.get(CORRELATION_ID_NAME, None)
            if old_correlation_id is not None:
                set_correlation_id(old_correlation_id)

            correlation_id_header = get_correlation_id_header()
            request_header.update(correlation_id_header)

            if header_in_kwargs:
                kwargs["headers"] = request_header
            else:
                updated_args = args[:4] + (request_header,) + args[5:]
                args = updated_args

            response = old_send(*args, **kwargs)
            if CORRELATION_ID_NAME not in response.headers:
                response.headers.add(CORRELATION_ID_NAME, get_correlation_id())
            return response

        self.new_send = new_urlopen

    def add_patch(self) -> None:
        HTTPConnectionPool.urlopen = self.new_send
