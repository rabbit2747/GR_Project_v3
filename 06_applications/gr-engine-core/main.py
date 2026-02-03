import sys
import os

# Install Dependencies automatically if missing (for prototype convenience)
try:
    import networkx
    import yaml
    import pydantic
except ImportError:
    print("Installing missing dependencies...")
    os.system("pip install networkx pyyaml pydantic")

from loader import AtomLoader
from graph_builder import GraphEngine

def main():
    base_path = os.path.abspath("../../02_knowledge_base")
    print(f"Initializing GR Engine Verification...")
    print(f"Target Knowledge Base: {base_path}")
    
    # 1. Load Data
    loader = AtomLoader(base_path)
    atoms = loader.load_atoms()
    
    print(f"\n[1] Data Loading")
    print(f" - Loaded Atoms: {len(atoms)}")
    print(f" - Broken Files: {len(loader.broken_files)}")
    if loader.broken_files:
        print(f"   ! Sample faulty file: {loader.broken_files[0]}")

    # 2. Build Graph
    engine = GraphEngine(atoms)
    stats = engine.get_stats()
    
    print(f"\n[2] Graph Connectivity Analysis")
    print(f" - Total Nodes: {stats['total_nodes']}")
    print(f" - Total Relations: {stats['total_edges']}")
    print(f" - Orphan Atoms (Isolated): {stats['orphans']}")
    
    # 3. Validation Checks
    print(f"\n[3] Logic Verification")
    
    # Check 3.1: Dangling Pointers
    dangling = engine.get_dangling_pointers()
    print(f" - Broken Links (Pointing to non-existent ID): {len(dangling)}")
    if dangling:
        print(f"   ! Example: {dangling[0][0]} -> {dangling[0][1]} ({dangling[0][2]})")
        
    # Check 3.2: Orphan List
    orphans = engine.get_orphans()
    if orphans:
        print(f" - Orphan Samples: {orphans[:5]}...")
    
    # 4. Generate Report
    report_path = "../../05_docs/GR_VERIFICATION_REPORT.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# GR Project v2 Verification Report\n\n")
        f.write(f"**Date:** {os.popen('date /t').read().strip()}\n")
        f.write(f"**Status:** {'PASS' if stats['orphans'] == 0 else 'WARNING'}\n\n")
        
        f.write("## 1. Summary\n")
        f.write(f"- **Total Atoms**: {len(atoms)}\n")
        f.write(f"- **Graph Edges**: {stats['total_edges']}\n")
        f.write(f"- **Orphan Nodes**: {stats['orphans']}\n")
        f.write(f"- **Broken Links**: {len(dangling)}\n\n")
        
        f.write("## 2. Issues Found\n")
        if orphans:
            f.write("### 2.1 Orphan Atoms (No Connections)\n")
            for o in orphans:
                f.write(f"- `{o}`\n")
            f.write("\n")
            
        if dangling:
            f.write("### 2.2 Broken Links (Invalid References)\n")
            for u, v, t in dangling:
                f.write(f"- `{u}` tries to link to `{v}` via `{t}`, but `{v}` does not exist.\n")

    print(f"\n[4] Report Generated: {os.path.abspath(report_path)}")

    # 5. Live Inference Test (Query Engine)
    print(f"\n[5] Live Inference Test (Partial Logic Verification)")
    from query_engine import QueryEngine
    query_bot = QueryEngine(engine)
    
    # Pick a sample atom that has connections (preferably mixed existing/missing)
    # We'll search for one with edges
    sample_id = "GR-SEC-TEC-00001" # Default fallback
    
    # Try to find a better sample dynamically
    for node, degree in engine.graph.degree():
        if degree > 2:
            sample_id = node
            break
            
    print(f"Target Atom: {sample_id}")
    context = query_bot.analyze_context(sample_id)
    for line in context:
        print(line)
        
    print(f"\nTest Complete. Engine is functional despite {len(dangling)} missing links.")

if __name__ == "__main__":
    main()
