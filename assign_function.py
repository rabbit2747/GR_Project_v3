#!/usr/bin/env python3
"""
GR Project v3 — Function 코드 배정 + 1글자 atom_tags 제거 스크립트
132개 인프라 파일에 function 필드 추가, 45개 파일에서 1글자 코드 제거

DRY RUN mode by default. Pass --apply to actually write changes.
"""

import yaml
import glob
import os
import sys
import re
import copy

DRY_RUN = "--apply" not in sys.argv

# ═══════════════════════════════════════════════════════════════
# 전체 매핑 테이블: atom_id → function code
# ═══════════════════════════════════════════════════════════════
FUNCTION_MAP = {
    # === COMP (Compliance Frameworks) → C domain ===
    "COMP-FRAMEWORK-GDPR-001":      "C1.1",
    "COMP-FRAMEWORK-HIPAA-001":     "C1.3",
    "COMP-FRAMEWORK-ISO27001-001":  "C2.2",
    "COMP-FRAMEWORK-NIST-001":      "C2.4",
    "COMP-FRAMEWORK-PCIDSS-001":    "C1.2",
    "COMP-FRAMEWORK-SOC2-001":      "C2.1",
    "COMP-GDPR-001":                "C1.1",
    "COMP-HIPAA-001":               "C1.3",
    "COMP-ISO27001-001":            "C2.2",
    "COMP-NIST-CSF-001":            "C2.4",
    "COMP-PCIDSS-001":              "C1.2",
    "COMP-SOC2-001":                "C2.1",

    # === DEF-AUTH → S2/S6 ===
    "DEF-AUTH-MFA-001":   "S2.1",
    "DEF-AUTH-PAM-001":   "S6.3",
    "DEF-AUTH-SSO-001":   "S2.1",

    # === DEF (General Defense) ===
    "DEF-AWARENESS-001":         "S12.5",   # Security Awareness → Advanced Security (Zero Trust mindset)
    "DEF-BACKUP-001":            "D5.1",
    "DEF-CASB-001":              "S10.1",
    "DEF-CLOUD-CIEM-001":        "S10.4",
    "DEF-CLOUD-CWPP-001":        "S10.3",
    "DEF-CLOUD-POSTURE-001":     "S10.2",
    "DEF-CONTAINER-RUNTIME-001": "R1.1",
    "DEF-CRYPTO-PKI-001":        "S3.1",
    "DEF-CRYPTO-TLS-001":        "S3.1",
    "DEF-DECEPTION-001":         "S12.4",
    "DEF-DLP-001":               "S12.1",
    "DEF-EMAIL-SECURITY-001":    "S12.2",
    "DEF-ENDPOINT-EDR-001":      "S9.1",
    "DEF-IAM-001":               "S6.1",
    "DEF-LOGGING-001":           "M3.1",
    "DEF-NDR-001":               "S9.3",
    "DEF-NET-FIREWALL-001":      "N8.1",
    "DEF-NET-IDS-001":           "M6.2",
    "DEF-NET-SEGMENTATION-001":  "N8.3",
    "DEF-PATCH-MANAGEMENT-001":  "S4.3",
    "DEF-SIEM-001":              "S5.1",
    "DEF-SOAR-001":              "S12.6",
    "DEF-THREAT-INTEL-001":      "S5.2",
    "DEF-UEBA-001":              "S12.3",
    "DEF-WAF-001":               "S1.1",
    "DEF-XDR-001":               "S9.2",

    # === DEF-DETECT ===
    "DEF-DETECT-ANOMALY-001":      "M4.2",
    "DEF-DETECT-IDS-001":          "M6.2",
    "DEF-DETECT-LOGGING-001":      "S8.1",
    "DEF-DETECT-MONITORING-001":   "M6.1",
    "DEF-DETECT-SOAR-001":         "S12.6",
    "DEF-DETECT-THREAT-INTEL-001": "S5.2",
    "DEF-DETECT-WAF-001":          "S1.1",
    "DEF-DETECT-XDR-001":          "S9.2",

    # === DEF-DEVSECOPS ===
    "DEF-DEVSECOPS-DAST-001": "S7.2",
    "DEF-DEVSECOPS-SAST-001": "S7.1",
    "DEF-DEVSECOPS-SCA-001":  "S7.3",

    # === DEF-FORENSIC ===
    "DEF-FORENSIC-DISK-001":    "S13.1",
    "DEF-FORENSIC-MEMORY-001":  "S13.2",
    "DEF-FORENSIC-NETWORK-001": "S13.3",

    # === DEF-K8S ===
    "DEF-K8S-NETWORK-POLICY-001": "N8.3",

    # === DEF-MONITOR ===
    "DEF-MONITOR-LOGGING-001": "M3.1",

    # === DEF-NET (security/defense/) ===
    "DEF-NET-RPKI-001": "N9.1",

    # === DEF-PREVENT ===
    "DEF-PREVENT-API-AUTH-001":     "N7.3",
    "DEF-PREVENT-API-GATEWAY-001":  "N7.1",
    "DEF-PREVENT-CASB-001":         "S10.1",
    "DEF-PREVENT-CERT-PINNING-001": "S3.1",
    "DEF-PREVENT-CORS-001":         "S11.2",
    "DEF-PREVENT-CSP-001":          "S11.2",
    "DEF-PREVENT-CSRF-TOKEN-001":   "S11.3",
    "DEF-PREVENT-DLP-001":          "S12.1",
    "DEF-PREVENT-ENCRYPT-001":      "S3.2",
    "DEF-PREVENT-HEADERS-001":      "S11.2",
    "DEF-PREVENT-HSTS-001":         "S11.2",
    "DEF-PREVENT-HTTPS-001":        "S3.1",
    "DEF-PREVENT-INPUTVAL-001":     "S11.1",
    "DEF-PREVENT-MFA-001":          "S2.1",
    "DEF-PREVENT-OUTPUTENC-001":    "S11.1",
    "DEF-PREVENT-PARAMQUERY-001":   "S11.4",
    "DEF-PREVENT-RATELIMIT-001":    "N7.2",
    "DEF-PREVENT-SANDBOX-001":      "S12.7",
    "DEF-PREVENT-SECRETS-001":      "P5.1",
    "DEF-PREVENT-SEGMENTATION-001": "N8.3",
    "DEF-PREVENT-WAF-RULES-001":    "S1.1",
    "DEF-PREVENT-ZERO-TRUST-001":   "S12.5",

    # === DEF-RESPOND ===
    "DEF-RESPOND-BLOCK-001":      "S5.3",
    "DEF-RESPOND-FORENSICS-001":  "S13.1",
    "DEF-RESPOND-INCIDENT-001":   "S5.3",
    "DEF-RESPOND-QUARANTINE-001": "S5.3",

    # === DEF-WIN (Windows) ===
    "DEF-WIN-ASR-001":              "S14.1",
    "DEF-WIN-CREDENTIAL-GUARD-001": "S14.1",
    "DEF-WIN-LAPS-001":             "S14.1",

    # === INFRA-APP ===
    "INFRA-APP-API-001":         "A3.1",
    "INFRA-APP-MOBILE-API-001":  "A3.1",
    "INFRA-APP-SPA-001":         "A1.1",
    "INFRA-APP-WAS-001":         "A6.1",
    "INFRA-APP-WAS-JBOSS-001":   "A6.1",
    "INFRA-APP-WAS-TOMCAT-001":  "A6.1",
    "INFRA-APP-WAS-WEBLOGIC-001":"A6.1",
    "INFRA-APP-WAS-WEBSPHERE-001":"A6.1",
    "INFRA-APP-WEBAPP-001":      "A1.1",
    "INFRA-APP-WEBSERVER-001":   "A6.2",

    # === INFRA-CLOUD ===
    "INFRA-CLOUD-001":          "P1.1",
    "INFRA-CLOUD-AWS-IAM-001":  "S6.1",
    "INFRA-CLOUD-AWS-S3-001":   "R3.2",
    "INFRA-CLOUD-AZURE-001":    "P1.1",
    "INFRA-CLOUD-AZURE-AD-001": "S6.1",
    "INFRA-CLOUD-GCP-001":      "P1.1",
    "INFRA-CLOUD-GCP-IAM-001":  "S6.1",
    "INFRA-CLOUD-IAM-001":      "S6.1",

    # === INFRA-COMPUTE ===
    "INFRA-COMPUTE-CONTAINER-001": "R1.1",
    "INFRA-COMPUTE-SERVER-001":    "R2.1",
    "INFRA-COMPUTE-VM-001":        "R2.1",

    # === INFRA-CONTAINER ===
    "INFRA-CONTAINER-DOCKER-001": "P3.1",
    "INFRA-CONTAINER-K8S-001":    "P3.2",

    # === INFRA-DATA ===
    "INFRA-DATA-CACHE-001":    "D3.1",
    "INFRA-DATA-MQ-001":       "D4.2",
    "INFRA-DATA-RDBMS-001":    "D1.1",
    "INFRA-DATA-STORAGE-001":  "R3.1",

    # === INFRA-DNS ===
    "INFRA-DNS-001": "N3.2",

    # === INFRA-IAM ===
    "INFRA-IAM-LDAP-001": "S6.1",

    # === INFRA-NET ===
    "INFRA-NET-CDN-001":      "N4.1",
    "INFRA-NET-DNS-001":      "N3.2",
    "INFRA-NET-FIREWALL-001": "N8.1",
    "INFRA-NET-LB-001":       "N1.2",
    "INFRA-NET-NETWORK-001":  "N2.1",
    "INFRA-NET-WAF-001":      "S1.1",

    # === INFRA-NETWORK ===
    "INFRA-NETWORK-VPN-001": "N5.2",

    # === INFRA-RUNTIME ===
    "INFRA-RUNTIME-CONTAINER-001": "R1.1",
    "INFRA-RUNTIME-JVM-001":       "R6.1",
    "INFRA-RUNTIME-K8S-001":       "R2.2",

    # === INFRA-SERVERLESS ===
    "INFRA-SERVERLESS-001": "P1.3",

    # === INFRA-SERVICE-MESH ===
    "INFRA-SERVICE-MESH-001": "N6.1",

    # === INFRA-SYS ===
    "INFRA-SYS-SERVER-001": "R2.1",
}

