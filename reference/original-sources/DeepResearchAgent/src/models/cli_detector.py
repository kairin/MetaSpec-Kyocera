"""CLI Tool Detection and Configuration

Detects available CLI tools and provides appropriate model mappings for configuration.
"""

import logging
import subprocess
import shutil
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class CLIToolDetector:
    """Detects available CLI tools and maps them to model configurations"""

    def __init__(self):
        self.detected_tools = {}
        self.model_mappings = {}

    def detect_claude_code_cli(self) -> Dict[str, any]:
        """Detect Claude Code CLI availability"""
        try:
            # Check if claude command exists (actual command name)
            if not shutil.which('claude'):
                return {
                    'available': False,
                    'reason': 'claude command not found',
                    'install_cmd': 'npm install -g @anthropics/claude-code'
                }

            # Claude CLI doesn't support --version, so just check if it responds
            result = subprocess.run(
                ['claude', '--help'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    'available': True,
                    'version': 'claude-code-cli',
                    'model_mappings': {
                        # Map API model names to CLI equivalents
                        'claude-3.7-sonnet-thinking': 'claude-code-cli',
                        'claude37-sonnet': 'claude-code-cli',
                        'claude-4-sonnet': 'claude-code-cli'
                    }
                }
            else:
                return {
                    'available': False,
                    'reason': f'claude failed: {result.stderr}',
                    'install_cmd': 'npm install -g @anthropics/claude-code'
                }

        except subprocess.TimeoutExpired:
            return {
                'available': False,
                'reason': 'claude-code command timed out',
                'install_cmd': 'npm install -g @anthropics/claude-code'
            }
        except Exception as e:
            return {
                'available': False,
                'reason': f'Error detecting claude-code: {e}',
                'install_cmd': 'npm install -g @anthropics/claude-code'
            }

    def detect_gemini_cli(self) -> Dict[str, any]:
        """Detect Gemini CLI availability"""
        try:
            # Check if gcloud is available and authenticated
            if not shutil.which('gcloud'):
                return {
                    'available': False,
                    'reason': 'gcloud command not found',
                    'install_cmd': 'Install Google Cloud SDK and run: gcloud auth application-default login'
                }

            # Check authentication status
            result = subprocess.run(
                ['gcloud', 'auth', 'list', '--format=value(account)'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0 or not result.stdout.strip():
                return {
                    'available': False,
                    'reason': 'gcloud not authenticated',
                    'install_cmd': 'gcloud auth application-default login'
                }

            # For CLI usage, we don't need google-generativeai package
            return {
                'available': True,
                'authenticated_account': result.stdout.strip().split('\n')[0],
                'model_mappings': {
                    # Map API model names to CLI equivalents
                    'gemini-2.5-pro': 'gemini-cli',
                    'gemini-vision': 'gemini-cli'
                }
            }

        except subprocess.TimeoutExpired:
            return {
                'available': False,
                'reason': 'gcloud command timed out',
                'install_cmd': 'Install Google Cloud SDK and authenticate'
            }
        except Exception as e:
            return {
                'available': False,
                'reason': f'Error detecting gemini CLI: {e}',
                'install_cmd': 'Install Google Cloud SDK and authenticate'
            }

    def detect_all_cli_tools(self) -> Dict[str, Dict]:
        """Detect all available CLI tools"""
        results = {
            'claude_code_cli': self.detect_claude_code_cli(),
            'gemini_cli': self.detect_gemini_cli()
        }

        # Cache results
        self.detected_tools = results

        # Build combined model mappings
        self.model_mappings = {}
        for tool_name, tool_info in results.items():
            if tool_info['available'] and 'model_mappings' in tool_info:
                self.model_mappings.update(tool_info['model_mappings'])

        return results

    def get_cli_model_mapping(self, api_model_name: str) -> Optional[str]:
        """Get CLI equivalent for an API model name

        Args:
            api_model_name: Original API model name

        Returns:
            CLI model name if available, None otherwise
        """
        if not self.model_mappings:
            self.detect_all_cli_tools()

        return self.model_mappings.get(api_model_name)

    def create_cli_config_overrides(self) -> Dict[str, str]:
        """Create configuration overrides for detected CLI tools

        Returns:
            Dictionary mapping original model names to CLI equivalents
        """
        if not self.detected_tools:
            self.detect_all_cli_tools()

        overrides = {}

        # Add mappings for all detected CLI tools
        for tool_name, tool_info in self.detected_tools.items():
            if tool_info['available'] and 'model_mappings' in tool_info:
                overrides.update(tool_info['model_mappings'])

        return overrides

    def get_fallback_models(self) -> Dict[str, str]:
        """Get fallback models for unavailable CLI tools"""
        fallbacks = {}

        # If Claude Code CLI not available, suggest local alternatives
        if not self.detected_tools.get('claude_code_cli', {}).get('available', False):
            fallbacks.update({
                'claude-3.7-sonnet-thinking': 'qwen2.5-32b-instruct',
                'claude37-sonnet': 'qwen2.5-32b-instruct'
            })

        # If Gemini CLI not available, suggest local alternatives
        if not self.detected_tools.get('gemini_cli', {}).get('available', False):
            fallbacks.update({
                'gemini-2.5-pro': 'qwen2.5-14b-instruct'
            })

        return fallbacks

    def log_detection_results(self):
        """Log CLI detection results"""
        if not self.detected_tools:
            self.detect_all_cli_tools()

        logger.info("CLI Tool Detection Results:")

        for tool_name, tool_info in self.detected_tools.items():
            if tool_info['available']:
                logger.info(f"✅ {tool_name}: Available")
                if 'version' in tool_info:
                    logger.info(f"   Version: {tool_info['version']}")
                if 'authenticated_account' in tool_info:
                    logger.info(f"   Account: {tool_info['authenticated_account']}")
            else:
                logger.warning(f"❌ {tool_name}: {tool_info['reason']}")
                logger.info(f"   Fix: {tool_info['install_cmd']}")

        if self.model_mappings:
            logger.info("Available CLI model mappings:")
            for api_model, cli_model in self.model_mappings.items():
                logger.info(f"  {api_model} → {cli_model}")

    def get_setup_instructions(self) -> str:
        """Generate setup instructions for missing CLI tools"""
        if not self.detected_tools:
            self.detect_all_cli_tools()

        instructions = []

        for tool_name, tool_info in self.detected_tools.items():
            if not tool_info['available']:
                instructions.append(f"## Setup {tool_name.replace('_', ' ').title()}")
                instructions.append(f"**Issue**: {tool_info['reason']}")
                instructions.append(f"**Solution**: {tool_info['install_cmd']}")
                instructions.append("")

        if instructions:
            return "\n".join([
                "# CLI Tools Setup Required",
                "",
                "To use CLI tools instead of API keys, set up the following:",
                "",
                *instructions,
                "After setup, restart the application."
            ])
        else:
            return "✅ All CLI tools are properly configured!"


# Global instance for easy access
cli_detector = CLIToolDetector()