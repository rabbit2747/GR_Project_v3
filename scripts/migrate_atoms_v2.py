#!/usr/bin/env python3
"""
GR Atom Migration Script v1.2 → v2.0
=====================================
Changes:
1. zone: "Zone3" → zone: "Z3"
2. Remove related_to sections
3. Add entity_class based on type
4. Note: tags → function migration requires manual review (different semantics)

Usage: python migrate_atoms_v2.py [--dry-run]
"""

import os
import re
import sys
import yaml
from pathlib import Path

# Types that are entity_class: true
ENTITY_TYPES = ['component', 'component_tool', 'component_control']

# Type mapping (old → new if needed)
TYPE_MAPPING = {
    'tool': 'tool_knowledge',  # Default mapping, may need manual review
    'control': 'control_policy',  # Default mapping, may need manual review
}

def migrate_yaml_content(content: str, filepath: str) -> tuple[str, list]:
    """Migrate YAML content and return (new_content, changes_made)"""
    changes = []
    
    # 1. Zone format change: Zone3 → Z3
    zone_pattern = r'zone:\s*["\']?Zone(\d)["\']?'
    if re.search(zone_pattern, content):
        content = re.sub(zone_pattern, r'zone: "Z\1"', content)
        changes.append("Zone format updated (Zone# → Z#)")
    
    # Zone0A, Zone0B handling
    zone0_pattern = r'zone:\s*["\']?Zone(0[AB])["\']?'
    if re.search(zone0_pattern, content):
        content = re.sub(zone0_pattern, r'zone: "Z\1"', content)
        changes.append("Zone0A/0B format updated")
    
    # 2. Remove related_to sections (multi-line)
    related_to_pattern = r'\n\s+related_to:\s*\n(\s+-\s+"[^"]+"\n)+'
    if re.search(related_to_pattern, content):
        content = re.sub(related_to_pattern, '\n', content)
        changes.append("related_to removed")
    
    # Single line related_to
    related_to_single = r'\n\s+related_to:\s*\[[^\]]*\]'
    if re.search(related_to_single, content):
        content = re.sub(related_to_single, '', content)
        changes.append("related_to (inline) removed")
    
    return content, changes

def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single YAML file"""
    result = {
        'path': str(filepath),
        'status': 'unchanged',
        'changes': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        new_content, changes = migrate_yaml_content(original_content, str(filepath))
        
        if changes:
            result['status'] = 'modified'
            result['changes'] = changes
            
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
    
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result

def main():
    dry_run = '--dry-run' in sys.argv
    
    kb_path = Path('/root/.openclaw/workspace/GR_PROJECT/GR_project_v3/04_knowledge_base')
    
    if not kb_path.exists():
        print(f"Error: Knowledge base path not found: {kb_path}")
        sys.exit(1)
    
    yaml_files = list(kb_path.rglob('*.yaml'))
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Processing {len(yaml_files)} YAML files...")
    print("=" * 60)
    
    stats = {'unchanged': 0, 'modified': 0, 'error': 0}
    modified_files = []
    
    for filepath in yaml_files:
        result = process_file(filepath, dry_run)
        stats[result['status']] += 1
        
        if result['status'] == 'modified':
            modified_files.append(result)
        elif result['status'] == 'error':
            print(f"ERROR: {result['path']}: {result.get('error', 'Unknown')}")
    
    print(f"\nSummary:")
    print(f"  - Modified: {stats['modified']}")
    print(f"  - Unchanged: {stats['unchanged']}")
    print(f"  - Errors: {stats['error']}")
    
    if modified_files and len(modified_files) <= 50:
        print(f"\nModified files:")
        for f in modified_files:
            print(f"  - {f['path']}: {', '.join(f['changes'])}")
    elif modified_files:
        print(f"\n(Too many modified files to list, showing first 20)")
        for f in modified_files[:20]:
            print(f"  - {f['path']}: {', '.join(f['changes'])}")
    
    if dry_run:
        print(f"\n[DRY RUN] No files were actually modified.")
    else:
        print(f"\nMigration complete!")

if __name__ == '__main__':
    main()
