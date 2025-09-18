#!/usr/bin/env python3
"""
Reorganize repository with device-centric structure
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def load_registry(base_path):
    """Load the master device registry"""
    registry_file = Path(base_path) / 'device_registry' / 'master_device_registry.json'
    with open(registry_file, 'r') as f:
        return json.load(f)

def create_device_structure(base_path):
    """Create the new device-centric folder structure"""
    registry = load_registry(base_path)
    devices_root = Path(base_path) / 'devices'
    
    print("Creating device-centric structure...")
    
    for serial, device in registry.items():
        # Create device folder
        device_path = devices_root / device['model'].replace(' ', '_') / serial
        device_path.mkdir(parents=True, exist_ok=True)
        
        # Create subfolders
        (device_path / 'scans').mkdir(exist_ok=True)
        (device_path / 'emails' / 'counter').mkdir(parents=True, exist_ok=True)
        (device_path / 'emails' / 'toner').mkdir(parents=True, exist_ok=True)
        (device_path / 'emails' / 'other').mkdir(parents=True, exist_ok=True)
        (device_path / 'reports').mkdir(exist_ok=True)
        (device_path / 'processed').mkdir(exist_ok=True)
        
        # Create device info file
        info_file = device_path / 'DEVICE_INFO.md'
        with open(info_file, 'w') as f:
            f.write(f"# Device Information: {serial}\n\n")
            f.write(f"**Model**: {device['model']}\n")
            f.write(f"**Location**: {device['location']}\n")
            f.write(f"**IP/URL**: {device['ip_url']}\n")
            f.write(f"**Email**: {device['email_address']}\n")
            f.write(f"**Device Number**: {device['device_number']}\n\n")
            f.write("## Data Sources\n")
            f.write(f"- Scans: {device['scan_count']} files\n")
            f.write(f"- Counter Emails: {device['counter_emails']}\n")
            f.write(f"- Toner Emails: {device['toner_emails']}\n")
            f.write(f"- Other Emails: {device['other_emails']}\n\n")
            f.write("## File Structure\n")
            f.write("```\n")
            f.write(f"{serial}/\n")
            f.write("├── DEVICE_INFO.md (this file)\n")
            f.write("├── scans/         (device screenshots)\n")
            f.write("├── emails/        (email files)\n")
            f.write("│   ├── counter/   (meter reading emails)\n")
            f.write("│   ├── toner/     (toner alert emails)\n")
            f.write("│   └── other/     (other emails)\n")
            f.write("├── reports/       (generated reports)\n")
            f.write("└── processed/     (processed data)\n")
            f.write("```\n")
        
        # Link scan files (preserve originals)
        scan_source = Path(base_path) / 'Kyocera-scan' / serial
        if scan_source.exists():
            for scan_file in scan_source.glob('*'):
                if scan_file.is_file():
                    dest = device_path / 'scans' / scan_file.name
                    if not dest.exists():
                        shutil.copy2(scan_file, dest)
        
        # Link email files (preserve originals)
        email_source = Path(base_path) / 'emails' / 'organized' / 'by-serial' / serial
        if email_source.exists():
            for email_file in email_source.glob('*'):
                if email_file.is_file():
                    # Determine email type
                    if 'counter' in email_file.name.lower():
                        dest_folder = device_path / 'emails' / 'counter'
                    elif 'toner' in email_file.name.lower():
                        dest_folder = device_path / 'emails' / 'toner'
                    else:
                        dest_folder = device_path / 'emails' / 'other'
                    
                    dest = dest_folder / email_file.name
                    if not dest.exists():
                        shutil.copy2(email_file, dest)
    
    print(f"✅ Created device structure for {len(registry)} devices")

def create_repository_index(base_path):
    """Create main repository index"""
    registry = load_registry(base_path)
    
    index_file = Path(base_path) / 'REPOSITORY_INDEX.md'
    with open(index_file, 'w') as f:
        f.write('# Kyocera Meter Reading Repository Index\n\n')
        f.write(f'**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        f.write('## Repository Structure\n\n')
        f.write('```\n')
        f.write('MonthlyKyocera/\n')
        f.write('├── REPOSITORY_INDEX.md     (this file)\n')
        f.write('├── devices/                (main device data - organized by model/serial)\n')
        f.write('├── device_registry/        (master device registry and metadata)\n')
        f.write('├── Kyocera-scan/          (original scan files - preserved)\n')
        f.write('├── emails/                (original email files - preserved)\n')
        f.write('│   ├── originals/         (backup of all emails)\n')
        f.write('│   ├── organized/         (emails organized by serial/type)\n')
        f.write('│   └── *.csv              (device inventory data)\n')
        f.write('├── scripts/               (processing scripts)\n')
        f.write('├── specs/                 (specifications and documentation)\n')
        f.write('└── visuals/              (project visualizations)\n')
        f.write('```\n\n')
        
        f.write('## Quick Access\n\n')
        f.write('### Key Documents\n')
        f.write('- [Device Registry](device_registry/DEVICE_REGISTRY.md)\n')
        f.write('- [Project Status](PROJECT_STATUS.md)\n')
        f.write('- [Project Visualization](PROJECT_VISUALIZATION.md)\n')
        f.write('- [Email Organization Report](emails/ORGANIZATION_REPORT.md)\n\n')
        
        f.write('### Device Models\n')
        models = {}
        for device in registry.values():
            model = device['model'] or 'Unknown'
            if model not in models:
                models[model] = []
            models[model].append(device['serial_number'])
        
        for model, serials in sorted(models.items()):
            f.write(f'- **{model}**: {len(serials)} devices\n')
            for serial in sorted(serials)[:5]:  # Show first 5
                device_path = f"devices/{model.replace(' ', '_')}/{serial}/"
                f.write(f'  - [{serial}]({device_path})\n')
            if len(serials) > 5:
                f.write(f'  - ... and {len(serials) - 5} more\n')
        
        f.write('\n## Processing Status\n')
        f.write('- ✅ Device registry created\n')
        f.write('- ✅ Emails organized by serial\n')
        f.write('- ✅ Scans linked to devices\n')
        f.write('- ⏳ Ready for agent processing\n')
    
    print(f"✅ Created repository index")

if __name__ == '__main__':
    base_path = Path.cwd()
    create_device_structure(base_path)
    create_repository_index(base_path)