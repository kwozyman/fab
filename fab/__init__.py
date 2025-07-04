"""
FAB - Fast Assembler for BootC

A command-line interface tool for assembling BootC code.
"""

# Version information
__version__ = "0.1.0"

# Import main function for easy access
from .cli import main

__all__ = ["main", "__version__"]
