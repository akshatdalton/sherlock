from sherlock.constants import CORRELATION_ID_NAME, PluginTypes
from sherlock.instrumentation import get_correlation_id
from sherlock.plugins.base_plugin import AbstractPlugin

try:
    from sentry_sdk import configure_scope
except ImportError:
    pass


class SentryPlugin(AbstractPlugin):
    plugin_name: PluginTypes = PluginTypes.SENTRY

    @staticmethod
    def add_correlation_id() -> None:
        with configure_scope() as scope:
            scope.set_tag(CORRELATION_ID_NAME, get_correlation_id())
