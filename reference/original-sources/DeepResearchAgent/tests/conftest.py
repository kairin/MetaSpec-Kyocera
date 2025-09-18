import os
import sys
from pathlib import Path

# Add the project root to the Python path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

# Set up environment variables for testing
os.environ.setdefault('PYTHONPATH', str(root))

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on path."""
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker("unit")
        elif "integration" in str(item.fspath):
            item.add_marker("integration")
        elif "e2e" in str(item.fspath):
            item.add_marker("e2e")
