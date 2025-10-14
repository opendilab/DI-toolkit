"""
Stream logging handlers module for distributed and rich text environments.

This module provides custom logging handlers and utilities for creating stream-based
loggers that work well in distributed computing environments and handle rich text markup.
It includes functionality for stripping rich markup from log messages and formatting
log output with distributed system information.
"""

import logging
import os
import sys
from logging import StreamHandler, LogRecord
from typing import Optional

from rich.markup import render

from .base import _LogLevelType
from ..distributed import is_distributed, get_rank, get_world_size

_STREAM_FMT = logging.Formatter(
    fmt='[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s',
    datefmt="%m-%d %H:%M:%S",
)


def _strip_rich_markup(text: str) -> str:
    """
    Strip rich markup from text and return plain text.

    :param text: The text containing rich markup to be stripped.
    :type text: str

    :return: Plain text with all rich markup removed.
    :rtype: str

    Example::

        >>> _strip_rich_markup("[bold red]Error message[/bold red]")
        'Error message'
    """
    return render(text).plain


class NoRichStreamHandler(StreamHandler):
    """
    A custom StreamHandler that strips rich markup from log messages.

    This handler extends the standard logging StreamHandler to automatically
    remove rich text markup from log messages before emitting them. This is
    useful when you want to log to streams that don't support rich formatting.
    """

    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record, stripping rich markup from the message if it's a string.

        :param record: The log record to emit.
        :type record: LogRecord

        :return: None
        :rtype: None
        """
        if isinstance(record.msg, str):
            record.msg = _strip_rich_markup(record.msg)
        super().emit(record)


def _get_log_format(
        include_distributed: bool = True,
        distributed_format: str = "[Rank {rank}/{world_size}][PID: {pid}]"
) -> str:
    """
    Generate a log format string with optional distributed system information.

    This function creates a log format string that includes timestamp, filename,
    line number, and log level. When running in a distributed environment and
    include_distributed is True, it also adds rank and world size information.

    :param include_distributed: Whether to include distributed system information in the format.
    :type include_distributed: bool

    :param distributed_format: Format string for distributed information containing {rank} and {world_size} placeholders.
    :type distributed_format: str

    :return: The formatted log format string.
    :rtype: str

    Example::

        >>> _get_log_format(include_distributed=False)
        '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
    """
    if include_distributed and is_distributed():
        rank = get_rank()
        world_size = get_world_size()
        prefix = distributed_format.format(rank=rank, world_size=world_size, pid=os.getpid())
        return f"[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]{prefix} %(message)s"
    else:
        return f"[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s"


def _create_stream_handler(
        use_stdout: bool = False,
        level: _LogLevelType = logging.NOTSET,
        include_distributed: bool = True,
        distributed_format: Optional[str] = None,
) -> StreamHandler:
    """
    Create a configured stream handler for logging.

    This function creates a NoRichStreamHandler with appropriate formatting
    for both single-node and distributed environments. The handler strips
    rich markup from messages and can include distributed system information.

    :param use_stdout: If True, use stdout; otherwise use stderr for output.
    :type use_stdout: bool

    :param level: The logging level for the handler.
    :type level: _LogLevelType

    :param include_distributed: Whether to include distributed system information in log format.
    :type include_distributed: bool

    :param distributed_format: Custom format string for distributed information. If None, uses default format.
    :type distributed_format: Optional[str]

    :return: Configured stream handler ready for use.
    :rtype: StreamHandler

    Example::

        >>> handler = _create_stream_handler(use_stdout=True, level=logging.INFO)
        >>> logger = logging.getLogger('my_logger')
        >>> logger.addHandler(handler)
    """
    handler = NoRichStreamHandler(sys.stdout if use_stdout else sys.stderr)
    handler.setFormatter(logging.Formatter(
        fmt=_get_log_format(
            include_distributed=include_distributed,
            distributed_format=distributed_format or "[Rank {rank}/{world_size}][PID: {pid}]",
        ),
        datefmt="%m-%d %H:%M:%S",
    ))
    handler.setLevel(level)
    return handler
