import os
import yaml
from typing import List, Dict
import glob
from atom_model import Atom

class AtomLoader:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.atoms: Dict[str, Atom] = {}
        self.broken_files: List[str] = []

    def load_atoms(self):
        # Recursive search for .yaml files
        search_pattern = os.path.join(self.base_path, "**", "*.yaml")
        files = glob.glob(search_pattern, recursive=True)
        
        print(f"DEBUG: Search pattern: {search_pattern}")
        print(f"DEBUG: Found {len(files)} YAML files.")

        for file_path in files:
            # Skip registry or non-atom files if needed
            if "id_registry.yaml" in file_path:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                    
                if not content or 'identity' not in content:
                    print(f"Skipping {file_path}: No identity field")
                    continue
                    
                # Validate with Pydantic
                atom = Atom(**content)
                self.atoms[atom.identity.id] = atom
                
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
                self.broken_files.append(f"{file_path} ({str(e)})")
        
        return self.atoms
