from threading import RLock

import wrapt
from decorator import contextmanager

from telemetry.api import Telemetry, TelemetryMixin
from telemetry.api.decorator import trace, extract_args
from telemetry.api.metrics import Metrics
from telemetry.api.trace import Tracer, SpanKind, Span, SynchronousSpanTracker, SpanTracker, \
    ConcurrentSpanTracker, Attributes, AttributeValue

telemetry: Telemetry = wrapt.ObjectProxy(Telemetry())
tracer: Tracer = wrapt.ObjectProxy(telemetry.tracer)
metrics: Metrics = wrapt.ObjectProxy(telemetry.metrics)

_telemetry_lock = RLock()

def get_telemetry():
    return telemetry.__wrapped__

def set_telemetry(instance: Telemetry):
    """
    UNIT TEST ONLY!

    Replace current telemetry instance with a new instance.

    TODO: Add "test only" check to this method
    TODO: use a read-write lock instead

    :param instance: new Telemetry instance
    :return: None
    """
    with _telemetry_lock:
        telemetry.__wrapped__ = instance
        tracer.__wrapped__ = instance.tracer
        metrics.__wrapped__ = instance.metrics
        instance.register()

@contextmanager
def with_telemetry(telemetry: Telemetry) -> Telemetry:
    """
    UNIT TEST ONLY!

    Temporarily replace the Telementry instance with a new one within a context

    TODO: Add "test only" check to this method
    TODO: use a read-write lock
    :param instance: new Telemetry instance
    :return: new Telemetry instance
    """
    previous = get_telemetry()
    set_telemetry(telemetry)
    yield telemetry
    set_telemetry(previous)


def initialize_json_logger():
    """
    Registers the Json log formmater which with telemetry-aware logging that will include current attributes/tags in
    each log message.
    :return: None
    """
    import logging
    from telemetry.api.logger.json import JsonLogFormatter
    
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(JsonLogFormatter())




