#!/usr/bin/env python3
"""
Command-line interface for FAB.
"""

import argparse
import sys
from .config import __version__, APP_DESCRIPTION
from .kickstart import handle_kickstart
from .whitelist import get_valid_commands


def main() -> int:
    """Main entry point for the fab CLI."""
    parser = argparse.ArgumentParser(
        description=APP_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fab --help                    Show this help message
  fab version                   Show version information
  fab kickstart file.ks         Execute a Kickstart file
  fab kickstart file.ks --dry-run  Validate a Kickstart file
  fab whitelist --list          List valid commands

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
    
    # Kickstart command
    kickstart_parser = subparsers.add_parser(
        'kickstart',
        help='Read and execute a Kickstart file'
    )
    kickstart_parser.add_argument(
        'file',
        help='Path to the Kickstart file'
    )
    kickstart_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and validate the Kickstart file without executing'
    )
    
    # Whitelist command
    whitelist_parser = subparsers.add_parser(
        'whitelist',
        help='Manage kickstart command whitelist'
    )
    whitelist_parser.add_argument(
        '--list',
        action='store_true',
        help='List all valid commands'
    )
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'version':
        print(f"fab version {__version__}")
        return 0
    
    elif args.command == 'kickstart':
        return handle_kickstart(args.file, args.dry_run)
    
    elif args.command == 'whitelist':
        if args.list:
            valid = get_valid_commands()
            print("Valid kickstart commands:")
            for cmd, desc in sorted(valid.items()):
                print(f"  {cmd:<20} - {desc}")
            return 0
        else:
            print("Use --list to see valid commands")
            return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 