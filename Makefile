# Makefile for FAB CLI

# Configurable settings
MAX_LINE_LENGTH ?= 120

.PHONY: help test install uninstall lint pep8-fix

help:
	@echo "Available targets:"
	@echo "  test       Run the test suite with pytest"
	@echo "  install    Install fab for the local user (pip install --user .)"
	@echo "  uninstall  Uninstall fab-cli package (pip uninstall -y fab-cli)"
	@echo "  lint       Check code for PEP8 compliance"
	@echo "  pep8-fix   Automatically fix PEP8 compliance issues"
	@echo ""
	@echo "Configuration:"
	@echo "  MAX_LINE_LENGTH=$(MAX_LINE_LENGTH) (can be overridden: make lint MAX_LINE_LENGTH=88)"

# Run tests using pytest
test:
	pytest --verbosity=2

# Install fab for the local user
install:
	pip install --user .

# Uninstall fab-cli package
uninstall:
	pip uninstall -y fab-cli

# Check code for PEP8 compliance
lint:
	flake8 --max-line-length=$(MAX_LINE_LENGTH) .

# Automatically fix PEP8 compliance issues
pep8-fix:
	autopep8 --max-line-length=$(MAX_LINE_LENGTH) --in-place --recursive . 