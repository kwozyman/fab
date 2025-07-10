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

        return True

    def execute_user(self):
        # check if the user is root
        self._check_root()
        
        # get the name, password, and group attributes from the command_obj
        name = getattr(self.command_obj, 'name', None)
        homedir = getattr(self.command_obj, 'homedir', None)
        iscrypted = getattr(self.command_obj, 'isCrypted', None)
        password = getattr(self.command_obj, 'password', None)
        shell = getattr(self.command_obj, 'shell', None)
        uid = getattr(self.command_obj, 'uid', None)
        lock = getattr(self.command_obj, 'lock', None)
        gecos = getattr(self.command_obj, 'gecos', None)
        gid = getattr(self.command_obj, 'gid', None)
        groups = getattr(self.command_obj, 'groups', None)

        print(f'Creating user {name}')
        # create the user with the given attributes
        # construct the command string and do not include parameters that are None

        # Build the useradd command, only including options if their values are not None
        command_parts = ['useradd']
        if homedir is not None and homedir != '':
            command_parts += ['--home-dir', str(homedir)]
        if password is not None:
            if not iscrypted:
                # generate an encrypted password usable by useradd using mkpasswd 
                encrypted_password = subprocess.run(f'mkpasswd -m SHA-512 {password}', shell=True, capture_output=True).stdout.decode('utf-8').strip()
                command_parts += ['--password', encrypted_password]
            else:
                command_parts += ['--password', str(password)]
        if shell is not None and shell != '':
            command_parts += ['--shell', str(shell)]
        if uid is not None:
            command_parts += ['--uid', str(uid)]
        if lock is not None and lock:
            #TODO: handle locked account
            pass
        if gecos is not None and gecos != '':
            command_parts += ['--comment', str(gecos)]
        if gid is not None:
            command_parts += ['--gid', str(gid)]
        if groups is not None and len(groups) > 0:
            command_parts += ['--groups', str(groups)]
        command_parts.append(str(name))
        command_string = ' '.join(command_parts)

        print(f'Executing command: {command_string}')

        result = subprocess.run(command_string, shell=True, capture_output=True)
        if result.returncode != 0:
            raise KickstartError(f"Failed to create user {name}: {result.stderr}")

        return True
