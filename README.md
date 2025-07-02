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

### Using pip (when published)

```bash
pip install fab-cli
```

## Usage

### Basic Commands

Show help:
```bash
fab --help
```

Show version:
```bash
fab version
```

### Examples

```bash
# Show help
fab --help

# Show version
fab version
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

### Project Structure

```
fab/
├── fab.py          # Main CLI entry point
├── setup.py        # Package configuration
├── README.md       # This file
├── requirements.txt # Dependencies (optional)
└── tests/          # Test files (optional)
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