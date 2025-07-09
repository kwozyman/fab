"""
Kickstart command execution framework using pyanaconda.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Tuple
from .whitelist import VALID_COMMANDS, get_valid_commands


class KickstartExecutor:
    """
    Framework for executing Kickstart commands using pyanaconda.
    
    This class provides a safe execution environment for Kickstart commands
    that have been validated against the whitelist.
    """
    
    def __init__(self, dry_run: bool = False, ignore_unknown: bool = False):
        """
        Initialize the Kickstart executor.
        
        Args:
            dry_run: If True, simulate execution without making changes
            ignore_unknown: If True, continue even if unknown commands are present
        """
        self.dry_run = dry_run
        self.ignore_unknown = ignore_unknown
        self.logger = logging.getLogger(__name__)
        self.execution_results = []
        
        # Initialize pyanaconda components
        try:
            from pyanaconda import kickstart
            from pyanaconda import installation
            from pyanaconda.core import util
            self.kickstart = kickstart
            self.installation = installation
            self.util = util
        except ImportError as e:
            raise ImportError(f"pyanaconda not available: {e}")
    
    def execute_kickstart_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Execute a Kickstart file using pyanaconda.
        
        Args:
            file_path: Path to the Kickstart file
            
        Returns:
            Tuple of (success, list_of_messages)
        """
        try:
            # Read and parse the Kickstart file
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse using pyanaconda
            handler = self._create_handler()
            parser = self.kickstart.AnacondaKSParser(handler)
            
            try:
                parser.readKickstartFromString(content)
                self.logger.info(f"Successfully parsed Kickstart file: {file_path}")
            except self.kickstart.KickstartError as e:
                return False, [f"Error parsing Kickstart file: {e}"]
            
            # Execute the commands
            return self._execute_parsed_kickstart(handler, content)
            
        except Exception as e:
            return False, [f"Unexpected error: {e}"]
    
    def _create_handler(self):
        """Create an appropriate pyanaconda handler for the current system."""
        try:
            # Try to use the latest Fedora handler as default
            from pykickstart.handlers.f40 import F40Handler
            return F40Handler()
        except ImportError:
            # Fallback to a basic handler - use the control handler
            from pykickstart.handlers.control import handler
            return handler
    
    def _execute_parsed_kickstart(self, handler, content: str) -> Tuple[bool, List[str]]:
        """
        Execute the parsed Kickstart commands.
        
        Args:
            handler: The pyanaconda handler with parsed commands
            content: Original Kickstart content
            
        Returns:
            Tuple of (success, list_of_messages)
        """
        messages = []
        success = True
        
        try:
            # SKIP all script execution (pre/post/traceback)
            # Only process system config (lang)
            config_success, config_messages = self._execute_system_config(handler)
            messages.extend(config_messages)
            if not config_success:
                success = False
            return success, messages
        except Exception as e:
            return False, [f"Error during execution: {e}"]
    
    def _execute_system_config(self, handler) -> Tuple[bool, List[str]]:
        """
        Execute system configuration commands.
        
        Args:
            handler: The pyanaconda handler
            
        Returns:
            Tuple of (success, list_of_messages)
        """
        messages = []
        success = True
        
        # Language configuration
        if hasattr(handler, 'lang') and handler.lang:
            messages.append(f"Setting language: {getattr(handler.lang, 'lang', 'default')}")
            if not self.dry_run:
                self._execute_language_config(handler.lang)
        
        return success, messages
    
    def _execute_language_config(self, lang_config):
        """Execute language configuration."""
        try:
            # Use pyanaconda's localization module
            from pyanaconda import localization
            if hasattr(lang_config, 'lang'):
                localization.setup_locale(lang_config.lang)
        except Exception as e:
           self.logger.warning(f"Failed to set language: {e}")
    

    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the execution results."""
        return {
            'dry_run': self.dry_run,
            'ignore_unknown': self.ignore_unknown,
            'results': self.execution_results,
            'valid_commands': get_valid_commands()
        }


def execute_kickstart_with_pyanaconda(
    file_path: str, 
    dry_run: bool = False, 
    ignore_unknown: bool = False
) -> Tuple[bool, List[str]]:
    """
    Execute a Kickstart file using pyanaconda framework.
    
    Args:
        file_path: Path to the Kickstart file
        dry_run: If True, simulate execution without making changes
        ignore_unknown: If True, continue even if unknown commands are present
        
    Returns:
        Tuple of (success, list_of_messages)
    """
    executor = KickstartExecutor(dry_run=dry_run, ignore_unknown=ignore_unknown)
    return executor.execute_kickstart_file(file_path) 