"""
Tests for the fab CLI tool.
"""

import pytest
from fab import main, __version__
import sys
import os
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


def test_kickstart_command_file_not_found():
    """Test the kickstart command with non-existent file."""
    # Redirect stdout to capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Mock sys.argv for kickstart command with non-existent file
        sys.argv = ['fab', 'kickstart', 'nonexistent.ks']
        result = main()
        
        # Get captured output
        output = sys.stdout.getvalue().strip()
        
        assert result == 1
        assert "Error: Kickstart file 'nonexistent.ks' not found." in output
    finally:
        sys.stdout = old_stdout


def test_kickstart_command_dry_run():
    """Test the kickstart command with dry-run option."""
    # Create a temporary kickstart file
    test_ks_content = """# Test kickstart file
lang en_US.UTF-8
keyboard us
"""
    
    test_file = "test_sample.ks"
    with open(test_file, 'w') as f:
        f.write(test_ks_content)
    
    try:
        # Redirect stdout to capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Mock sys.argv for kickstart command with dry-run
        sys.argv = ['fab', 'kickstart', test_file, '--dry-run']
        result = main()
        
        # Get captured output
        output = sys.stdout.getvalue().strip()
        
        # Note: This test will fail if pykickstart is not installed
        # but that's expected behavior
        if "pykickstart library is not installed" in output:
            assert result == 1
        else:
            assert result == 0
            assert "Successfully parsed Kickstart file" in output
            assert "Dry run mode" in output
    finally:
        sys.stdout = old_stdout
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == '__main__':
    pytest.main([__file__]) 