#!/usr/bin/env python3
"""
Create a master device registry from all sources:
1. Kyocera-scan folder (primary source)
2. Device inventory CSV
3. Email files
"""

import csv
import json
import os
from pathlib import Path
from collections import defaultdict

def parse_device_inventory(csv_file):
    """Parse the device inventory CSV file"""
    devices = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            serial = row.get('Device Serial #', '').strip()
            if serial and serial.startswith('W'):
                devices[serial] = {
                    'model': row.get('Device Model', '').strip().replace(',', ''),
                    'location': row.get('Device Location', '').strip(),
                    'ip_url': row.get('Column1', '').strip(),  # IP/URL column
                    'email_address': row.get('Device Email Address', '').strip(),
                    'device_number': row.get('No #', '').strip().replace('-', '').strip()
                }
    return devices

def scan_kyocera_folders(base_path):
    """Scan Kyocera-scan folders for device information"""
    devices = {}
    kyocera_path = Path(base_path) / 'Kyocera-scan'
    
    for folder in kyocera_path.iterdir():
        if folder.is_dir() and folder.name.startswith('W'):
            serial = folder.name
            screenshots = list(folder.glob('*.png')) + list(folder.glob('*.jpg'))
            devices[serial] = {
                'has_scans': True,
                'scan_count': len(screenshots),
                'scan_files': [f.name for f in screenshots]
            }
    return devices

def scan_email_files(base_path):
    """Scan email files for device information"""
    email_devices = defaultdict(lambda: {'counter_emails': 0, 'toner_emails': 0, 'other_emails': 0})
    emails_path = Path(base_path) / 'emails' / 'organized' / 'by-serial'
    
    if emails_path.exists():
        for serial_folder in emails_path.iterdir():
            if serial_folder.is_dir() and serial_folder.name.startswith('W'):
                serial = serial_folder.name
                for email_file in serial_folder.iterdir():
                    if 'Counter' in email_file.name or 'counter' in email_file.name.lower():
                        email_devices[serial]['counter_emails'] += 1
                    elif 'Toner' in email_file.name or 'toner' in email_file.name.lower():
                        email_devices[serial]['toner_emails'] += 1
                    else:
                        email_devices[serial]['other_emails'] += 1
    
    return dict(email_devices)

def create_master_registry(base_path):
    """Create master device registry combining all sources"""
    
    # Get data from all sources
    inventory = parse_device_inventory(Path(base_path) / 'emails' / 'Devices in ITE CW-with-ip-add.csv')
    scans = scan_kyocera_folders(base_path)
    emails = scan_email_files(base_path)
    
    # Combine all serials
    all_serials = set(inventory.keys()) | set(scans.keys()) | set(emails.keys())
    
    # Build master registry
    master_registry = {}
    
    for serial in sorted(all_serials):
        device = {
            'serial_number': serial,
            'model': '',
            'location': '',
            'ip_url': '',
            'email_address': '',
            'device_number': '',
            'has_scans': False,
            'scan_count': 0,
            'scan_files': [],
            'counter_emails': 0,
            'toner_emails': 0,
            'other_emails': 0,
            'total_emails': 0,
            'data_sources': []
        }
        
        # Add inventory data
        if serial in inventory:
            device.update(inventory[serial])
            device['data_sources'].append('inventory')
        
        # Add scan data
        if serial in scans:
            device.update(scans[serial])
            device['data_sources'].append('scans')
        
        # Add email data
        if serial in emails:
            device.update(emails[serial])
            device['total_emails'] = (emails[serial]['counter_emails'] + 
                                     emails[serial]['toner_emails'] + 
                                     emails[serial]['other_emails'])
            device['data_sources'].append('emails')
        
        # Determine model from serial prefix if not in inventory
        if not device['model']:
            if serial.startswith('W7F'):
                device['model'] = 'TASKalfa 5004i'
            elif serial.startswith('W79'):
                if serial.startswith('W794'):
                    device['model'] = 'TASKalfa 5054ci'
                elif serial.startswith('W793'):
                    device['model'] = 'TASKalfa 5054ci'
                elif serial.startswith('W792'):
                    device['model'] = 'TASKalfa 5054ci'
        
        master_registry[serial] = device
    
    return master_registry

def save_registry(registry, base_path):
    """Save registry in multiple formats"""
    output_dir = Path(base_path) / 'device_registry'
    output_dir.mkdir(exist_ok=True)
    
    # Save as JSON
    with open(output_dir / 'master_device_registry.json', 'w') as f:
        json.dump(registry, f, indent=2)
    
    # Save as Markdown
    with open(output_dir / 'DEVICE_REGISTRY.md', 'w') as f:
        f.write('# Master Device Registry\n\n')
        f.write(f'**Total Devices**: {len(registry)}\n\n')
        
        # Summary statistics
        with_scans = sum(1 for d in registry.values() if d['has_scans'])
        with_emails = sum(1 for d in registry.values() if d['total_emails'] > 0)
        with_inventory = sum(1 for d in registry.values() if 'inventory' in d['data_sources'])
        
        f.write('## Data Coverage\n')
        f.write(f'- Devices with scans: {with_scans}\n')
        f.write(f'- Devices with emails: {with_emails}\n')
        f.write(f'- Devices in inventory: {with_inventory}\n\n')
        
        # Device table
        f.write('## Device Details\n\n')
        f.write('| Serial | Model | Location | Scans | Emails | Sources |\n')
        f.write('|--------|-------|----------|-------|--------|----------|\n')
        
        for serial, device in sorted(registry.items()):
            sources = ', '.join(device['data_sources'])
            f.write(f"| {serial} | {device['model']} | {device['location'][:30]}... | "
                   f"{device['scan_count']} | {device['total_emails']} | {sources} |\n")
    
    print(f"✅ Registry saved to {output_dir}")
    print(f"   - Total devices: {len(registry)}")
    print(f"   - With scans: {with_scans}")
    print(f"   - With emails: {with_emails}")
    print(f"   - In inventory: {with_inventory}")

if __name__ == '__main__':
    base_path = Path.cwd()
    registry = create_master_registry(base_path)
    save_registry(registry, base_path)