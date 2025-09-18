#!/usr/bin/env python3
"""
Checks the devices/ folder for repeated model folders, misplaced files, and extra nesting.
Reports any issues found.
"""
import os
from pathlib import Path

DEVICES_DIR = Path(__file__).parent.parent / "devices"

# Allowed structure: devices/<MODEL>/<SERIAL>/<YYYY-MM-DD>/<files>
def is_date_folder(name):
    # Accepts YYYY-MM-DD
    parts = name.split("-")
    return len(parts) == 3 and all(p.isdigit() for p in parts)

def check_structure():
    problems = []
    for model in DEVICES_DIR.iterdir():
        if not model.is_dir() or model.name.startswith("."):
            continue
        # Check for repeated model folders
        for root, dirs, files in os.walk(model):
            rel = Path(root).relative_to(DEVICES_DIR)
            parts = rel.parts
            # Detect repeated model folders
            if parts.count(model.name) > 1:
                problems.append(f"Repeated model folder: {root}")
            # Should be: <MODEL>/<SERIAL>/<YYYY-MM-DD>/
            if len(parts) == 1:
                # Should only contain serial folders
                for d in dirs:
                    if d.startswith(model.name):
                        problems.append(f"Extra model folder nesting: {root}/{d}")
            if len(parts) == 2:
                # Should only contain date folders or 'unknown-date'
                for d in dirs:
                    if not is_date_folder(d) and d != "unknown-date":
                        problems.append(f"Non-date folder under serial: {root}/{d}")
            if len(parts) == 3:
                # Should only contain files
                for d in dirs:
                    problems.append(f"Extra folder under date folder: {root}/{d}")
    if not problems:
        print("No folder structure problems found.")
    else:
        print("Folder structure problems detected:")
        for p in problems:
            print("-", p)

if __name__ == "__main__":
    check_structure()
