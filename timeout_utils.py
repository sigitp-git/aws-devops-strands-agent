#!/usr/bin/env python3
"""
Timeout utilities for AWS DevOps agent.
"""

import signal
import functools
from typing import Callable, Any, TypeVar, Optional
from contextlib import contextmanager

T = TypeVar('T')


class TimeoutError(Exception):
    """Raised when an operation times out."""
    pass


@contextmanager
def timeout_context(timeout_seconds: int, message: str = "Operation timed out"):
    """
    Context manager for timeout operations.
    
    Args:
        timeout_seconds: Timeout in seconds
        message: Error message for timeout
        
    Raises:
        TimeoutError: If operation times out
    """
    def timeout_handler(signum, frame):
        raise TimeoutError(message)
    
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)
        if old_handler is not None:
            try:
                signal.signal(signal.SIGALRM, old_handler)
            except (OSError, ValueError):
                pass  # Ignore cleanup errors


def timeout_decorator(timeout_seconds: int, message: Optional[str] = None):
    """
    Decorator to add timeout to functions.
    
    Args:
        timeout_seconds: Timeout in seconds
        message: Optional custom timeout message
        
    Returns:
        Decorated function that raises TimeoutError on timeout
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            timeout_msg = message or f"{func.__name__} timed out after {timeout_seconds} seconds"
            with timeout_context(timeout_seconds, timeout_msg):
                return func(*args, **kwargs)
        return wrapper
    return decorator