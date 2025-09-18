#!/usr/bin/env python3
"""
Script to list all available serial numbers from device folders directly under devices/ and within TASKalfa-5004i and TASKalfa-5054ci subfolders.
"""
from pathlib import Path

DEVICES_DIR = Path(__file__).parent.parent / 'devices'
MODEL_FOLDERS = ['TASKalfa-5054ci', 'TASKalfa-5004i']

serials = set()

def extract_serial(folder_name):
    parts = folder_name.split('_', 1)
    if len(parts) == 2:
        return parts[1]
    return None

def list_serials():
    # Top-level device folders
    for folder in DEVICES_DIR.iterdir():
        if folder.is_dir() and not folder.name.startswith('TASKalfa-'):
            serial = extract_serial(folder.name)
            if serial:
                serials.add(serial)
    # Model subfolders
    for model in MODEL_FOLDERS:
        model_path = DEVICES_DIR / model
        if model_path.exists():
            for folder in model_path.iterdir():
                if folder.is_dir():
                    serial = extract_serial(folder.name)
                    if serial:
                        serials.add(serial)
    return sorted(serials)

def main():
    found_serials = list_serials()
    print("Available serial numbers:")
    for s in found_serials:
        print(f"- {s}")

if __name__ == "__main__":
    main()
