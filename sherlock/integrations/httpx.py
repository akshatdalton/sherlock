from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header, set_correlation_id
from sherlock.integrations.integration import AbstractIntegration

try:
    from httpx import Client, Request, Response
except ImportError:
    pass


class HttpxIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.HTTPX

    def __init__(self) -> None:
        old_send = Client.send

        def new_send(_self, request: Request, **kwargs) -> Response:
            old_correlation_id = request.headers.get(CORRELATION_ID_NAME, None)
            if old_correlation_id is not None:
                set_correlation_id(old_correlation_id)

            correlation_id_header = get_correlation_id_header()
            request.headers.update(correlation_id_header)

            response: Response = old_send(_self, request, **kwargs)
            response.headers.update(correlation_id_header)
            return response

        self.new_send = new_send

    def add_patch(self) -> None:
        Client.send = self.new_send
