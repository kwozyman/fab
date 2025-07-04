"""
OS detection and handler selection for pykickstart.
"""

import os
import platform


def detect_os_handler():
    """Detect the operating system and return the appropriate handler class."""
    try:
        # Try to read /etc/os-release for Linux distribution info
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                os_info = dict(line.strip().split("=", 1) for line in f if "=" in line)

            distro_id = os_info.get("ID", "").lower()
            distro_version = os_info.get("VERSION_ID", "").strip('"')

            # Map common distributions to handlers
            if distro_id == "fedora":
                # Try to use the version-specific handler, fallback to latest
                try:
                    version_num = int(distro_version.split(".")[0])
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

            elif distro_id in ["rhel", "centos", "rocky", "alma"]:
                # Try to use the version-specific handler, fallback to latest
                try:
                    version_num = int(distro_version.split(".")[0])
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
        if system == "linux":
            # Default to Fedora 40 handler for Linux
            from pykickstart.handlers.f40 import F40Handler

            return F40Handler
        elif system == "windows":
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
