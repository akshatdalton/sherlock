from sherlock.constants import CORRELATION_ID_NAME, IntegrationTypes
from sherlock.instrumentation import get_correlation_id_header, set_correlation_id
from sherlock.integrations.integration import AbstractIntegration

try:
    import fastapi
except ImportError:
    pass


class FastAPIIntegration(AbstractIntegration):
    integration_type: IntegrationTypes = IntegrationTypes.FASTAPI

    def __init__(self) -> None:
        old_get_request_handler = fastapi.routing.get_request_handler

        def new_get_request_handler(*args, **kwargs):
            old_app = old_get_request_handler(*args, **kwargs)

            async def new_app(*args, **kwargs):
                request = args[0]
                headers = dict(request.scope["headers"])
                old_correlation_id = headers.get(CORRELATION_ID_NAME)
                if old_correlation_id is not None:
                    set_correlation_id(old_correlation_id)

                correlation_id_header = get_correlation_id_header()
                headers.update(correlation_id_header)
                request.scope["headers"] = [(k, v) for k, v in headers.items()]

                # FastAPI auto-sets the correlation id header in response from request.
                return await old_app(*args, **kwargs)

            return new_app

        self.new_send = new_get_request_handler

    def add_patch(self) -> None:
        fastapi.routing.get_request_handler = self.new_send
