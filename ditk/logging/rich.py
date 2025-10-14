"""
Rich logging utilities for distributed training environments.

This module provides enhanced logging capabilities using the Rich library,
with special support for distributed training scenarios. It includes utilities
for creating properly formatted console outputs with terminal width detection,
distributed rank information, and rich text formatting.

The module automatically detects distributed training environments and can
include rank information in log messages to help distinguish between different
processes in multi-GPU or multi-node training setups.
"""

import logging
import os
import shutil
from functools import lru_cache
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

import ditk
from .base import _LogLevelType
from ..distributed import is_distributed, get_rank, get_world_size

# This value is set due the requirement of displaying the tables
_DEFAULT_WIDTH = 170


@lru_cache()
def _get_terminal_width() -> int:
    """
    Get the current terminal width with caching for performance.

    This function detects the terminal width and caches the result to avoid
    repeated system calls. It falls back to a default width if terminal
    size detection fails.

    :return: The terminal width in characters.
    :rtype: int

    Example::
        >>> width = _get_terminal_width()
        >>> print(f"Terminal width: {width}")
        Terminal width: 170
    """
    width, _ = shutil.get_terminal_size(fallback=(_DEFAULT_WIDTH, 24))
    return width


@lru_cache()
def _get_rich_console(use_stdout: bool = False) -> Console:
    """
    Create and cache a Rich Console instance with appropriate configuration.

    This function creates a Rich Console with the detected terminal width
    and configures output to stderr by default (or stdout if specified).
    The result is cached to ensure consistent console usage across the application.

    :param use_stdout: Whether to use stdout instead of stderr for output.
    :type use_stdout: bool

    :return: A configured Rich Console instance.
    :rtype: Console

    Example::
        >>> console = _get_rich_console()
        >>> console.print("Hello, World!")
        Hello, World!
    """
    return Console(width=_get_terminal_width(), stderr=not use_stdout)


def _get_log_format(
        include_distributed: bool = True,
        distributed_format: str = "[Rank {rank}/{world_size}][PID: {pid}]"
) -> str:
    """
    Get the appropriate log format based on distributed training status.

    This function generates a logging format string that optionally includes
    distributed training information such as rank and world size. When
    distributed training is detected and enabled, it prepends rank information
    to log messages to help identify which process generated each log entry.

    :param include_distributed: Whether to include distributed information in the format.
    :type include_distributed: bool
    :param distributed_format: Format string template for distributed info, should contain
                              {rank} and {world_size} placeholders.
    :type distributed_format: str

    :return: Format string for logging that includes distributed info if applicable.
    :rtype: str

    Example::
        >>> # In a distributed environment
        >>> format_str = _get_log_format(include_distributed=True)
        >>> print(format_str)
        [Rank 0/4] %(message)s

        >>> # Without distributed info
        >>> format_str = _get_log_format(include_distributed=False)
        >>> print(format_str)
        %(message)s
    """
    if include_distributed and is_distributed():
        rank = get_rank()
        world_size = get_world_size()
        prefix = distributed_format.format(rank=rank, world_size=world_size, pid=os.getpid())
        return f"{prefix} %(message)s"
    else:
        return "%(message)s"


def _create_rich_handler(
        use_stdout: bool = False,
        level: _LogLevelType = logging.NOTSET,
        include_distributed: bool = True,
        distributed_format: Optional[str] = None
) -> RichHandler:
    """
    Create a Rich handler with optional distributed training information.

    This function creates a fully configured RichHandler that provides
    enhanced logging output with rich text formatting, traceback highlighting,
    and optional distributed training rank information. The handler is
    configured with appropriate formatters and console settings.

    :param use_stdout: Whether to use stdout instead of stderr for log output.
    :type use_stdout: bool
    :param level: Logging level threshold for this handler.
    :type level: _LogLevelType
    :param include_distributed: Whether to include distributed rank information
                               in log messages when running in distributed mode.
    :type include_distributed: bool
    :param distributed_format: Custom format template for distributed info.
                              If None, uses a default Rich markup format with
                              bold blue styling. Should contain {rank} and
                              {world_size} placeholders.
    :type distributed_format: Optional[str]

    :return: A configured RichHandler instance ready for use with Python logging.
    :rtype: RichHandler

    Example::
        >>> # Create a basic rich handler
        >>> handler = _create_rich_handler()
        >>> logger = logging.getLogger("my_logger")
        >>> logger.addHandler(handler)
        >>> logger.info("This will be beautifully formatted!")

        >>> # Create handler with custom distributed format
        >>> handler = _create_rich_handler(
        ...     distributed_format="[Process {rank}]",
        ...     level=logging.INFO
        ... )
    """
    if distributed_format is None:
        distributed_format = "[bold blue]\\[Rank {rank}/{world_size}][/bold blue][bold blue]\\[PID: {pid}][/bold blue]"  # Rich markup support

    # Dynamically create formatter with distributed information
    rich_fmt = logging.Formatter(
        fmt=_get_log_format(include_distributed, distributed_format),
        datefmt="[%m-%d %H:%M:%S]"
    )

    handler = RichHandler(
        level=level,
        console=_get_rich_console(use_stdout),
        rich_tracebacks=True,
        markup=True,
        tracebacks_suppress=[ditk],
    )
    handler.setFormatter(rich_fmt)
    return handler
