"""
Kickstart file processing functionality.
"""

import os
from .os_detection import detect_os_handler
from .whitelist import validate_kickstart_commands


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
        
        # Read the kickstart file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the kickstart file first to validate kickstart commands
        handler = HandlerClass()
        parser = KickstartParser(handler)
        
        try:
            parser.readKickstartFromString(content)
            print(f"Successfully parsed Kickstart file: {file_path}")
        except KickstartError as e:
            print(f"Error parsing Kickstart file: {e}")
            return 1
        
        # Now validate against our whitelist (only kickstart commands, not script content)
        is_valid, violations = validate_kickstart_commands(content)
        if not is_valid:
            print("Warning: Kickstart file contains unknown commands:")
            for violation in violations:
                print(f"  {violation}")
            return 1
        
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
            
    except ImportError:
        print("Error: pykickstart library is not installed.")
        print("Install it with: pip install pykickstart")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1 