from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header, set_correlation_id
from sherlock.integrations.integration import AbstractIntegration

try:
    from requests import PreparedRequest, Session
except ImportError:
    pass


class RequestsIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.REQUESTS

    def __init__(self) -> None:
        old_send = Session.send

        def new_send(_self, request: PreparedRequest, **kwargs):
            old_correlation_id = request.headers.get(CORRELATION_ID_NAME, None)
            if old_correlation_id is not None:
                set_correlation_id(old_correlation_id)

            correlation_id_header = get_correlation_id_header()
            request.prepare_headers(correlation_id_header)

            response = old_send(_self, request, **kwargs)
            response.headers.update(correlation_id_header)
            return response

        self.new_send = new_send

    def add_patch(self) -> None:
        Session.send = self.new_send
