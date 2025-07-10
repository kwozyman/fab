"""
Kickstart file processing functionality.
"""

import os
import logging

from .os_detection import detect_os_handler
from .commands import KickstartCommandExecutor

# Whitelist of valid kickstart commands
VALID_COMMANDS = {
    # Basic system configuration
    #"lang": "System language setting",
    #"keyboard": "Keyboard layout",
    #"timezone": "System timezone",
    #"rootpw": "Root password",
    # Network configuration
    #"firewall": "Firewall settings",
    # Package management
    #"repo": "Repository configuration",
    # User management
    "user": "User creation",
    "group": "Group creation",
    # System services
    #"services": "Service configuration",
    #"selinux": "SELinux configuration",
    # Miscellaneous
    #"firstboot": "First boot configuration",
    # SSH configuration
    #"sshkey": "SSH key",
    # Additional valid commands for containers
    #"timesource": "Time source configuration",
    # Section markers (valid kickstart syntax)
    "%packages": "Package selection section",
    "%end": "Section end marker",
    "%post": "Post-installation script section",
    "%pre": "Pre-installation script section",
}


class FabKickstart:
    def __init__(self,
                file_path: str,
                dry_run: bool = False,
                ignore_unknown: bool = False):
        """
        Initialize the Kickstart executor.

        Args:
            dry_run: If True, only validate, do not execute
            ignore_unknown: If True, continue even if unknown commands are present
        """
        self.file_path = file_path
        #self.handler = handler
        #self.parser = parser
        self.dry_run = dry_run
        self.ignore_unknown = ignore_unknown
        self.logger = logging.getLogger(__name__)
        self.execution_results = []
   

    def execute(self):
        """
        Execute the Kickstart file.
        """

    def validate_kickstart_commands(self) -> tuple[bool, list[str]]:
        """
        Validate kickstart commands against the whitelist.
        Only validates actual kickstart commands, not script content within sections.

        Returns:
            Tuple of (is_valid, list_of_violations)
        """
        violations = []
        lines = self.content.split("\n")

        in_script_section = False

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Check for section markers
            if line.startswith("%"):
                if line in ["%packages", "%pre", "%post", "%traceback", "%end"]:
                    if line == "%end":
                        in_script_section = False
                    else:
                        in_script_section = True
                    continue

            # Skip lines within script sections (let pykickstart handle validation)
            if in_script_section:
                continue

            # Extract command (first word on the line)
            parts = line.split()
            if not parts:
                continue

            command = parts[0].lower()

            # Check if command is in whitelist
            if command not in VALID_COMMANDS:
                violations.append(
                    f"Line {line_num}: Warning: Unknown command '{command}' - not in valid list"
                )

        return len(violations) == 0, violations

    
    def handle_kickstart(self) -> int:
        """Handle kickstart command execution.
        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            # Import pykickstart here to avoid import errors if not installed
            from pykickstart.parser import KickstartParser
            from pykickstart.errors import KickstartError

            # Check if file exists
            if not os.path.exists(self.file_path):
                print(f"Error: Kickstart file '{self.file_path}' not found.")
                return 1

            # Detect and use the appropriate handler for the current OS
            try:
                HandlerClass = detect_os_handler()
                print(f"Using handler: {HandlerClass.__name__}")
                self.handler = HandlerClass()
            except ImportError as e:
                print(f"Error: {e}")
                return 1

            # Read the kickstart file content
            with open(self.file_path, "r") as f:
                self.content = f.read()

            # Parse the kickstart file first to validate kickstart commands
            self.handler = HandlerClass()
            self.parser = KickstartParser(self.handler)

            try:
                self.parser.readKickstartFromString(self.content)
                print(f"Successfully parsed Kickstart file: {self.file_path}")
            except KickstartError as e:
                print(f"Error parsing Kickstart file: {e}")
                return 1

            # Now validate against our whitelist (only kickstart commands, not script content)
            is_valid, violations = self.validate_kickstart_commands()
            if not is_valid:
                print("Warning: Kickstart file contains unknown commands:")
                for violation in violations:
                    print(f"  {violation}")
                if not self.ignore_unknown:
                    return 1
            else:
                print("Kickstart contains only valid commands")

            if self.dry_run:
                print("Dry run mode: Kickstart file is valid and ready for execution.")
                return 0

            # Command execution
            print("Executing Kickstart file...")
            for command in VALID_COMMANDS:
                if hasattr(self.handler, command):
                    command_obj = getattr(self.handler, command)
                    for obj in command_obj.dataList():
                        KickstartCommandExecutor(command, obj)

            return 0

        except ImportError:
            print("Error: pykickstart library is not installed.")
            print("Install it with: pip install pykickstart")
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 1
