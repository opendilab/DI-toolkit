"""
Distributed training utilities for PyTorch.

This module provides utility functions to handle distributed training scenarios in PyTorch.
It offers convenient methods to check distributed status, get process information, and
determine the main process. The functions gracefully handle both distributed and
non-distributed environments.

Example::
    >>> # Check if distributed training is active
    >>> if is_distributed():
    ...     print(f"Running on rank {get_rank()} of {get_world_size()}")
    >>> 
    >>> # Execute code only on main process
    >>> if is_main_process():
    ...     print("This runs only on the main process")
"""


def is_distributed() -> bool:
    """
    Check if distributed training is available and initialized.

    This function verifies whether PyTorch distributed training is both available
    (compiled with distributed support) and properly initialized. It handles cases
    where PyTorch or its distributed module might not be installed.

    :return: True if distributed training is available and initialized, False otherwise.
    :rtype: bool

    Example::
        >>> if is_distributed():
        ...     print("Distributed training is active")
        ... else:
        ...     print("Running in single-process mode")
    """
    try:
        import torch
        import torch.distributed as dist
    except (ImportError, ModuleNotFoundError):
        return False

    # Check if distributed is available (compiled with distributed support) and is initialized
    return dist.is_available() and dist.is_initialized()


def get_rank() -> int:
    """
    Get the global rank of the current process.

    Returns the global rank (process ID) of the current process in distributed training.
    In non-distributed environments, this function returns 0, making it safe to use
    in both distributed and single-process scenarios.

    :return: Global rank of the current process. Returns 0 if distributed training is not active.
    :rtype: int

    Example::
        >>> rank = get_rank()
        >>> print(f"Current process rank: {rank}")
    """
    if is_distributed():
        import torch.distributed as dist
        return dist.get_rank()
    else:
        return 0


def get_world_size() -> int:
    """
    Get the total number of processes across all nodes.

    Returns the total number of processes participating in distributed training.
    In non-distributed environments, this function returns 1, ensuring consistent
    behavior across different training setups.

    :return: Total number of processes in the distributed training. Returns 1 if distributed training is not active.
    :rtype: int

    Example::
        >>> world_size = get_world_size()
        >>> print(f"Total number of processes: {world_size}")
    """
    if is_distributed():
        import torch.distributed as dist
        return dist.get_world_size()
    else:
        return 1


# Utility functions for easier usage
def is_main_process() -> bool:
    """
    Check if the current process is the main process (global rank 0).

    This function is useful for executing code that should only run once across
    all processes, such as logging, saving checkpoints, or printing progress.
    In non-distributed environments, it always returns True.

    :return: True if current process is main process (rank 0) or if distributed is not available.
    :rtype: bool

    Example::
        >>> if is_main_process():
        ...     print("Saving model checkpoint...")
        ...     # Save checkpoint logic here
    """
    if not is_distributed():
        return True
    return get_rank() == 0
