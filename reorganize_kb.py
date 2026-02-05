#!/usr/bin/env python3
"""
GR Project v3 — Knowledge Base 디렉토리 재구조화
목표: atom ID 접두어 기반으로 1:1 매핑되는 깔끔한 구조

DRY RUN by default. Pass --apply to execute moves.
"""

import os
import re
import glob
import shutil
import sys

DRY_RUN = "--apply" not in sys.argv
KB = "04_knowledge_base"

# ═══════════════════════════════════════════════════════════════
# 접두어 → 최상위 디렉토리 매핑
# ═══════════════════════════════════════════════════════════════
PREFIX_MAP = {
    "ATK":  "attacks",
    "COMP": "compliance",
    "DEF":  "defenses",
    "GR":   "concepts",
    "INFRA":"infrastructure",
    "TECH": "technology",
    "TOOL": "tools",
    "VUL":  "vulnerabilities",
}

# ═══════════════════════════════════════════════════════════════
# 세부 디렉토리 매핑 (ID 패턴 기반)
# ═══════════════════════════════════════════════════════════════
def get_subdir(atom_id, current_path):
    """Determine sub-directory within the target top-level dir"""
    
    # ATK: keep the nice sub-structure from security/attacks/
    if atom_id.startswith("ATK-MITRE"):
        return "mitre"
    elif atom_id.startswith("ATK-WIN"):
        return "windows"
    elif atom_id.startswith("ATK-LINUX"):
        return "linux"
    elif atom_id.startswith("ATK-NET"):
        return "network"
    elif atom_id.startswith("ATK-WEB") or atom_id.startswith("ATK-INJECT") or atom_id.startswith("ATK-XSS"):
        return "web"
    elif atom_id.startswith("ATK-API"):
        return "api"
    elif atom_id.startswith("ATK-AUTH"):
        return "authentication"
    elif atom_id.startswith("ATK-CLIENT"):
        return "client-side"
    elif atom_id.startswith("ATK-CLOUD"):
        return "cloud"
    elif atom_id.startswith("ATK-CONTAINER") or atom_id.startswith("ATK-K8S"):
        return "container"
    elif atom_id.startswith("ATK-CRYPTO"):
        return "crypto"
    elif atom_id.startswith("ATK-IOT"):
        return "iot"
    elif atom_id.startswith("ATK-MALWARE"):
        return "malware"
    elif atom_id.startswith("ATK-MOBILE"):
        return "mobile"
    elif atom_id.startswith("ATK-PHYS"):
        return "physical"
    elif atom_id.startswith("ATK-RECON"):
        return "reconnaissance"
    elif atom_id.startswith("ATK-SERVER"):
        return "server-side"
    elif atom_id.startswith("ATK-SOCIAL"):
        return "social"
    elif atom_id.startswith("ATK-SUPPLY"):
        return "supply-chain"
    elif atom_id.startswith("ATK-NETWORK"):
        return "network"
    elif atom_id.startswith("ATK-"):
        # Check current location for hint
        if "security/attacks/" in current_path:
            # Extract sub-dir from current path
            parts = current_path.split("security/attacks/")
            if len(parts) > 1:
                subparts = parts[1].split("/")
                if len(subparts) > 1:
                    return subparts[0]
        # For concepts/attacks files, try to infer
        if "injection" in atom_id.lower() or "sqli" in atom_id.lower():
            return "web"
        return ""  # root of attacks/
    
    # TECH: keep sub-dirs
    if atom_id.startswith("TECH-LANG"):
        return "languages"
    elif atom_id.startswith("TECH-PROTOCOL"):
        return "protocols"
    elif atom_id.startswith("TECH-FORMAT"):
        return "formats"
    elif atom_id.startswith("TECH-CONCEPT"):
        return "concepts"
    elif atom_id.startswith("TECH-"):
        if "technology/" in current_path:
            parts = current_path.split("technology/")
            if len(parts) > 1:
                subparts = parts[1].split("/")
                if len(subparts) > 1:
                    return subparts[0]
        return "concepts"  # default for TECH
    
    # VUL: categorize by type
    if atom_id.startswith("VUL-WEB"):
        return "web"
    elif atom_id.startswith("VUL-AUTH"):
        return "auth"
    elif atom_id.startswith("VUL-CONFIG"):
        return "config"
    elif atom_id.startswith("VUL-CRYPTO"):
        return "crypto"
    elif atom_id.startswith("VUL-MOBILE"):
        return "mobile"
    elif atom_id.startswith("VUL-"):
        if "security/vulnerabilities/" in current_path:
            return ""
        return ""
    
    # TOOL: keep simple structure
    if atom_id.startswith("TOOL-OFFENSE") or atom_id.startswith("TOOL-PENTEST"):
        return "offensive"
    elif atom_id.startswith("TOOL-DEFENSE"):
        return "defensive"
    elif atom_id.startswith("TOOL-AUDIT") or atom_id.startswith("TOOL-SCAN"):
        return "audit"
    elif atom_id.startswith("TOOL-RECON") or atom_id.startswith("TOOL-OSINT"):
        return "recon"
    elif atom_id.startswith("TOOL-AD"):
        return "active-directory"
    elif atom_id.startswith("TOOL-API"):
        return "api"
    elif atom_id.startswith("TOOL-SCANNER"):
        return "audit"
    elif atom_id.startswith("TOOL-"):
        return ""
    
    # Others: flat structure
    return ""


