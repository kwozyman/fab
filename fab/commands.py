"""
Kickstart command execution functionality.
"""

import subprocess
import os

class KickstartRootError(Exception):
    """Exception raised when a command requires root privileges."""
    pass

class KickstartError(Exception):
    """Exception raised when a command fails."""
    pass

class KickstartCommandExecutor:
    def __init__(self, command_name: str, command_obj: object):
        self.command_name = command_name
        self.command_obj = command_obj
        try:
            execute_method = getattr(self, f"execute_{self.command_name}")
            print(f'Executing {self.command_name} command: {self.command_obj.__str__().strip()}')
            execute_method()
        except AttributeError:
            print(f"Command '{self.command_name}' not found in executor")

    def _check_root(self):
        if os.geteuid() != 0:
            raise KickstartRootError(f"Must be root")

    def execute_group(self):
        # check if the user is root
        self._check_root()

        name = getattr(self.command_obj, 'name')
        gid = getattr(self.command_obj, 'gid')
        print(f'Creating group {name} with gid {gid}')

        # if gid is not None, create the group with the given gid
        if gid is not None:
            # use subprocess.run to create the group with the given gid and merge stderr and stdout
            result = subprocess.run(f'groupadd -g {gid} {name}', shell=True, capture_output=True)
        else:
            result = subprocess.run(f'groupadd {name}', shell=True, capture_output=True)
        if result.returncode != 0:
            raise KickstartError(f"Failed to create group {name}: {result.stderr}")