# Function domain 1-letter codes (to remove from atom_tags)
FUNCTION_DOMAIN_LETTERS = {'A', 'C', 'D', 'I', 'M', 'N', 'P', 'R', 'S', 'T', 'E'}

def load_yaml_raw(filepath):
    """Load YAML preserving comments by reading raw text"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_atom_id(content):
    """Extract atom ID from YAML content"""
    match = re.search(r'id:\s*"?([A-Z][A-Z0-9\-]+)"?', content)
    return match.group(1) if match else None

def get_is_infrastructure(content):
    """Check if is_infrastructure: true"""
    return 'is_infrastructure: true' in content

def remove_single_letter_tags(content):
    """Remove single-letter codes from atom_tags"""
    # Find atom_tags line(s)
    lines = content.split('\n')
    new_lines = []
    changed = False
    
    for i, line in enumerate(lines):
        # Match atom_tags: [...] format
        match = re.match(r'^(\s*atom_tags:\s*)\[(.+)\](.*)$', line)
        if match:
            prefix, tags_str, suffix = match.groups()
            # Parse tags
            tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',')]
            original_len = len(tags)
            # Remove single-letter function domain codes
            tags = [t for t in tags if not (len(t) == 1 and t in FUNCTION_DOMAIN_LETTERS)]
            if len(tags) < original_len:
                changed = True
                if tags:
                    tags_formatted = ', '.join(f'"{t}"' for t in tags)
                    new_lines.append(f'{prefix}[{tags_formatted}]{suffix}')
                else:
                    new_lines.append(f'{prefix}[]{suffix}')
                continue
        
        # Also handle multi-line atom_tags format
        # atom_tags:
        #   - "TAG"
        if re.match(r'^\s*-\s*"?[A-Z]"?\s*$', line):
            # Check if previous context is atom_tags
            # Find if we're inside atom_tags block
            tag_val = line.strip().lstrip('- ').strip('"').strip("'")
            if len(tag_val) == 1 and tag_val in FUNCTION_DOMAIN_LETTERS:
                # Check context - is this inside atom_tags?
                for j in range(i-1, max(i-5, -1), -1):
                    if 'atom_tags:' in lines[j] or (re.match(r'^\s*-\s*"?[A-Z]', lines[j]) and j > 0):
                        changed = True
                        continue  # skip this line
                    elif lines[j].strip() and not lines[j].strip().startswith('-'):
                        break
        
        new_lines.append(line)
    
    return '\n'.join(new_lines), changed

def add_or_update_function_field(content, function_code):
    """Add or update function field in gr_coordinates section"""
    lines = content.split('\n')
    new_lines = []
    updated = False
    added = False
    in_gr_coordinates = False
    
    for i, line in enumerate(lines):
        # Check if this is an existing function line to replace
        if re.match(r'^\s+function:\s*', line) and not updated:
            # Extract current value
            current = re.search(r'function:\s*"?([^"\n]+)"?', line)
            current_val = current.group(1).strip() if current else ''
            if current_val != function_code:
                indent = re.match(r'^(\s+)', line).group(1)
                new_lines.append(f'{indent}function: "{function_code}"')
                updated = True
                added = True  # mark as handled
                continue
            else:
                new_lines.append(line)
                added = True  # already correct
                continue
        
        new_lines.append(line)
        
        if 'gr_coordinates:' in line:
            in_gr_coordinates = True
            continue
        
        if in_gr_coordinates and not added:
            # Look for the zone line (last coordinate in gr_coordinates)
            if re.match(r'^\s+zone:', line):
                # Check if next line is already function
                next_line = lines[i+1] if i+1 < len(lines) else ''
                if not re.match(r'^\s+function:', next_line):
                    indent = re.match(r'^(\s+)', line).group(1)
                    new_lines.append(f'{indent}function: "{function_code}"')
                    added = True
                in_gr_coordinates = False
            elif re.match(r'^\s+layer:', line) and i+1 < len(lines):
                next_line = lines[i+1] if i+1 < len(lines) else ''
                if not re.match(r'^\s+zone:', next_line) and not re.match(r'^\s+function:', next_line):
                    indent = re.match(r'^(\s+)', line).group(1)
                    new_lines.append(f'{indent}function: "{function_code}"')
                    added = True
                    in_gr_coordinates = False
    
    # If we didn't find gr_coordinates but file is infrastructure
    if not added and 'gr_coordinates:' not in content:
        lines2 = []
        for line in new_lines:
            lines2.append(line)
            if 'is_infrastructure: true' in line:
                indent = re.match(r'^(\s*)', line).group(1)
                lines2.append(f'{indent}gr_coordinates:')
                lines2.append(f'{indent}  function: "{function_code}"')
                added = True
        new_lines = lines2
    
    return '\n'.join(new_lines), added or updated

def process_file(filepath):
    """Process a single YAML file"""
    content = load_yaml_raw(filepath)
    atom_id = get_atom_id(content)
    if not atom_id:
        return None, None, None
    
    is_infra = get_is_infrastructure(content)
    original = content
    changes = []
    
    # 1. Remove single-letter codes from atom_tags (all files that have them)
    content, tag_changed = remove_single_letter_tags(content)
    if tag_changed:
        changes.append("removed 1-letter codes from atom_tags")
    
    # 2. Add/update function field (infrastructure files only)
    if is_infra and atom_id in FUNCTION_MAP:
        func_code = FUNCTION_MAP[atom_id]
        content, func_added = add_or_update_function_field(content, func_code)
        if func_added:
            changes.append(f"function: {func_code}")
    
    # 3. Remove function field from non-infrastructure files
    if not is_infra and re.search(r'^\s+function:', content, re.MULTILINE):
        lines = content.split('\n')
        content = '\n'.join(line for line in lines if not re.match(r'^\s+function:', line))
        changes.append("removed function (non-infra)")
    
    if content != original:
        return atom_id, content, changes
    return atom_id, None, None

def main():
    base_dir = "04_knowledge_base"
    if not os.path.exists(base_dir):
        print("Error: Run from GR_project_v3 root directory")
        sys.exit(1)
    
    mode = "DRY RUN" if DRY_RUN else "APPLYING"
    print(f"=== Function 코드 배정 스크립트 ({mode}) ===\n")
    
    # Find all YAML files
    yaml_files = sorted(glob.glob(f"{base_dir}/**/*.yaml", recursive=True))
    
    stats = {
        'total': 0,
        'function_added': 0,
        'tags_cleaned': 0,
        'skipped': 0,
        'errors': 0,
        'no_mapping': [],
    }
    
    processed_ids = set()
    
    for fp in yaml_files:
        try:
            atom_id, new_content, changes = process_file(fp)
            if not atom_id:
                continue
            
            stats['total'] += 1
            
            # Track infrastructure files without mapping
            content = load_yaml_raw(fp)
            if get_is_infrastructure(content) and atom_id not in FUNCTION_MAP:
                if atom_id not in processed_ids:
                    stats['no_mapping'].append(atom_id)
            
            processed_ids.add(atom_id)
            
            if new_content and changes:
                for c in changes:
                    if 'function' in c:
                        stats['function_added'] += 1
                    if 'tags' in c:
                        stats['tags_cleaned'] += 1
                
                print(f"  {'[DRY]' if DRY_RUN else '[OK]'} {os.path.basename(fp)}: {', '.join(changes)}")
                
                if not DRY_RUN:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            else:
                stats['skipped'] += 1
                
        except Exception as e:
            stats['errors'] += 1
            print(f"  [ERROR] {fp}: {e}")
    
    print(f"\n=== 결과 ===")
    print(f"전체 파일: {stats['total']}")
    print(f"function 추가: {stats['function_added']}")
    print(f"atom_tags 정리: {stats['tags_cleaned']}")
    print(f"변경 없음: {stats['skipped']}")
    print(f"오류: {stats['errors']}")
    
    if stats['no_mapping']:
        print(f"\n⚠️  매핑 없는 인프라 파일 ({len(stats['no_mapping'])}개):")
        for aid in sorted(stats['no_mapping']):
            print(f"  - {aid}")
    
    if DRY_RUN:
        print(f"\n💡 실제 적용하려면: python3 assign_function.py --apply")

if __name__ == "__main__":
    main()
