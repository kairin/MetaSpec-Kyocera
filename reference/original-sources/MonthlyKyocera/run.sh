#!/bin/bash
# Quick runner for MonthlyKyocera processing (Linux)
set -e

SCRIPTS_DIR="$(dirname "$0")/scripts"

# Step 0: Autofix folder structure
echo "--- Step 0: Autofixing folder structure ---"
python3 "$SCRIPTS_DIR/fix_folder_structure.py"

# Step 1: Checking system date
echo "--- Step 1: Checking system date ---"
python3 "$SCRIPTS_DIR/date_check.py"

# Step 2: Processing emails
echo "\n--- Step 2: Processing emails ---"
python3 "$SCRIPTS_DIR/process_emails.py"

# Step 3: Updating device status
echo "\n--- Step 3: Updating device status ---"
python3 "$SCRIPTS_DIR/update_device_status_md.py"

# Step 4: Verifying folder structure
echo "\n--- Step 4: Verifying folder structure ---"
VERIFY_OUT=$(python3 "$SCRIPTS_DIR/check_folder_structure.py")
if echo "$VERIFY_OUT" | grep -q "problems detected"; then
  echo "$VERIFY_OUT"
  echo "WARNING: Folder structure problems remain. Please review the output above."
else
  echo "Folder structure verified: OK."
fi
