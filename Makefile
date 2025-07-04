# Makefile for FAB CLI

.PHONY: help test install uninstall

help:
	@echo "Available targets:"
	@echo "  test       Run the test suite with pytest"
	@echo "  install    Install fab for the local user (pip install --user .)"
	@echo "  uninstall  Uninstall fab-cli package (pip uninstall -y fab-cli)"

# Run tests using pytest
test:
	pytest

# Install fab for the local user
install:
	pip install --user .

# Uninstall fab-cli package
uninstall:
	pip uninstall -y fab-cli 