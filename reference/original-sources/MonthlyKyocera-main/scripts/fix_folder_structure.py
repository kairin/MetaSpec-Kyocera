#!/usr/bin/env python3
"""
Autofix script for devices/ folder structure.
- Flattens repeated model folders
- Moves files to correct devices/<MODEL>/<SERIAL>/<YYYY-MM-DD>/
- Removes empty/extra folders
"""
import os
import shutil
from pathlib import Path
import re

DEVICES_DIR = Path(__file__).parent.parent / "devices"
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

# Helper: is a date folder
def is_date_folder(name):
    return bool(DATE_PATTERN.fullmatch(name))

# Helper: get all model folders
def get_model_folders():
    return [f for f in DEVICES_DIR.iterdir() if f.is_dir() and not f.name.startswith(".")]

# Helper: flatten repeated model folders
def flatten_model_folders():
    # Aggressively flatten any repeated model folders
    for model in get_model_folders():
        while True:
            # Look for nested model folders
            nested = list((model / model.name).glob('**'))
            if (model / model.name).exists():
                # Move all contents up one level
                for item in (model / model.name).iterdir():
                    dest = model / item.name
                    if dest.exists():
                        # Merge files/folders
                        if item.is_dir():
                            for subitem in item.iterdir():
                                subdest = dest / subitem.name
                                if subdest.exists():
                                    base, ext = subitem.stem, subitem.suffix
                                    i = 1
                                    while (dest / f"{base}_{i}{ext}").exists():
                                        i += 1
                                    subdest = dest / f"{base}_{i}{ext}"
                                shutil.move(str(subitem), str(subdest))
                            item.rmdir()
                        else:
                            base, ext = item.stem, item.suffix
                            i = 1
                            while (model / f"{base}_{i}{ext}").exists():
                                i += 1
                            dest = model / f"{base}_{i}{ext}"
                            shutil.move(str(item), str(dest))
                    else:
                        shutil.move(str(item), str(dest))
                (model / model.name).rmdir()
            else:
                break

# Helper: move files to correct date subfolder
def fix_files_in_serial_folder(serial_folder):
    for item in list(serial_folder.iterdir()):
        if item.is_dir() and is_date_folder(item.name):
            continue
        if item.is_file():
            # Try to extract date from filename
            m = re.search(r"(\d{4}-\d{2}-\d{2})", item.name)
            date_folder = m.group(1) if m else None
            if not date_folder:
                # Try to extract from file content if .eml
                if item.suffix == '.eml':
                    with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    m2 = re.search(r"(\d{4}-\d{2}-\d{2})", content)
                    date_folder = m2.group(1) if m2 else None
            if not date_folder:
                date_folder = "unknown-date"
            target = serial_folder / date_folder
            target.mkdir(exist_ok=True)
            shutil.move(str(item), str(target / item.name))
        elif item.is_dir():
            # Move all files inside this folder up if it's not a date folder
            for subitem in item.iterdir():
                shutil.move(str(subitem), str(serial_folder / subitem.name))
            try:
                item.rmdir()
            except Exception:
                pass

# Main autofix
if __name__ == "__main__":
    print("Autofixing folder structure...")
    flatten_model_folders()
    for model in get_model_folders():
        for serial_folder in model.iterdir():
            if not serial_folder.is_dir():
                continue
            fix_files_in_serial_folder(serial_folder)
    print("Folder structure autofix complete.")
