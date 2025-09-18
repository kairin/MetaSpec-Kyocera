"""
Pytest configuration and shared fixtures for MonthlyKyocera testing.
"""
import pytest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage
from email import policy

# Test data constants
SAMPLE_SERIALS = ["W7F3501393", "W792300234", "W7F3601610", "W7F3501399"]
SAMPLE_MODELS = ["TASKalfa 5054ci", "TASKalfa 5004i"]

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test isolation."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def project_root():
    """Return the absolute path to the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def scripts_dir(project_root):
    """Return the path to the scripts directory."""
    return project_root / "scripts"

@pytest.fixture
def sample_email_data():
    """Provide sample email data for testing."""
    return {
        "subject": "TASKalfa 5054ci - W7F3501393 - Counter Report",
        "sender": "kyocera@example.com",
        "date": "Wed, 15 Sep 2025 10:30:00 +0000",
        "body": """MeterDate: 2025-09-15
Device Type: TASKalfa 5054ci
Serial Number: W7F3501393
Model Name: TASKalfa 5054ci

Counters:
Total Counter: 123456
Copy Counter: 98765
Print Counter: 24691
Scan Counter: 12345
Fax Counter: 4567
""",
        "serial": "W7F3501393",
        "model": "TASKalfa 5054ci"
    }

@pytest.fixture
def create_test_eml_file(temp_dir):
    """Factory function to create test .eml files."""
    def _create_eml(email_data, filename="test_email.eml"):
        msg = EmailMessage(policy=policy.default)
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['sender']
        msg['Date'] = email_data['date']
        msg.set_content(email_data['body'])
        
        eml_path = temp_dir / filename
        with open(eml_path, 'wb') as f:
            f.write(msg.as_bytes())
        
        return eml_path
    
    return _create_eml

@pytest.fixture
def mock_device_structure(temp_dir):
    """Create a mock device directory structure for testing."""
    devices_dir = temp_dir / "devices"
    devices_dir.mkdir()
    
    # Create sample device folders
    device_folders = [
        "001_W7F3501393",
        "002_W792300234", 
        "003_W7F3601610"
    ]
    
    for folder in device_folders:
        (devices_dir / folder).mkdir()
        # Create subdirectories for dates
        date_folder = devices_dir / folder / "2025-09-15"
        date_folder.mkdir(parents=True)
    
    return devices_dir

@pytest.fixture
def sample_extraction_result():
    """Expected result from email info extraction."""
    return {
        "body": """MeterDate: 2025-09-15
Device Type: TASKalfa 5054ci
Serial Number: W7F3501393
Model Name: TASKalfa 5054ci

Counters:
Total Counter: 123456
Copy Counter: 98765
Print Counter: 24691
Scan Counter: 12345
Fax Counter: 4567
""",
        "email_date": "2025-09-15",
        "model": "TASKalfa 5054ci"
    }

@pytest.fixture
def invalid_email_data():
    """Email data with various issues for negative testing."""
    return [
        {
            "name": "missing_serial",
            "subject": "TASKalfa 5054ci - Counter Report",
            "body": "MeterDate: 2025-09-15\nCounters: some data",
            "expected_error": "Could not extract serial"
        },
        {
            "name": "invalid_serial_format", 
            "subject": "Invalid Serial - ABC123456",
            "body": "Serial Number: ABC123456\nCounters: data",
            "expected_error": "Could not extract serial"
        },
        {
            "name": "missing_counter_data",
            "subject": "TASKalfa 5054ci - W7F3501393",
            "body": "Just some random text without meter data",
            "expected_error": "missing expected meter/counter keywords"
        }
    ]
