#!/usr/bin/env python3
"""
FAB - Fast Assembler for BootC

A command-line interface tool for assembling BootC containers.
"""

import argparse
import sys
import os
from typing import Optional

# Version information
__version__ = "0.1.0"


def handle_kickstart(file_path: str, dry_run: bool = False) -> int:
    """Handle kickstart command execution."""
    try:
        # Import pykickstart here to avoid import errors if not installed
        from pykickstart.parser import KickstartParser
        from pykickstart.handlers.f40 import F40Handler as Handler
        from pykickstart.errors import KickstartError
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: Kickstart file '{file_path}' not found.")
            return 1
        
        # Parse the kickstart file
        handler = Handler()
        parser = KickstartParser(handler)
        with open(file_path, 'r') as f:
            content = f.read()
        
        try:
            parser.readKickstartFromString(content)
            print(f"Successfully parsed Kickstart file: {file_path}")
            
            if dry_run:
                print("Dry run mode: Kickstart file is valid and ready for execution.")
                return 0
            
            # Here you would implement the actual execution logic
            # For now, we'll just print what we found
            print("Kickstart file contents:")
            print(f"  Language: {parser.handler.lang.lang}")
            print(f"  Keyboard: {parser.handler.keyboard.keyboard}")
            print(f"  Network: {len(parser.handler.network.network)} network(s) configured")
            print(f"  Packages: {len(parser.handler.packages.packageList)} packages selected")
            
            return 0
            
        except KickstartError as e:
            print(f"Error parsing Kickstart file: {e}")
            return 1
            
    except ImportError:
        print("Error: pykickstart library is not installed.")
        print("Install it with: pip install pykickstart")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


def main() -> int:
    """Main entry point for the fab CLI."""
    parser = argparse.ArgumentParser(
        description="FAB - Fast Assembler for BootC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fab --help                    Show this help message
  fab version                   Show version information
  fab kickstart file.ks         Execute a Kickstart file
  fab kickstart file.ks --dry-run  Validate a Kickstart file
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
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'version':
        print(f"fab version {__version__}")
        return 0
    
    elif args.command == 'kickstart':
        return handle_kickstart(args.file, args.dry_run)
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 