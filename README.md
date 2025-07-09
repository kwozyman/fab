# FAB - Fast Assembler for BootC

A command-line interface tool for assembling BootC containers.

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
- `pykickstart>=3.0` - For Kickstart file parsing and validation
- `pyanaconda>=40.0` - For executing Kickstart commands (system integration)

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

Execute Kickstart file:
```bash
fab kickstart file.ks
fab kickstart file.ks --dry-run
fab kickstart file.ks --ignore-unknown
```

**Note**: The `--dry-run` option is recommended for testing, as it simulates execution without making system changes.

### Examples

```bash
# Show help
fab --help

# Show version
fab version
fab version --show-commands  # Also show valid kickstart commands

# Execute a Kickstart file
fab kickstart samples/sample.ks

# Validate a Kickstart file without executing
fab kickstart samples/sample.ks --dry-run

# Continue execution even with unknown commands (warnings only)
fab kickstart samples/sample.ks --ignore-unknown
```

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
```

### Project Structure

```
fab/
├── fab/                    # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Configuration and version
│   ├── os_detection.py    # OS detection and handler selection
│   ├── kickstart.py       # Kickstart processing
│   ├── executor.py        # Command execution framework (pyanaconda)
│   └── whitelist.py       # Command validation
├── samples/                # Sample Kickstart files
│   ├── sample.ks          # Basic sample
│   ├── test_forbidden.ks  # Test file with forbidden commands
│   ├── test_ignored.ks    # Test file with ignored commands
│   └── test_script.ks     # Test file with script sections
├── fab.py                 # Entry point script
├── setup.py               # Package configuration
├── Makefile               # Build and development tasks
├── README.md              # This file
├── requirements.txt       # Dependencies
└── tests/                 # Test files
    └── test_executor.py   # Tests for executor framework
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