import networkx as nx
from typing import Dict, List, Set, Tuple
from atom_model import Atom

class GraphEngine:
    def __init__(self, atoms: Dict[str, Atom]):
        self.atoms = atoms
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        # Add all nodes first
        for atom_id in self.atoms:
            self.graph.add_node(atom_id)
            
        # Add edges
        for atom in self.atoms.values():
            src_id = atom.identity.id
            
            # Flatten relations
            if not atom.relations:
                continue
                
            # Handle nested relation structure (structural, causal, etc.)
            for rel_category, rel_types in atom.relations.items():
                if isinstance(rel_types, dict):
                    for rel_type, targets in rel_types.items():
                        if not targets: continue
                        
                        # Normalize targets to a list
                        if isinstance(targets, str): 
                            target_list = [targets]
                        elif isinstance(targets, list):
                            target_list = targets
                        else:
                            continue

                        for target in target_list:
                            # Handle case where target might be a dict (e.g. conditional relation) or complex object
                            target_id = None
                            if isinstance(target, str):
                                target_id = target
                            elif isinstance(target, dict):
                                # Try to find ID in dict keys or values, often formatted as {id: metadata}
                                # For now, let's assume if it's a dict, we skip or extract a specific 'id' key if present
                                # This is a common YAML parsing issue where - id: x becomes a list of dicts
                                if 'id' in target:
                                    target_id = target['id']
                                else:
                                    # Fallback: simple key-value pairs?
                                    pass
                            
                            if target_id:
                                self.graph.add_edge(src_id, target_id, type=rel_type)

    def get_orphans(self) -> List[str]:
        # Nodes with 0 degree (no in or out edges)
        return [n for n, d in self.graph.degree() if d == 0]
    
    def get_dangling_pointers(self) -> List[Tuple[str, str, str]]:
        # Edges pointing to nodes that don't exist in loaded atoms
        dangling = []
        for u, v, data in self.graph.edges(data=True):
            if v not in self.atoms:
                dangling.append((u, v, data.get('type', 'unknown')))
        return dangling

    def find_path(self, start_id: str, end_id: str) -> List[str]:
        try:
            return nx.shortest_path(self.graph, start_id, end_id)
        except nx.NetworkXNoPath:
            return []
            
    def get_stats(self):
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "orphans": len(self.get_orphans()),
            "connected_components": nx.number_weakly_connected_components(self.graph)
        }
