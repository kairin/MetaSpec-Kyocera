"""API Configuration Validator

Validates API configuration before model initialization to prevent startup crashes
caused by invalid URLs or placeholder values in environment configuration.
"""

import logging
import os
from typing import Dict, List, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class APIConfigValidator:
    """Validates API configuration before model initialization"""

    # Known placeholder values that indicate invalid configuration
    PLACEHOLDER_VALUES = {'', 'xxxxx', 'your_key_here', 'none', 'placeholder'}

    def __init__(self):
        self.validation_results: Dict[str, Dict] = {}

    def validate_url(self, url: str, name: str = "API URL") -> Tuple[bool, str]:
        """Validate API URL format and basic structure

        Args:
            url: The URL to validate
            name: Human-readable name for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url or url.lower() in self.PLACEHOLDER_VALUES:
            return False, f"{name} is placeholder or empty"

        if not url.startswith(('http://', 'https://')):
            return False, f"Invalid URL protocol: {url} (must start with http:// or https://)"

        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False, f"Invalid URL format: {url} (missing hostname)"
            return True, "Valid URL format"
        except Exception as e:
            return False, f"URL validation error: {e}"

    def validate_api_key(self, key: str, name: str = "API key") -> Tuple[bool, str]:
        """Validate API key format (not placeholder)

        Args:
            key: The API key to validate
            name: Human-readable name for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not key or key.lower() in self.PLACEHOLDER_VALUES:
            return False, f"{name} is placeholder or empty"

        if len(key) < 10:  # Reasonable minimum length
            return False, f"{name} appears too short (minimum 10 characters)"

        return True, "API key format appears valid"

    def validate_openai_config(self) -> Dict[str, any]:
        """Validate OpenAI configuration"""
        result = {
            'provider': 'OpenAI',
            'available': False,
            'issues': [],
            'api_key_valid': False,
            'base_url_valid': False
        }

        # Check API key
        api_key = os.getenv('OPENAI_API_KEY', '')
        key_valid, key_msg = self.validate_api_key(api_key, "OPENAI_API_KEY")
        result['api_key_valid'] = key_valid
        if not key_valid:
            result['issues'].append(f"API Key: {key_msg}")

        # Check base URL (optional for OpenAI)
        base_url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        if base_url and base_url.lower() not in self.PLACEHOLDER_VALUES:
            url_valid, url_msg = self.validate_url(base_url, "OPENAI_API_BASE")
            result['base_url_valid'] = url_valid
            if not url_valid:
                result['issues'].append(f"Base URL: {url_msg}")
        else:
            result['base_url_valid'] = True  # Default is valid

        result['available'] = key_valid and result['base_url_valid']
        return result

    def validate_anthropic_config(self) -> Dict[str, any]:
        """Validate Anthropic configuration"""
        result = {
            'provider': 'Anthropic',
            'available': False,
            'issues': [],
            'api_key_valid': False,
            'base_url_valid': False
        }

        # Check API key
        api_key = os.getenv('ANTHROPIC_API_KEY', '')
        key_valid, key_msg = self.validate_api_key(api_key, "ANTHROPIC_API_KEY")
        result['api_key_valid'] = key_valid
        if not key_valid:
            result['issues'].append(f"API Key: {key_msg}")

        # Check base URL (critical for Anthropic)
        base_url = os.getenv('ANTHROPIC_API_BASE', '')
        if base_url and base_url.lower() not in self.PLACEHOLDER_VALUES:
            url_valid, url_msg = self.validate_url(base_url, "ANTHROPIC_API_BASE")
            result['base_url_valid'] = url_valid
            if not url_valid:
                result['issues'].append(f"Base URL: {url_msg}")
        else:
            # Anthropic can work without explicit base URL
            result['base_url_valid'] = True

        result['available'] = key_valid and result['base_url_valid']
        return result

    def validate_google_config(self) -> Dict[str, any]:
        """Validate Google configuration"""
        result = {
            'provider': 'Google',
            'available': False,
            'issues': [],
            'api_key_valid': False,
            'credentials_valid': False
        }

        # Check API key
        api_key = os.getenv('GOOGLE_API_KEY', '')
        if api_key:
            key_valid, key_msg = self.validate_api_key(api_key, "GOOGLE_API_KEY")
            result['api_key_valid'] = key_valid
            if not key_valid:
                result['issues'].append(f"API Key: {key_msg}")

        # Check credentials file
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
        if creds_path and os.path.exists(creds_path):
            result['credentials_valid'] = True
        elif creds_path:
            result['issues'].append(f"Credentials file not found: {creds_path}")

        # Google needs either API key or credentials
        result['available'] = result['api_key_valid'] or result['credentials_valid']
        if not result['available'] and not result['issues']:
            result['issues'].append("Either GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS required")

        return result

    def validate_local_model_config(self) -> Dict[str, any]:
        """Validate local model configuration"""
        result = {
            'provider': 'Local Models',
            'available': False,
            'issues': [],
            'base_url_valid': False
        }

        # Check Qwen configuration
        qwen_base = os.getenv('QWEN_API_BASE', '')
        if qwen_base and qwen_base.lower() not in self.PLACEHOLDER_VALUES:
            url_valid, url_msg = self.validate_url(qwen_base, "QWEN_API_BASE")
            result['base_url_valid'] = url_valid
            if not url_valid:
                result['issues'].append(f"Qwen Base URL: {url_msg}")
            else:
                result['available'] = True

        return result

    def validate_all_configs(self) -> Dict[str, Dict]:
        """Validate all API configurations

        Returns:
            Dictionary with validation results for each provider
        """
        results = {
            'openai': self.validate_openai_config(),
            'anthropic': self.validate_anthropic_config(),
            'google': self.validate_google_config(),
            'local': self.validate_local_model_config()
        }

        # Store results for later access
        self.validation_results = results

        # Log summary
        available_providers = [name for name, config in results.items() if config['available']]
        logger.info(f"API Validation Complete. Available providers: {available_providers}")

        for name, config in results.items():
            if config['issues']:
                logger.warning(f"{config['provider']} issues: {config['issues']}")

        return results

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        if not self.validation_results:
            self.validate_all_configs()

        return [name for name, config in self.validation_results.items() if config['available']]

    def has_any_valid_provider(self) -> bool:
        """Check if at least one provider is properly configured"""
        return len(self.get_available_providers()) > 0

    def get_configuration_guidance(self) -> str:
        """Generate user-friendly configuration guidance"""
        if not self.validation_results:
            self.validate_all_configs()

        if self.has_any_valid_provider():
            available = self.get_available_providers()
            return f"✅ Configuration OK. Available providers: {', '.join(available)}"

        # No valid providers - provide helpful guidance
        guidance = [
            "❌ No valid API configurations found.",
            "",
            "To fix this, choose one of these options:",
            "",
            "Option 1: Use API Keys",
            "  Edit your .env file and add valid API keys:",
            "  OPENAI_API_KEY=sk-your-actual-openai-key",
            "  ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key",
            "  GOOGLE_API_KEY=your-actual-google-key",
            "",
            "Option 2: Use CLI Tools (Recommended)",
            "  Install Claude Code CLI:",
            "    npm install -g @anthropics/claude-code",
            "  Install Gemini CLI:",
            "    pip install google-generativeai",
            "    gcloud auth application-default login",
            "",
            "Option 3: Use Local Models",
            "  Set up vLLM server and configure:",
            "  QWEN_API_BASE=http://localhost:8000/v1",
            "",
            "Current issues found:"
        ]

        for name, config in self.validation_results.items():
            if config['issues']:
                guidance.append(f"  {config['provider']}: {', '.join(config['issues'])}")

        return "\n".join(guidance)