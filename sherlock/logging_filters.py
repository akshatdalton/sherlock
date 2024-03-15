from logging import Filter, LogRecord

from sherlock.instrumentation import get_correlation_id


class CorrelationIDFilter(Filter):
    """
    Filter to add correlation IDs to log records
    """

    def filter(self, record: LogRecord) -> bool:
        # TODO: If `get_correlation_id` returns `None`
        #  then generate unique value from `generator`.
        record.correlation_id = get_correlation_id()
        return True
