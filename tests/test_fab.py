"""
Tests for the fab CLI tool.
"""

import pytest
from fab import main, __version__
import sys
from io import StringIO


def test_version_command():
    """Test the version command."""
    # Redirect stdout to capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Mock sys.argv for version command
        sys.argv = ['fab', 'version']
        result = main()
        
        # Get captured output
        output = sys.stdout.getvalue().strip()
        
        assert result == 0
        assert output == f"fab version {__version__}"
    finally:
        sys.stdout = old_stdout





def test_help_command():
    """Test that help is displayed when no command is given."""
    # Redirect stdout to capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Mock sys.argv for help (no command)
        sys.argv = ['fab']
        result = main()
        
        # Get captured output
        output = sys.stdout.getvalue()
        
        assert result == 0
        assert "FAB - Fast Assembler for BootC" in output
        assert "Available commands" in output
    finally:
        sys.stdout = old_stdout


if __name__ == '__main__':
    pytest.main([__file__]) 