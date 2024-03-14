from contextvars import ContextVar
from typing import Dict
from uuid import uuid4

from sherlock.constants import CORRELATION_ID_NAME

correlation_id: ContextVar[str] = ContextVar("correlation_id", default=uuid4().hex)


def get_correlation_id_header(generate_new: bool = False) -> Dict[str, str]:
    """
    Returns Correlation ID header

    :param generate_new: If to generate new correlation ID
    :type generate_new: bool
    :return: Correlation ID Header
    :rtype: Dict[str, str]
    """
    if generate_new:
        set_correlation_id(uuid4().hex)
    return {CORRELATION_ID_NAME: correlation_id.get()}


def get_correlation_id() -> str:
    return correlation_id.get()


def set_correlation_id(value: str) -> None:
    correlation_id.set(value)
