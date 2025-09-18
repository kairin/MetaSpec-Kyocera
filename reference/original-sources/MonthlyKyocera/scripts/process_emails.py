#!/usr/bin/env python3
"""
Orchestrates email processing:
- For each .eml file in emails/, extracts info, moves folder if needed, generates output files, and logs all actions.
- At the end, writes a summary of all moves and file creations for the current month.
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import re

EMAILS_DIR = Path(__file__).parent.parent / 'emails'
DEVICES_DIR = Path(__file__).parent.parent / 'devices'
SUMMARY_FILE = Path(__file__).parent.parent / 'SUMMARY.md'
ARCHIVE_DIR = Path(__file__).parent.parent / 'archive'
ARCHIVE_DIR.mkdir(exist_ok=True)

# Helper to get current month string
def current_month():
    return datetime.now().strftime('%Y-%m')

def find_serial_and_folder(filename):
    for folder in DEVICES_DIR.iterdir():
        if folder.is_dir():
            parts = folder.name.split('_', 1)
            if len(parts) == 2 and parts[1] in filename:
                return parts[0], parts[1], folder
    return None, None, None

def find_serial_and_folder_recursive(serial):
    """
    Recursively search for a device folder matching the serial number.
    Returns (folder_num, serial, folder_path) or (None, None, None)
    """
    for root, dirs, files in os.walk(DEVICES_DIR):
        for d in dirs:
            parts = d.split('_', 1)
            if len(parts) == 2 and parts[1] == serial:
                return parts[0], parts[1], Path(root) / d
    return None, None, None

def extract_serial_from_text(text):
    """
    Try to extract a Kyocera serial number from text using known patterns.
    """
    # Typical Kyocera serials: W7F3501393, W792300234, etc.
    match = re.search(r'(W[0-9A-Z]{2}[0-9A-Z]{7})', text)
    if match:
        return match.group(1)
    return None

def update_summary(moves, files, errors):
    month = current_month()
    # Archive previous summary if month changed
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines and month not in ''.join(lines[:5]):
            # Archive old summary
            archive_path = ARCHIVE_DIR / f"SUMMARY_{lines[1].strip().replace('# ','').replace(' ','_')}.md"
            shutil.copy(SUMMARY_FILE, archive_path)
    # Write new summary
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Monthly Kyocera Processing Summary\n")
        f.write(f"## {month}\n\n")
        f.write(f"### Folder Moves\n")
        if moves:
            for move in moves:
                f.write(f"- {move}\n")
        else:
            f.write("- No folder moves this run.\n")
        f.write(f"\n### Files Created\n")
        if files:
            for fileinfo in files:
                f.write(f"- {fileinfo}\n")
        else:
            f.write("- No files created this run.\n")
        f.write(f"\n### Errors\n")
        if errors:
            for err in errors:
                f.write(f"- {err}\n")
        else:
            f.write("- No errors this run.\n")
        f.write(f"\n_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")

def main():
    moves = []
    files = []
    errors = []
    for eml_file in EMAILS_DIR.glob("*.eml"):
        try:
            # 1. Try to extract serial from filename
            serial = extract_serial_from_text(eml_file.name)
            # 2. If not found, try to extract from file content (subject/body)
            if not serial:
                with open(eml_file, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_content = f.read()
                serial = extract_serial_from_text(raw_content)
            if not serial:
                errors.append(f"{eml_file.name}: Could not extract serial from filename or content.")
                continue
            # 3. Recursively find device folder
            folder_num, found_serial, device_folder = find_serial_and_folder_recursive(serial)
            if not (folder_num and found_serial and device_folder):
                errors.append(f"{eml_file.name}: Could not find device folder for serial {serial}.")
                continue
            # 4. Extract info from email
            result = subprocess.run([
                sys.executable, str(Path(__file__).parent / 'extract_email_info.py'), str(eml_file)
            ], capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"{eml_file.name}: Failed to extract info. {result.stderr.strip()}")
                continue
            info = json.loads(result.stdout)
            body, email_date, model = info['body'], info['email_date'], info['model']
            # 5. Post-conversion: verify serial in body
            serial_in_body = extract_serial_from_text(body)
            if not serial_in_body or serial_in_body != serial:
                errors.append(f"{eml_file.name}: Serial mismatch or not found in converted text. Found: {serial_in_body}, Expected: {serial}")
                continue
            # 6. Check for meter/counter keywords
            if not any(kw in body for kw in ["MeterDate", "Counters", "Serial Number"]):
                errors.append(f"{eml_file.name}: Converted text missing expected meter/counter keywords.")
                continue
            # 7. Move device folder if needed
            move_result = subprocess.run([
                sys.executable, str(Path(__file__).parent / 'move_device_folder.py'), str(device_folder.resolve()), model or ''
            ], capture_output=True, text=True)
            move_msg = move_result.stdout.strip()
            if move_msg:
                moves.append(move_msg)
                # Always resolve device_folder to avoid double-nesting
                model_folder = 'TASKalfa-5054ci' if model == 'TASKalfa 5054ci' else ('TASKalfa-5004i' if model == 'TASKalfa 5004i' else None)
                if model_folder:
                    device_folder = (DEVICES_DIR / model_folder / device_folder.name).resolve()
            else:
                # If already in correct place, resolve path
                model_folder = 'TASKalfa-5054ci' if model == 'TASKalfa 5054ci' else ('TASKalfa-5004i' if model == 'TASKalfa 5004i' else None)
                if model_folder and device_folder.parent.name == model_folder:
                    device_folder = (DEVICES_DIR / model_folder / device_folder.name).resolve()
            # 7.1 Ensure output goes to correct date subfolder
            current_date = datetime.now().strftime('%Y-%m-%d')
            date_folder = device_folder / current_date
            date_folder.mkdir(parents=True, exist_ok=True)
            # 8. Prepare output file base name
            model_str = model.replace(' ', '') if model else 'UnknownModel'
            base_name = f"{email_date}_{model_str}_{serial}_{current_date}_meter_reading"
            output_base = date_folder / base_name
            # 9. Avoid overwriting: add suffix if file exists
            suffix = 1
            txt_path = output_base.with_suffix('.txt')
            pdf_path = output_base.with_suffix('.pdf')
            while txt_path.exists() or pdf_path.exists():
                output_base = date_folder / f"{base_name}_{suffix}"
                txt_path = output_base.with_suffix('.txt')
                pdf_path = output_base.with_suffix('.pdf')
                suffix += 1
            # 10. Write body to temp file for generate_output_files.py
            tmp_body = date_folder / (output_base.name + '.tmp')
            with open(tmp_body, 'w', encoding='utf-8') as f:
                f.write(body)
            # 11. Generate .txt and .pdf
            gen_result = subprocess.run([
                sys.executable, str(Path(__file__).parent / 'generate_output_files.py'), str(tmp_body), str(output_base)
            ], capture_output=True, text=True)
            os.remove(tmp_body)
            if gen_result.returncode != 0:
                errors.append(f"{eml_file.name}: Failed to generate output files. {gen_result.stderr.strip()}")
                continue
            files.append(f"{txt_path.name} in {date_folder}")
            files.append(f"{pdf_path.name} in {date_folder}")
            # 12. Move .eml
            shutil.move(str(eml_file), date_folder / eml_file.name)
            files.append(f"{eml_file.name} moved to {date_folder}")
        except Exception as e:
            errors.append(f"{eml_file.name}: {e}")
    update_summary(moves, files, errors)

if __name__ == "__main__":
    main()
