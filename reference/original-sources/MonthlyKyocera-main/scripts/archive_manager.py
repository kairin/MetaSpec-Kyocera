#!/usr/bin/env python3
"""
Archive Manager - Intelligently archive files with short names and mapping
"""

import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
import yaml

class ArchiveManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.archive_root = self.base_path / '.archive'
        self.archive_root.mkdir(exist_ok=True)
        
        # Create archive subdirectories
        self.dirs = {
            'emails': self.archive_root / 'emails',
            'scans': self.archive_root / 'scans',
            'docs': self.archive_root / 'docs',
            'data': self.archive_root / 'data'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(exist_ok=True)
        
        self.mapping_file = self.archive_root / 'file_mapping.json'
        self.mapping = self.load_mapping()
        self.stats = {'moved': 0, 'errors': 0, 'skipped': 0}
    
    def load_mapping(self):
        """Load existing mapping or create new"""
        if self.mapping_file.exists():
            with open(self.mapping_file, 'r') as f:
                return json.load(f)
        return {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'files': {},
            'index': {}
        }
    
    def save_mapping(self):
        """Save mapping to file"""
        with open(self.mapping_file, 'w') as f:
            json.dump(self.mapping, f, indent=2)
        
        # Also save as YAML for readability
        yaml_file = self.archive_root / 'file_mapping.yaml'
        with open(yaml_file, 'w') as f:
            yaml.dump(self.mapping, f, default_flow_style=False)
    
    def generate_short_name(self, original_path, file_type):
        """Generate short filename based on content hash and type"""
        # Get file extension
        ext = original_path.suffix.lower()
        
        # Generate hash from original filename for uniqueness
        hash_obj = hashlib.md5(str(original_path).encode())
        short_hash = hash_obj.hexdigest()[:8]
        
        # Determine prefix based on file type
        prefixes = {
            'eml': 'E',
            'msg': 'M', 
            'png': 'S',
            'jpg': 'S',
            'jpeg': 'S',
            'pdf': 'P',
            'ods': 'D',
            'csv': 'D',
            'txt': 'T',
            'md': 'T'
        }
        
        prefix = prefixes.get(ext[1:], 'X')
        
        # Extract device serial if present in path or filename
        serial = self.extract_serial(original_path)
        if serial:
            # Format: P_SERIAL_HASH.ext (e.g., E_W7F3601552_a3b2c1d4.eml)
            short_name = f"{prefix}_{serial}_{short_hash}{ext}"
        else:
            # Format: P_HASH.ext (e.g., D_a3b2c1d4.csv)
            short_name = f"{prefix}_{short_hash}{ext}"
        
        return short_name
    
    def extract_serial(self, path):
        """Extract device serial from path or filename"""
        import re
        path_str = str(path)
        # Look for serial pattern (W followed by 9-10 alphanumeric)
        match = re.search(r'(W[0-9A-Z]{9,10})', path_str)
        return match.group(1) if match else None
    
    def determine_archive_dir(self, file_path):
        """Determine which archive directory to use"""
        ext = file_path.suffix.lower()
        name_lower = file_path.name.lower()
        
        if ext in ['.eml', '.msg']:
            return self.dirs['emails']
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self.dirs['scans']
        elif ext in ['.ods', '.csv', '.xls', '.xlsx']:
            return self.dirs['data']
        elif ext in ['.pdf', '.txt', '.md', '.yaml', '.json']:
            return self.dirs['docs']
        else:
            return self.dirs['data']
    
    def archive_file(self, source_path, preserve_original=False):
        """Archive a single file with short name"""
        source_path = Path(source_path)
        
        if not source_path.exists():
            self.stats['errors'] += 1
            return None
        
        # Determine archive directory
        archive_dir = self.determine_archive_dir(source_path)
        
        # Generate short name
        short_name = self.generate_short_name(source_path, archive_dir.name)
        dest_path = archive_dir / short_name
        
        # Handle duplicates
        counter = 1
        while dest_path.exists():
            base_name = short_name.rsplit('.', 1)[0]
            ext = short_name.rsplit('.', 1)[1]
            short_name = f"{base_name}_{counter}.{ext}"
            dest_path = archive_dir / short_name
            counter += 1
        
        # Move or copy file
        if preserve_original:
            shutil.copy2(source_path, dest_path)
        else:
            shutil.move(str(source_path), str(dest_path))
        
        # Update mapping
        file_id = dest_path.stem
        self.mapping['files'][file_id] = {
            'original_name': source_path.name,
            'original_path': str(source_path.relative_to(self.base_path)),
            'archive_name': short_name,
            'archive_path': str(dest_path.relative_to(self.base_path)),
            'file_size': dest_path.stat().st_size,
            'archived_at': datetime.now().isoformat(),
            'serial': self.extract_serial(source_path),
            'type': archive_dir.name
        }
        
        # Update index for quick lookups
        self.mapping['index'][source_path.name] = file_id
        
        self.stats['moved'] += 1
        return dest_path
    
    def archive_directory(self, directory, pattern='*', preserve_original=False):
        """Archive all files in a directory"""
        directory = Path(directory)
        
        if not directory.exists():
            print(f"Directory not found: {directory}")
            return
        
        files = list(directory.glob(pattern))
        print(f"Archiving {len(files)} files from {directory.name}...")
        
        for file_path in files:
            if file_path.is_file():
                try:
                    archived = self.archive_file(file_path, preserve_original)
                    if archived:
                        print(f"  ✓ {file_path.name[:50]}... -> {archived.name}")
                except Exception as e:
                    print(f"  ✗ Error archiving {file_path.name}: {e}")
                    self.stats['errors'] += 1
            else:
                self.stats['skipped'] += 1
    
    def cleanup_root(self):
        """Clean up root directory by archiving loose files"""
        print("\n=== Cleaning up root directory ===")
        
        # Archive emails/pending
        if (self.base_path / 'emails' / 'pending').exists():
            self.archive_directory(self.base_path / 'emails' / 'pending', '*.eml')
            self.archive_directory(self.base_path / 'emails' / 'pending', '*.msg')
        
        # Archive emails/originals
        if (self.base_path / 'emails' / 'originals').exists():
            self.archive_directory(self.base_path / 'emails' / 'originals', '*.*')
            # Remove the originals directory after archiving
            shutil.rmtree(self.base_path / 'emails' / 'originals')
        
        # Archive root level email files
        if (self.base_path / 'emails').exists():
            for pattern in ['*.pdf', '*.ods', '*.csv', '*.txt']:
                for file in (self.base_path / 'emails').glob(pattern):
                    if file.is_file():
                        self.archive_file(file)
        
        # Clean up empty directories
        self.remove_empty_dirs()
        
    def remove_empty_dirs(self):
        """Remove empty directories"""
        for root, dirs, files in os.walk(self.base_path / 'emails', topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  Removed empty directory: {dir_path}")
    
    def create_retrieval_script(self):
        """Create a script to retrieve original files when needed"""
        script_content = '''#!/usr/bin/env python3
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
        choice = int(input("\\nSelect file number to retrieve (0 to cancel): "))
        if choice == 0:
            return
    
    selected = found[choice - 1]
    source = Path(selected['archive_path'])
    dest = Path(output_dir) / selected['original_name']
    
    shutil.copy2(source, dest)
    print(f"\\n✓ Retrieved to: {dest}")

if __name__ == '__main__':
    search = input("Enter filename or pattern to search: ")
    retrieve_file(search)
'''
        
        script_path = self.base_path / 'retrieve_archived.py'
        with open(script_path, 'w') as f:
            f.write(script_content)
        script_path.chmod(0o755)
        print(f"\n✓ Created retrieval script: retrieve_archived.py")
    
    def print_summary(self):
        """Print archive summary"""
        print("\n=== Archive Summary ===")
        print(f"Files archived: {self.stats['moved']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"\nArchive location: {self.archive_root}")
        print(f"Mapping file: {self.mapping_file}")
        
        # Count by type
        type_counts = {}
        for info in self.mapping['files'].values():
            file_type = info['type']
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        print("\nFiles by type:")
        for file_type, count in type_counts.items():
            print(f"  {file_type}: {count} files")

import os

if __name__ == '__main__':
    manager = ArchiveManager(Path.cwd())
    
    # Archive and clean up
    manager.cleanup_root()
    
    # Save mapping
    manager.save_mapping()
    
    # Create retrieval script
    manager.create_retrieval_script()
    
    # Print summary
    manager.print_summary()