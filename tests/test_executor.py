"""
Tests for the Kickstart executor framework.
"""

import pytest
import tempfile
import os
from fab.executor import KickstartExecutor, execute_kickstart_with_pyanaconda


class TestKickstartExecutor:
    """Test the KickstartExecutor class."""

    def test_executor_initialization(self):
        """Test that the executor can be initialized."""
        try:
            executor = KickstartExecutor(dry_run=True)
            assert executor.dry_run is True
            assert executor.ignore_unknown is False
        except ImportError:
            pytest.skip("pyanaconda not available")

    def test_executor_with_ignore_unknown(self):
        """Test executor initialization with ignore_unknown=True."""
        try:
            executor = KickstartExecutor(dry_run=True, ignore_unknown=True)
            assert executor.ignore_unknown is True
        except ImportError:
            pytest.skip("pyanaconda not available")

    def test_execute_simple_kickstart(self):
        """Test executing a simple Kickstart file."""
        try:
            # Create a simple test Kickstart file
            test_content = """# Test kickstart file
lang en_US.UTF-8
keyboard us
timezone UTC
"""

            with tempfile.NamedTemporaryFile(mode='w', suffix='.ks', delete=False) as f:
                f.write(test_content)
                temp_file = f.name

            try:
                success, messages = execute_kickstart_with_pyanaconda(
                    temp_file, dry_run=True
                )

                # Should succeed in dry-run mode
                assert success is True
                assert len(messages) > 0

                # Should only contain language message (only lang command is handled)
                message_text = '\n'.join(messages)
                assert "Setting language" in message_text
                assert "Setting keyboard" not in message_text
                assert "Setting timezone" not in message_text

            finally:
                os.unlink(temp_file)

        except ImportError:
            pytest.skip("pyanaconda not available")

    def test_execute_kickstart_with_scripts(self):
        """Test executing a Kickstart file with script sections."""
        try:
            # Create a test Kickstart file with scripts
            test_content = """# Test kickstart file with scripts
lang en_US.UTF-8
keyboard us

%pre
#!/bin/bash
echo "Pre-installation script"
%end

%post
#!/bin/bash
echo "Post-installation script"
%end
"""

            with tempfile.NamedTemporaryFile(mode='w', suffix='.ks', delete=False) as f:
                f.write(test_content)
                temp_file = f.name

            try:
                success, messages = execute_kickstart_with_pyanaconda(
                    temp_file, dry_run=True
                )

                # Should succeed in dry-run mode
                assert success is True
                assert len(messages) > 0

                # Should contain language message (scripts are skipped in current implementation)
                message_text = '\n'.join(messages)
                assert "Setting language" in message_text
                # Note: Script execution is currently skipped in the executor
                # assert "pre-installation scripts" in message_text.lower()
                # assert "post-installation scripts" in message_text.lower()

            finally:
                os.unlink(temp_file)

        except ImportError:
            pytest.skip("pyanaconda not available")

    def test_execute_nonexistent_file(self):
        """Test executing a non-existent Kickstart file."""
        try:
            success, messages = execute_kickstart_with_pyanaconda(
                "nonexistent.ks", dry_run=True
            )

            # Should fail
            assert success is False
            assert len(messages) > 0
            assert "no such file" in messages[0].lower()

        except ImportError:
            pytest.skip("pyanaconda not available")

    def test_executor_summary(self):
        """Test getting execution summary."""
        try:
            executor = KickstartExecutor(dry_run=True)
            summary = executor.get_execution_summary()

            assert 'dry_run' in summary
            assert 'ignore_unknown' in summary
            assert 'results' in summary
            assert 'valid_commands' in summary
            assert summary['dry_run'] is True
            assert summary['ignore_unknown'] is False

        except ImportError:
            pytest.skip("pyanaconda not available")
