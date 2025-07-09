"""
Kickstart file processing functionality.
"""

import os
from .os_detection import detect_os_handler
from .whitelist import validate_kickstart_commands
from .executor import execute_kickstart_with_pyanaconda


def handle_kickstart(
    file_path: str, dry_run: bool = False, ignore_unknown: bool = False
) -> int:
    """Handle kickstart command execution.
    Args:
        file_path: Path to the Kickstart file
        dry_run: If True, only validate, do not execute
        ignore_unknown: If True, continue even if unknown commands are present
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
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
        with open(file_path, "r") as f:
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
            if not ignore_unknown:
                return 1

        if dry_run:
            print("Dry run mode: Kickstart file is valid and ready for execution.")
            return 0

        # Execute the Kickstart file using pyanaconda framework
        print("Executing Kickstart file using pyanaconda framework...")
        success, messages = execute_kickstart_with_pyanaconda(
            file_path, dry_run=dry_run, ignore_unknown=ignore_unknown
        )
        
        # Print execution messages
        for message in messages:
            print(f"  {message}")
        
        if success:
            print("Kickstart execution completed successfully.")
        else:
            print("Kickstart execution failed.")
            
        return 0 if success else 1

    except ImportError:
        print("Error: pykickstart library is not installed.")
        print("Install it with: pip install pykickstart")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
