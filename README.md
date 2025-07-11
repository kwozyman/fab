# FAB - Fast Assembler for BootC

A command-line interface tool for configuring [BootC](https://github.com/containers/bootc) containers via [Kickstart](https://pykickstart.readthedocs.io) and Containerfiles.

## Overview

FAB (Fast Assembler for BootC) is a versatile tool that provides two main functionalities:

1. **Kickstart Execution**: A tool for reading and executing Kickstart files with validation and dry-run capabilities
2. **BootC Container Building**: A modular build pipeline for BootC containers, allowing the modularization of Containerfiles and bootc image building

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/kwozyman/fab.git
cd fab
```

2. Install in development mode:
```bash
pip install -e .
```

Or use the Makefile:
```bash
make install
```

### Using pip (when published)

```bash
pip install fab-cli
```

### Dependencies

FAB requires the following dependencies:
- `pykickstart>=3.0`
- `pyyaml>=6.0`

## Usage

### Basic Commands

Show help:
```bash
fab --help
```

Show version:
```bash
fab version
fab version --show-commands  # Also show valid kickstart commands
```

### Kickstart File Execution

Execute Kickstart file:
```bash
fab kickstart file.ks
fab kickstart file.ks --dry-run # just validate kickstart file, no actual execution
fab kickstart file.ks --ignore-unknown # ignore kickstart commands that are not implemented yet
```

**Note**: The `--dry-run` option is recommended for testing, as it simulates execution without making system changes.

### BootC Container Building

Build a container using a fabfile:
```bash
fab build Fabfile.example
fab build Fabfile.example --container-tool /usr/bin/podman
fab build Fabfile.example --container-tool-extra-args="--no-cache"
```

**Note**: The `--container-tool-extra-args` option allows passing additional arguments to the underlying container tool (default: podman).

### Examples

```bash
# Show help
fab --help

# Show version
fab version
fab version --show-commands  # Also show valid commands

# Execute a Kickstart file
fab kickstart samples/sample.ks

# Validate a Kickstart file without executing
fab kickstart samples/sample.ks --dry-run

# Continue execution even with unknown commands (warnings only)
fab kickstart samples/sample.ks --ignore-unknown

# Build a BootC container
fab build samples/Fabfile.example
```

## Kickstart File Execution

FAB enables declarative configuration of BootC images by leveraging the well-established Kickstart language. By interpreting Kickstart files directly, FAB allows users to define system setup and provisioning steps in a familiar, structured format, integrating these instructions seamlessly into modern container-based workflows.

FAB's Kickstart support allows you to:

- **Declarative execution**: Execute Kickstart commands inside `RUN` invocations in Dockerfiles
- **Preserve existing investments**: Move Kickstart configurations without complete rewrites

### Features

FAB can parse and execute Kickstart files using the pykickstart framework. It supports:

- **Declarative execution**: Execute commands inside container `RUN` statements
- **Validation**: Parse and validate Kickstart syntax
- **Dry-run**: Simulate execution without making system changes
- **Error handling**: Graceful handling of unknown commands

### Integration with Container Builds

Rather than generating new formats, FAB focuses on executing declarative code inside `RUN` invocations in Dockerfiles. This approach:

- **Leverages existing ecosystem**: Works with all Dockerfile consumers (podman build, docker build, etc.)
- **Maintains compatibility**: Supports remote builds, multi-arch builds, and other container features

### Sample Kickstart Files

The `samples/` directory contains several example Kickstart files for testing and migration:
- `sample.ks` - Basic sample demonstrating core functionality
- `test_forbidden.ks` - Test file with forbidden commands (security validation)
- `test_ignored.ks` - Test file with ignored commands (migration scenarios)
- `test_script.ks` - Test file with script sections (complex deployment scenarios)

### Example of applying a Kickstart to a BootC container build

```Dockerfile
FROM quay.io/kwozyman/fab:latest as fab
COPY ./example.ks /
FROM registry.fedoraproject.org/fedora-bootc:latest
RUN --mount=type=bind,from=fab,target=/ks /ks/fab kickstart /ks/example.ks
```

This would run and apply `example.ks` to a BootC Containerfile. Notice the usage of a second container image (`quay.io/kwozyman/fab:latest`) to keep `fab`'s environment separated from the resulting image.

## BootC Container Building

### Fabfiles

FAB uses a main descriptive file called "Fabfile" to define the final BootC image. A Fabfile example looks like this:

```yaml
---
metadata:
  name: fabrules
  description: My first bootc
from: quay.io/centos-bootc/centos-bootc:stream9
include:
  - modules/ssh/ssh.yaml
  - modules/dnf/install.yaml
buildargs:
  - SSHPUBKEY: insert_ssh_pub_key_here
  - RPMS: tmux cloud-init
```

The fields are:
- `metadata`: Metadata about the BootC image
- `from`: Base image (i.e., the first `FROM` in the pipeline)
- `include`: List of modules to include, in order in the BootC image
- `buildargs`: List of buildargs (variables) used in the build process

### Modules

For each module, there is a short descriptive file with the module definition. See the `samples/modules/` directory for examples:

```yaml
---
metadata:
  name: dnf-install
  description: |
    Install a list of packages via dnf
containerfile: install.Containerfile
buildargs:
  - RPMS
```

Module fields:
- `metadata`: Module level metadata
- `containerfile`: Filename for the Containerfile to use
- `buildargs`: Simple list of expected buildargs (without values!)

### Available Modules

The project includes several example modules in `samples/modules/`:
- `cloud-init/` - Cloud-init configuration
- `dnf/` - Package management (install, upgrade, autoremove)
- `mount/` - Filesystem mounting
- `ssh/` - SSH key configuration


## Development

### Setup Development Environment

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

Or use the Makefile:
```bash
make test
```

3. Format code:
```bash
black .
```

4. Lint code:
```bash
flake8
```

5. Type checking:
```bash
mypy .
```

### Makefile Targets

The project includes a Makefile for common tasks:

```bash
make help        # Show available targets
make test        # Run the test suite
make install     # Install fab for the local user
make uninstall   # Uninstall fab-cli package
make container   # Build a container image
make lint        # Check code for PEP8 compliance
make pep8-fix    # Automatically fix PEP8 issues
```

### Project Structure

```
fab/
├── fab/                    # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Configuration and version
│   ├── fabfile.py         # BootC fabfile processing
│   ├── kickstart.py       # Kickstart processing
│   ├── module.py          # Module handling
│   ├── os_detection.py    # OS detection and handler selection
│   └── commands.py        # Kickstart command execution framework
├── samples/                # Sample files
│   ├── Fabfile.example    # Example BootC fabfile
│   ├── Containerfile      # Example container file
│   ├── modules/           # Example modules
│   │   ├── cloud-init/    # Cloud-init module
│   │   ├── dnf/          # Package management modules
│   │   ├── mount/        # Mounting module
│   │   └── ssh/          # SSH module
│   ├── sample.ks          # Basic Kickstart sample
│   ├── test_forbidden.ks  # Test file with forbidden commands
│   ├── test_ignored.ks    # Test file with ignored commands
│   └── test_script.ks     # Test file with script sections
├── fab.py                 # Entry point script
├── setup.py               # Package configuration
├── Makefile               # Build and development tasks
├── README.md              # This file
├── requirements.txt       # Dependencies
└── tests/                 # Test files
    ├── __init__.py
    ├── test_executor.py   # Tests for executor framework
    └── test_fab.py        # Tests for fab functionality
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 