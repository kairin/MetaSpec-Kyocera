#!/usr/bin/env python3
"""
Orchestrator script to:
1. Print the current system date (calls scripts/date_check.py)
2. Run the email processing script (calls scripts/process_emails.py)
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / 'scripts'

def main():
    print("--- Step 0: Autofixing folder structure ---")
    subprocess.run([sys.executable, str(SCRIPTS_DIR / 'fix_folder_structure.py')], check=True)
    print("--- Step 1: Checking system date ---")
    subprocess.run([sys.executable, str(SCRIPTS_DIR / 'date_check.py')], check=True)
    print("\n--- Step 2: Processing emails ---")
    subprocess.run([sys.executable, str(SCRIPTS_DIR / 'process_emails.py')], check=True)
    print("\n--- Step 3: Updating device status ---")
    subprocess.run([sys.executable, str(SCRIPTS_DIR / 'update_device_status_md.py')], check=True)
    print("\n--- Step 4: Verifying folder structure ---")
    result = subprocess.run([sys.executable, str(SCRIPTS_DIR / 'check_folder_structure.py')], capture_output=True, text=True)
    if "problems detected" in result.stdout:
        print(result.stdout)
        print("WARNING: Folder structure problems remain. Please review the output above.")
    else:
        print("Folder structure verified: OK.")

if __name__ == "__main__":
    main()
