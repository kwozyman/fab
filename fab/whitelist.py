"""
Kickstart command whitelist for security validation.
"""

# Whitelist of valid kickstart commands
VALID_COMMANDS = {
    # Basic system configuration
    #"lang": "System language setting",
    #"keyboard": "Keyboard layout",
    #"timezone": "System timezone",
    "rootpw": "Root password",
    # Network configuration
    #"firewall": "Firewall settings",
    # Package management
    #"repo": "Repository configuration",
    # User management
    "user": "User creation",
    "group": "Group creation",
    # System services
    #"services": "Service configuration",
    "selinux": "SELinux configuration",
    # Miscellaneous
    #"firstboot": "First boot configuration",
    # SSH configuration
    "sshkey": "SSH key",
    # Additional valid commands for containers
    #"timesource": "Time source configuration",
    # Section markers (valid kickstart syntax)
    "%packages": "Package selection section",
    "%end": "Section end marker",
    "%post": "Post-installation script section",
    "%pre": "Pre-installation script section",
}


def validate_kickstart_commands(content: str) -> tuple[bool, list[str]]:
    """
    Validate kickstart commands against the whitelist.
    Only validates actual kickstart commands, not script content within sections.

    Args:
        content: The kickstart file content

    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    lines = content.split("\n")

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


def get_valid_commands() -> dict[str, str]:
    """Get the current whitelist of valid commands."""
    return VALID_COMMANDS.copy()


def add_valid_command(command: str, description: str = "") -> None:
    """Add a command to the whitelist."""
    VALID_COMMANDS[command.lower()] = description


def remove_valid_command(command: str) -> None:
    """Remove a command from the whitelist."""
    command = command.lower()
    if command in VALID_COMMANDS:
        del VALID_COMMANDS[command]
