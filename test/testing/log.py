import logging
from contextlib import contextmanager
from typing import Optional


@contextmanager
def close_all_handlers(name: Optional[str] = None):
    try:
        yield
    finally:
        logger = logging.getLogger(name)
        for handler in logger.handlers:
            handler.close()
