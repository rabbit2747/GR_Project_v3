from typing import List, Dict, Any
import networkx as nx
from graph_builder import GraphEngine

class QueryEngine:
    def __init__(self, graph_engine: GraphEngine):
        self.ge = graph_engine
        self.graph = graph_engine.graph
        self.atoms = graph_engine.atoms

    def get_atom_details(self, atom_id: str) -> Dict[str, Any]:
        """Returns details if atom exists, or marks as 'Missing Knowledge'"""
        if atom_id in self.atoms:
            atom = self.atoms[atom_id]
            coords = atom.classification.gr_coordinates if atom.classification and atom.classification.gr_coordinates else {}
            return {
                "status": "EXISTING",
                "name": atom.identity.name,
                "type": atom.classification.type if atom.classification else "Unknown",
                "layer": coords.get('layer', 'N/A')
            }
        else:
            return {
                "status": "MISSING (Frontier)",
                "name": "Unknown Concept",
                "type": "N/A",
                "layer": "N/A"
            }

    def analyze_context(self, atom_id: str) -> List[str]:
        """Analyzes immediate surroundings (Context)"""
        if atom_id not in self.graph:
            return [f"Atom '{atom_id}' not found in Knowledge Graph."]
        
        results = []
        
        # 1. Forward Context (What it affects/needs)
        for target in self.graph.successors(atom_id):
            edge_data = self.graph.get_edge_data(atom_id, target)
            rel_type = edge_data.get('type', 'related_to')
            target_info = self.get_atom_details(target)
            
            results.append(f"  [This] --({rel_type})--> {target} : {target_info['name']} ({target_info['status']})")

        # 2. Backward Context (What affects/needs it)
        for source in self.graph.predecessors(atom_id):
            edge_data = self.graph.get_edge_data(source, atom_id)
            rel_type = edge_data.get('type', 'related_to')
            source_info = self.get_atom_details(source)
            
            results.append(f"  {source} : {source_info['name']} ({source_info['status']}) --({rel_type})--> [This]")

        if not results:
            results.append("  (No connections found)")
            
        return results

    def find_attack_path(self, start_atom_id: str) -> List[str]:
        """Traces offensive relationships (causes, enables, etc.)"""
        offensive_rels = ['causes', 'enables', 'precipitates', 'is_a']
        return self._trace_path(start_atom_id, offensive_rels, "Attack Path")

    def _trace_path(self, start_id: str, rel_types: List[str], label: str) -> List[str]:
        if start_id not in self.graph:
            return []
            
        paths = []
        # Simple 1-hop trace for MVP
        for target in self.graph.successors(start_id):
            edge_data = self.graph.get_edge_data(start_id, target)
            rtype = edge_data.get('type', '')
            
            if rtype in rel_types:
                t_info = self.get_atom_details(target)
                paths.append(f"  [{label}] --({rtype})--> {target} ({t_info['status']})")
                
        return paths
