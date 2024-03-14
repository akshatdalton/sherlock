from logging import Filter, LogRecord

from sherlock.instrumentation import get_correlation_id


class CorrelationIDFilter(Filter):
    """
    Filter to add correlation IDs to log records
    """

    def filter(self, record: LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        return True
