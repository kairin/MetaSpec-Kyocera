#!/usr/bin/env python3
"""
Moves a device folder to the correct model subfolder if needed.
Usage: python3 move_device_folder.py <device_folder> <model>
Prints the move action as a string if a move was performed, else prints nothing.
"""
import sys
import shutil
from pathlib import Path

MODEL_FOLDERS = {
    'TASKalfa 5054ci': 'TASKalfa-5054ci',
    'TASKalfa 5004i': 'TASKalfa-5004i',
}

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 move_device_folder.py <device_folder> <model>", file=sys.stderr)
        sys.exit(1)
    device_folder = Path(sys.argv[1]).resolve()
    model = sys.argv[2]
    if model in MODEL_FOLDERS:
        model_folder_name = MODEL_FOLDERS[model]
        # If already inside any model folder, move to correct model folder root (not nested)
        parent = device_folder.parent
        if parent.name in MODEL_FOLDERS.values():
            # If already in correct model folder, do nothing
            if parent.name == model_folder_name:
                print("")
                return
            # If in wrong model folder, move to correct one
            dest_dir = device_folder.parents[1] / model_folder_name
        else:
            dest_dir = device_folder.parent / model_folder_name
        dest_dir.mkdir(exist_ok=True)
        dest_folder = dest_dir / device_folder.name
        if not dest_folder.exists():
            shutil.move(str(device_folder), str(dest_folder))
            print(f"Moved {device_folder} to {dest_folder}")
        else:
            print("")
    else:
        print("")

if __name__ == "__main__":
    main()
