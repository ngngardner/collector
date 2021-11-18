"""Global console module."""

from rich.console import Console


def init() -> Console:
    """Initialize logging.

    Returns:
        Console: Console object.
    """
    return Console()


console = init()
