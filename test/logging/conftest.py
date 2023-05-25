import pytest

from ditk import logging


@pytest.fixture(scope='module', autouse=True)
def init_logging_level():
    logging.try_init_root(logging.WARNING)
