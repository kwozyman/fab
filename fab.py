#!/usr/bin/env python3
"""
FAB - Fast Assembler for BootC

A command-line interface tool for assembling BootC containers.
"""

import argparse
import sys
import os
import platform
from typing import Optional

# Version information
__version__ = "0.1.0"


def detect_os_handler():
    """Detect the operating system and return the appropriate handler class."""
    try:
        # Try to read /etc/os-release for Linux distribution info
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                os_info = dict(line.strip().split('=', 1) for line in f if '=' in line)
            
            distro_id = os_info.get('ID', '').lower()
            distro_version = os_info.get('VERSION_ID', '').strip('"')
            
            # Map common distributions to handlers
            if distro_id == 'fedora':
                # Try to use the version-specific handler, fallback to latest
                try:
                    version_num = int(distro_version.split('.')[0])
                    if version_num >= 40:
                        from pykickstart.handlers.f40 import F40Handler
                        return F40Handler
                    elif version_num >= 39:
                        from pykickstart.handlers.f39 import F39Handler
                        return F39Handler
                    elif version_num >= 38:
                        from pykickstart.handlers.f38 import F38Handler
                        return F38Handler
                    else:
                        # Fallback to latest available
                        from pykickstart.handlers.f40 import F40Handler
                        return F40Handler
                except (ValueError, ImportError):
                    # Fallback to latest available
                    from pykickstart.handlers.f40 import F40Handler
                    return F40Handler
            
            elif distro_id in ['rhel', 'centos', 'rocky', 'alma']:
                # Try to use the version-specific handler, fallback to latest
                try:
                    version_num = int(distro_version.split('.')[0])
                    if version_num >= 10:
                        from pykickstart.handlers.rhel10 import RHEL10Handler
                        return RHEL10Handler
                    elif version_num >= 9:
                        from pykickstart.handlers.rhel9 import RHEL9Handler
                        return RHEL9Handler
                    elif version_num >= 8:
                        from pykickstart.handlers.rhel8 import RHEL8Handler
                        return RHEL8Handler
                    else:
                        # Fallback to latest available
                        from pykickstart.handlers.rhel10 import RHEL10Handler
                        return RHEL10Handler
                except (ValueError, ImportError):
                    # Fallback to latest available
                    from pykickstart.handlers.rhel10 import RHEL10Handler
                    return RHEL10Handler
        
        # Fallback to platform detection
        system = platform.system().lower()
        if system == 'linux':
            # Default to Fedora 40 handler for Linux
            from pykickstart.handlers.f40 import F40Handler
            return F40Handler
        elif system == 'windows':
            # Windows doesn't have native Kickstart support, but we can still parse
            from pykickstart.handlers.f40 import F40Handler
            return F40Handler
        else:
            # Default fallback
            from pykickstart.handlers.f40 import F40Handler
            return F40Handler
            
    except ImportError:
        # Ultimate fallback if no handlers are available
        raise ImportError("No suitable pykickstart handler found for this system")


def handle_kickstart(file_path: str, dry_run: bool = False) -> int:
    """Handle kickstart command execution."""
    try:
        # Import pykickstart here to avoid import errors if not installed
        from pykickstart.parser import KickstartParser
        from pykickstart.errors import KickstartError
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: Kickstart file '{file_path}' not found.")
            return 1
        
        # Detect and use the appropriate handler for the current OS
        try:
            HandlerClass = detect_os_handler()
            print(f"Using handler: {HandlerClass.__name__}")
        except ImportError as e:
            print(f"Error: {e}")
            return 1
        
        # Parse the kickstart file
        handler = HandlerClass()
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
            
            # Safely access handler attributes
            try:
                lang = getattr(parser.handler.lang, 'lang', 'Not specified')
                print(f"  Language: {lang}")
            except AttributeError:
                print("  Language: Not specified")
            
            try:
                keyboard = getattr(parser.handler.keyboard, 'keyboard', 'Not specified')
                print(f"  Keyboard: {keyboard}")
            except AttributeError:
                print("  Keyboard: Not specified")
            
            try:
                network_count = len(parser.handler.network.network) if hasattr(parser.handler.network, 'network') else 0
                print(f"  Network: {network_count} network(s) configured")
            except AttributeError:
                print("  Network: Not specified")
            
            try:
                package_count = len(parser.handler.packages.packageList) if hasattr(parser.handler.packages, 'packageList') else 0
                print(f"  Packages: {package_count} packages selected")
            except AttributeError:
                print("  Packages: Not specified")
            
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