from contextvars import ContextVar
from typing import Callable, Dict, Optional
from uuid import uuid4

from sherlock.constants import CORRELATION_ID_NAME

_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def _default_correlation_id_generator() -> Callable[[], str]:
    return lambda: uuid4().hex


correlation_id_generator: Callable[[], str] = _default_correlation_id_generator()


def get_correlation_id_header() -> Dict[str, str]:
    """
    Returns Correlation ID header.

    :return: Correlation ID Header
    :rtype: Dict[str, str]
    """
    if is_correlation_id_unset():
        set_correlation_id(correlation_id_generator())
    return {CORRELATION_ID_NAME: _correlation_id.get()}


def get_correlation_id() -> Optional[str]:
    return _correlation_id.get()


def set_correlation_id(value: str) -> None:
    _correlation_id.set(value)


def is_correlation_id_unset() -> bool:
    return get_correlation_id() is None


def set_correlation_id_generator(func: Optional[Callable[[], str]]) -> None:
    global correlation_id_generator
    if func is not None:
        correlation_id_generator = func
