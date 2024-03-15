from contextvars import ContextVar
from typing import Dict, Optional
from uuid import uuid4

from sherlock.constants import CORRELATION_ID_NAME

_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def get_correlation_id_header() -> Dict[str, str]:
    """
    Returns Correlation ID header.

    :return: Correlation ID Header
    :rtype: Dict[str, str]
    """
    if is_correlation_id_unset():
        set_correlation_id(uuid4().hex)
    return {CORRELATION_ID_NAME: _correlation_id.get()}


def get_correlation_id() -> Optional[str]:
    return _correlation_id.get()


def set_correlation_id(value: str) -> None:
    _correlation_id.set(value)


def is_correlation_id_unset() -> bool:
    return get_correlation_id() is None
