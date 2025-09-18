"""Compatibility Warnings Manager

Manages compatibility issues and warnings, suppressing known non-critical warnings
while logging what's being suppressed for transparency.
"""

import warnings
import sys
import logging

logger = logging.getLogger(__name__)


class CompatibilityManager:
    """Manages compatibility issues and warnings"""

    def __init__(self):
        self.suppressed_warnings = []
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

    def suppress_known_warnings(self):
        """Suppress known, non-critical warnings"""

        # Pydantic v1 deprecation warnings (scheduled for Phase 1 fix)
        warnings.filterwarnings(
            'ignore',
            message='.*Pydantic.*deprecated.*',
            category=DeprecationWarning
        )
        self.suppressed_warnings.append("Pydantic v1 deprecation warnings")

        # Pydantic v2 migration warnings
        warnings.filterwarnings(
            'ignore',
            message='.*pydantic.*BaseModel.*',
            category=DeprecationWarning
        )

        warnings.filterwarnings(
            'ignore',
            message='.*pydantic.*Field.*',
            category=DeprecationWarning
        )

        # Python 3.13 aifc module removal warnings
        if sys.version_info >= (3, 13):
            warnings.filterwarnings(
                'ignore',
                message='.*aifc.*removed.*',
                category=DeprecationWarning
            )
            self.suppressed_warnings.append("Python 3.13 aifc module warnings")

        # Python 3.13 other deprecated modules
        deprecated_modules_313 = ['audioop', 'chunk', 'cgi', 'cgitb', 'crypt']
        for module in deprecated_modules_313:
            warnings.filterwarnings(
                'ignore',
                message=f'.*{module}.*deprecated.*',
                category=DeprecationWarning
            )

        # OpenAI API deprecation warnings
        warnings.filterwarnings(
            'ignore',
            message='.*openai.*deprecated.*',
            category=DeprecationWarning
        )

        # Anthropic API warnings
        warnings.filterwarnings(
            'ignore',
            message='.*anthropic.*deprecated.*',
            category=DeprecationWarning
        )

        # httpx warnings for invalid protocols (we handle these gracefully)
        warnings.filterwarnings(
            'ignore',
            message='.*UnsupportedProtocol.*',
            category=UserWarning
        )

        # Async warnings that are expected in our architecture
        warnings.filterwarnings(
            'ignore',
            message='.*asyncio.*deprecated.*',
            category=DeprecationWarning
        )

        # Suppress urllib3 warnings for unverified HTTPS requests (if configured)
        warnings.filterwarnings(
            'ignore',
            message='.*Unverified HTTPS.*',
            category=Warning
        )

    def suppress_development_warnings(self):
        """Suppress warnings that are only relevant during development"""

        # Jupyter/IPython warnings in non-interactive environments
        warnings.filterwarnings(
            'ignore',
            message='.*IPython.*',
            category=UserWarning
        )

        # Matplotlib warnings for headless environments
        warnings.filterwarnings(
            'ignore',
            message='.*matplotlib.*GUI.*',
            category=UserWarning
        )

        # Pytest warnings when running outside pytest
        warnings.filterwarnings(
            'ignore',
            message='.*pytest.*',
            category=DeprecationWarning
        )

    def log_suppressed_warnings(self):
        """Log what warnings we're suppressing and why"""
        if self.suppressed_warnings:
            logger.info("Compatibility: Suppressing known warnings:")
            for warning in self.suppressed_warnings:
                logger.info(f"  - {warning}")
            logger.info("These warnings are scheduled for resolution in Phase 1")
        else:
            logger.info("Compatibility: No warnings suppressed")

        logger.info(f"Python version: {self.python_version}")

    def apply_compatibility_fixes(self):
        """Apply all compatibility fixes"""
        logger.info("Applying compatibility fixes...")

        self.suppress_known_warnings()
        self.suppress_development_warnings()
        self.log_suppressed_warnings()

        logger.info("Compatibility fixes applied successfully")

    def check_python_compatibility(self) -> dict:
        """Check Python version compatibility"""
        version_info = {
            'version': self.python_version,
            'version_tuple': sys.version_info,
            'compatible': True,
            'warnings': [],
            'recommendations': []
        }

        # Check for Python 3.13 specific issues
        if sys.version_info >= (3, 13):
            version_info['warnings'].append(
                "Python 3.13 detected - some modules have been removed"
            )
            version_info['recommendations'].append(
                "Consider updating deprecated code in Phase 1"
            )

        # Check for minimum version
        if sys.version_info < (3, 8):
            version_info['compatible'] = False
            version_info['warnings'].append(
                "Python version too old - minimum 3.8 required"
            )

        # Check for recommended version
        if sys.version_info < (3, 10):
            version_info['recommendations'].append(
                "Consider upgrading to Python 3.10+ for better performance"
            )

        return version_info

    def handle_import_errors(self, module_name: str, error: ImportError) -> str:
        """Handle import errors with helpful suggestions

        Args:
            module_name: Name of the module that failed to import
            error: The ImportError that occurred

        Returns:
            Helpful error message with suggestions
        """
        error_msg = str(error)

        # Common import error patterns and solutions
        if "No module named" in error_msg:
            return (
                f"Module '{module_name}' not found. "
                f"Try: uv add {module_name}"
            )

        if "cannot import name" in error_msg:
            return (
                f"Import error in '{module_name}'. "
                f"This may be due to version incompatibility. "
                f"Try: uv add {module_name} --upgrade"
            )

        if "DLL load failed" in error_msg or "library not found" in error_msg:
            return (
                f"System library missing for '{module_name}'. "
                f"Check system dependencies in documentation."
            )

        return f"Import error for '{module_name}': {error_msg}"


# Global instance for easy access
compatibility_manager = CompatibilityManager()