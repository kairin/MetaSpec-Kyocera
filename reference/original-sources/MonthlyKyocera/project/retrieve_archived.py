#!/usr/bin/env python3
"""
Retrieve archived files by original name or pattern
"""
import json
import shutil
from pathlib import Path
import sys

def retrieve_file(search_term, output_dir='.'):
    mapping_file = Path('.archive/file_mapping.json')
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)
    
    found = []
    for file_id, info in mapping['files'].items():
        if search_term.lower() in info['original_name'].lower():
            found.append(info)
    
    if not found:
        print(f"No files found matching: {search_term}")
        return
    
    print(f"Found {len(found)} files:")
    for i, info in enumerate(found, 1):
        print(f"{i}. {info['original_name']}")
        print(f"   Archived as: {info['archive_name']}")
        print(f"   Serial: {info.get('serial', 'N/A')}")
    
    if len(found) == 1:
        choice = 1
    else:
        choice = int(input("\nSelect file number to retrieve (0 to cancel): "))
        if choice == 0:
            return
    
    selected = found[choice - 1]
    source = Path(selected['archive_path'])
    dest = Path(output_dir) / selected['original_name']
    
    shutil.copy2(source, dest)
    print(f"\n✓ Retrieved to: {dest}")

if __name__ == '__main__':
    search = input("Enter filename or pattern to search: ")
    retrieve_file(search)
