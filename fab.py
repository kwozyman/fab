#!/usr/bin/env python3
"""
FAB - Fast Assembler for BootC

A command-line interface tool for assembling BootC containers.
"""

import argparse
import sys
from typing import Optional

# Version information
__version__ = "0.1.0"


def main() -> int:
    """Main entry point for the fab CLI."""
    parser = argparse.ArgumentParser(
        description="FAB - Fast Assembler for BootC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fab --help                    Show this help message
  fab version                   Show version information
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'fab {__version__}'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Version command
    version_parser = subparsers.add_parser(
        'version',
        help='Show version information'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'version':
        print(f"fab version {__version__}")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 