def main():
    if not os.path.exists(KB):
        print("Error: Run from GR_project_v3 root directory")
        sys.exit(1)
    
    mode = "DRY RUN" if DRY_RUN else "APPLYING"
    print(f"=== KB 디렉토리 재구조화 ({mode}) ===\n")
    
    # Phase 1: Collect all YAML files and plan moves
    moves = []
    conflicts = []
    skips = []
    
    for fp in sorted(glob.glob(f"{KB}/**/*.yaml", recursive=True)):
        basename = os.path.basename(fp)
        if basename.startswith("_") or basename in ("expansion_plan_v1.yaml", "id_registry.yaml"):
            skips.append(fp)
            continue
        
        with open(fp) as f:
            content = f.read()
        
        match = re.search(r'id:\s*"?([A-Z][A-Z0-9\-]+)', content)
        if not match:
            skips.append(fp)
            continue
        
        atom_id = match.group(1)
        prefix = atom_id.split("-")[0]
        
        if prefix not in PREFIX_MAP:
            skips.append(fp)
            continue
        
        target_top = PREFIX_MAP[prefix]
        subdir = get_subdir(atom_id, fp)
        
        if subdir:
            target_path = os.path.join(KB, target_top, subdir, basename)
        else:
            target_path = os.path.join(KB, target_top, basename)
        
        # Normalize path
        target_path = os.path.normpath(target_path)
        source_path = os.path.normpath(fp)
        
        if source_path == target_path:
            continue  # Already in correct location
        
        moves.append((source_path, target_path, atom_id))
    
    # Check for conflicts (multiple files targeting same location)
    targets = {}
    for src, tgt, aid in moves:
        if tgt in targets:
            conflicts.append((tgt, targets[tgt], (src, aid)))
        else:
            targets[tgt] = (src, aid)
    
    if conflicts:
        print(f"⚠️  충돌 {len(conflicts)}개 발견:")
        for tgt, (src1, aid1), (src2, aid2) in conflicts:
            print(f"  {tgt}:")
            print(f"    ← {src1} ({aid1})")
            print(f"    ← {src2} ({aid2})")
        print()
    
    # Phase 2: Report plan
    print(f"이동 계획: {len(moves)}개 파일")
    print(f"이미 올바른 위치: {561 - len(moves) - len(skips)}개")
    print(f"건너뛰기 (메타파일): {len(skips)}개")
    print()
    
    # Group by source top-level dir
    from collections import Counter
    source_dirs = Counter()
    for src, tgt, aid in moves:
        parts = src.replace(KB + "/", "").split("/")
        source_dirs[parts[0]] += 1
    
    print("이동 소스별:")
    for d, c in source_dirs.most_common():
        print(f"  {d}/: {c}개 이동")
    print()
    
    # Show sample moves
    print("샘플 이동:")
    shown = set()
    for src, tgt, aid in moves[:15]:
        src_short = src.replace(KB + "/", "")
        tgt_short = tgt.replace(KB + "/", "")
        print(f"  {src_short}")
        print(f"    → {tgt_short}")
    if len(moves) > 15:
        print(f"  ... (+{len(moves)-15}개)")
    print()
    
    # Phase 3: Execute moves
    if not DRY_RUN and not conflicts:
        moved = 0
        errors = 0
        for src, tgt, aid in moves:
            try:
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                shutil.move(src, tgt)
                moved += 1
            except Exception as e:
                print(f"  [ERROR] {src}: {e}")
                errors += 1
        
        # Also move non-YAML files from security/attacks/injection/sqli/
        sqli_src = os.path.join(KB, "security/attacks/injection/sqli")
        sqli_tgt = os.path.join(KB, "attacks/web/injection/sqli")
        if os.path.exists(sqli_src):
            for f in glob.glob(f"{sqli_src}/**/*", recursive=True):
                if os.path.isfile(f) and not f.endswith('.yaml'):
                    rel = os.path.relpath(f, sqli_src)
                    new_path = os.path.join(sqli_tgt, rel)
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    if not os.path.exists(new_path):
                        shutil.move(f, new_path)
                        moved += 1
        
        # Clean up empty directories
        for root, dirs, files in os.walk(KB, topdown=False):
            for d in dirs:
                dirpath = os.path.join(root, d)
                try:
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                except:
                    pass
        
        print(f"=== 결과 ===")
        print(f"이동 완료: {moved}개")
        print(f"오류: {errors}개")
        
        # Verify final structure
        print(f"\n=== 최종 구조 ===")
        for d in sorted(os.listdir(KB)):
            dpath = os.path.join(KB, d)
            if os.path.isdir(dpath):
                count = len(glob.glob(f"{dpath}/**/*.yaml", recursive=True))
                print(f"  {d}/: {count}개")
    
    if DRY_RUN:
        print(f"💡 실제 적용: python3 reorganize_kb.py --apply")


if __name__ == "__main__":
    main()
