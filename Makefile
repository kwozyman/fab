# Makefile for FAB CLI

# Configurable settings
MAX_LINE_LENGTH ?= 120
INSTALL_USER ?= --user
CONTAINER_NAME ?= fab-cli
CONTAINER_TOOL ?= podman
FROM ?= registry.fedoraproject.org/fedora-bootc:latest

.PHONY: help test install uninstall lint pep8-fix

help:
	@echo "Available targets:"
	@echo "  test       Run the test suite with pytest"
	@echo "  install    Install fab for the local user (pip install --user .)"
	@echo "  uninstall  Uninstall fab-cli package (pip uninstall -y fab-cli)"
	@echo "  container  Build a container image from the current directory"
	@echo "  container-run  Run the container image"
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
	python -c "import importlib.util; import sys; sys.exit(0 if importlib.util.find_spec('pyanaconda') else 1)" || echo "Error: pyanaconda is not installed"
	pip install $(INSTALL_USER) .

# Uninstall fab-cli package
uninstall:
	pip uninstall -y fab-cli

# Build a container image from the current directory
container:
	$(CONTAINER_TOOL) build --from $(FROM) --tag $(CONTAINER_NAME) .

# Run the container image
container-run:
	$(CONTAINER_TOOL) run --rm -it $(CONTAINER_NAME)

# Check code for PEP8 compliance
lint:
	flake8 --max-line-length=$(MAX_LINE_LENGTH) --exclude=build .

# Automatically fix PEP8 compliance issues
pep8-fix:
	autopep8 --max-line-length=$(MAX_LINE_LENGTH) --in-place --recursive . 
