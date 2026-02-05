# 누락 개념 로우 데이터 v4 (Pass 3)

> v3의 ~349개 신규 항목을 재분해
> 이미 발견된 ~840개와 기존 KB 560개에 없는 것만 추출
> 생성일: 2026-02-05

---

## Pass 3: v3 항목 재분해에서 나온 신규 개념

### [P3-01] 암호학 더 깊이 (P2-01 재분해)
- X.509v3 Extension (SAN, Key Usage, Extended Key Usage)
- Certificate Signing Request (CSR)
- Certificate Pinning vs Certificate Transparency 차이
- Let's Encrypt / ACME Protocol
- Wildcard Certificate (보안 위험)
- Multi-Domain Certificate (SAN Certificate)
- Code Signing Certificate 남용
- Timestamping (코드서명)
- FIPS 140-2 / 140-3 (암호 모듈 인증)
- Common Criteria (CC)
- Quantum Key Distribution (QKD)
- Hybrid Cryptography (Classic + PQC)
- Key Ceremony
- Secret Sharing (Shamir's)

### [P3-02] AD/Windows 더 깊이 (P2-02 재분해)
- AD Schema (classSchema, attributeSchema)
- LDAP Filter Syntax (보안 관점)
- SID Filtering
- Selective Authentication (Forest Trust)
- AD DNS Integration
- ADIDNS Zone (보안)
- msDS-AllowedToDelegateTo
- msDS-AllowedToActOnBehalfOfOtherIdentity (RBCD)
- userAccountControl Flags
- servicePrincipalName Attribute
- Managed Password (gMSA 내부)
- nTSecurityDescriptor
- AD Recycle Bin (보안 관점)
- LDAP Channel Binding Token
- NTLM Downgrade Attack
- NTLMv1 vs NTLMv2 차이
- Windows Token Manipulation 상세 (SeAssignPrimaryTokenPrivilege)
- Print Spooler Service (보안 — PrintNightmare, SpoolFool)
- PetitPotam (NTLM Relay via EFS)
- Coercion Attacks (개념 — DFSCoerce, ShadowCoerce)
- SCCM/MECM (보안 관점)

### [P3-03] 네트워크 더 깊이 (P2-03 재분해)
- TCP Window Size Attack
- TCP Reset Attack
- IP Fragmentation Attack
- TTL-Based Evasion (IDS)
- Protocol Mismatch Evasion
- GRE/IP-in-IP Tunneling (보안)
- DNS Exfiltration (상세 — 인코딩, chunk 크기)
- ICMP Tunneling
- SSH Tunneling / Port Forwarding (보안 관점)
- Reverse SSH Tunnel
- SOCKS Proxy (보안 관점)
- Chisel / Ligolo / SSH Tunnel Tools (개념)
- Pivoting 개념
- Network Scanning Techniques (SYN/ACK/FIN/XMAS)
- OS Fingerprinting (TTL, Window Size)
- Service Fingerprinting (Banner Grabbing)
- SSL/TLS Certificate Transparency Log Mining
- JA3/JA3S Fingerprinting
- HASSH Fingerprinting
- Network Beaconing Detection
- DNS Beaconing

### [P3-04] 웹 더 깊이 (P2-04 재분해)
- Shadow DOM (보안 관점)
- Mutation XSS (mXSS)
- DOM Clobbering
- Prototype Pollution → RCE Chain
- Server-Sent Events (SSE) 보안
- HTTP/2 Stream Multiplexing (보안)
- gRPC Security
- GraphQL Introspection Disabling
- GraphQL Batching Attack
- GraphQL Field Suggestion Leak
- REST API Versioning (보안 관점)
- API Rate Limiting Implementation (Token Bucket, Leaky Bucket)
- API Pagination Abuse
- Mass Assignment (상세 — 프레임워크별)
- BOLA vs BFLA 차이
- Broken Object Property Level Authorization (BOPLA)
- API Schema Validation
- OpenAPI/Swagger (보안 관점)
- Insecure API Endpoint Discovery
- CORS Preflight (OPTIONS)
- CORS Misconfiguration Patterns (null origin, regex bypass)
- Content-Security-Policy Bypass Techniques
- CSP Nonce vs Hash
- Trusted Types Bypass

### [P3-05] 클라우드 더 깊이 (P2-05 재분해)
- AWS IAM Policy Evaluation Logic (explicit deny, SCP boundary)
- AWS S3 Object Lock
- AWS Lambda Execution Role Abuse
- AWS SSM Parameter Store / Secrets Manager
- AWS ECS Task Role vs Execution Role
- AWS EKS IRSA (IAM Roles for Service Accounts)
- AWS CloudFront Signed URL/Cookie
- Azure RBAC vs Azure AD Role
- Azure Managed Identity (System vs User Assigned)
- Azure Resource Lock
- GCP IAM Conditions
- GCP Organization Policy Constraints
- Cloud Cost Abuse / Cryptomining
- Cloud Forensics (Snapshot, Log, Metadata)
- Multi-Cloud Security Challenges
- Cloud Egress Filtering
- Cloud Network Firewall (AWS Network Firewall, Azure Firewall)

### [P3-06] 컨테이너/리눅스 더 깊이 (P2-08 재분해)
- Kubernetes API Server (보안)
- Kubernetes etcd Encryption at Rest
- Kubernetes Audit Log
- Kubernetes RuntimeClass
- Kubernetes Network Policy (Ingress/Egress)
- Calico / Cilium (Network Policy Engines)
- Falco Rules (커스텀)
- OPA/Gatekeeper (Admission Control)
- Kyverno
- Container Runtime Interface (CRI)
- Image Pull Policy (Always/IfNotPresent — 보안)
- Kubernetes Dashboard Exposure
- RBAC Misconfiguration (K8s)
- Anonymous Authentication (K8s)
- kubelet API (보안)
- Pod-to-Pod Encryption (mTLS)
- eBPF Programs (Cilium, Tetragon — 보안)
- Linux Audit Rules (auditctl)
- Falcoctl / Tracee
- Immutable Infrastructure

### [P3-07] AI/ML 더 깊이 (P2-09 재분해)
- RAG (Retrieval Augmented Generation) Poisoning
- Tool Use Attack (LLM)
- Agent Hijacking
- System Prompt Leakage
- Model Serialization Attack (Pickle, SafeTensors)
- Federated Learning Attack
- Differential Privacy (ML 관점)
- Model Watermarking
- AI Alignment (보안 관점)
- Responsible AI / AI Ethics (보안 교차)

### [P3-08] 무선 더 깊이 (P2-10 재분해)
- 802.11 Frame Types (Management, Control, Data)
- Beacon Frame / Probe Request
- EAP over LAN (EAPOL)
- PMK / PTK / GTK (Key Hierarchy)
- TKIP vs CCMP vs GCMP
- Wi-Fi Direct Security
- Captive Portal (보안 관점)
- Wireless Mesh Security
- Zigbee Network Key
- BLE GATT (보안 관점)
- UWB (Ultra-Wideband) Security

### [P3-09] DevSecOps 더 깊이 (P2-14 재분해)
- SARIF (Static Analysis Results Interchange Format)
- CycloneDX (SBOM Format)
- SPDX (SBOM Format)
- VEX (Vulnerability Exploitability eXchange)
- SLSA (Supply-chain Levels for Software Artifacts)
- Sigstore / Cosign / Rekor
- In-Toto (Supply Chain Attestation)
- Tekton / ArgoCD (보안 관점)
- Terraform Sentinel
- Checkov / tfsec / KICS
- Trivy (상세 — Image/Filesystem/Config Scanning)
- Semgrep (Custom Rules)
- CodeQL (GitHub)

### [P3-10] SOC/탐지 더 깊이 (P2-13 재분해)
- Sigma Rule Structure (logsource, detection, condition)
- YARA Rule Structure (meta, strings, condition)
- Snort Rule Structure (header, options)
- Suricata Rule Keywords
- ELK Stack Architecture (Elasticsearch, Logstash, Kibana)
- Splunk SPL (Search Processing Language — 보안)
- KQL (Kusto Query Language — Azure Sentinel)
- SIEM Use Case Library
- Detection Engineering
- Detection-as-Code
- MITRE D3FEND
- MITRE ATLAS (AI Threat)
- MITRE ENGAGE (Deception)
- Threat Intelligence Lifecycle
- Intelligence Requirements (PIR, EEI)
- Diamond Model (상세 — Adversary, Infrastructure, Capability, Victim)
- Campaign Tracking
- Attribution (사이버)

### [P3-11] 포렌식 더 깊이 (P2-07 재분해)
- Windows Alternate Data Streams (ADS)
- Windows WMI Event Subscription (Persistence)
- Windows Scheduled Task XML
- Registry Run Keys / Startup Folder
- Services Registry (보안)
- COM Object Hijacking (Registry)
- Browser Forensic Artifacts (History, Cache, Cookies DB)
- Email Header Forensics (Received headers, X-headers)
- Cloud Forensics Challenges (Volatility, Jurisdiction)
- Container Forensics (Layer Analysis, Runtime State)
- Mobile Forensics (Acquisition Types — Logical, Physical, File System)
- Anti-Forensics (Timestomping, Log Clearing, Secure Delete)
- Steganography (보안/포렌식)
- Covert Channel (Network, Storage)

### [P3-12] GRC/컴플라이언스 더 깊이 (P2-15 재분해)
- ISO 27001 Annex A Controls
- ISO 27005 (Risk Management)
- NIST CSF Core Functions (Identify, Protect, Detect, Respond, Recover)
- NIST CSF 2.0 (Govern 추가)
- NIST SP 800-171 (CUI Protection)
- NIST SP 800-63B (Digital Identity)
- FedRAMP
- SOC 2 Trust Service Criteria
- PCI DSS v4.0 변경사항
- HIPAA Security Rule vs Privacy Rule
- GDPR Article 25 (Data Protection by Design)
- GDPR Article 32 (Security of Processing)
- GDPR Data Transfer Mechanisms (SCCs, BCRs)
- ISO 22301 (Business Continuity)
- COBIT (IT Governance)
- ITIL (Service Management — 보안 교차)
- Vendor Risk Management (Third-Party Risk)
- Fourth-Party Risk
- Security Questionnaire (SIG, CAIQ)
- Cyber Insurance

### [P3-13] 기타 깊이 발견
- Steganography (데이터 은닉)
- Covert Channel (다시 등장 — 네트워크 + 포렌식 공유)
- Digital Watermarking
- Homomorphic Encryption (응용)
- Secure Multi-Party Computation (응용)
- Confidential Computing (TEE, SGX, SEV)
- Trusted Execution Environment (TEE)
- Remote Attestation
- SBOM Vulnerability Matching
- Software Identification (SWID Tags)
- CPE (Common Platform Enumeration)
- SCAP (Security Content Automation Protocol)
- OVAL (Open Vulnerability Assessment Language)
- XCCDF (Extensible Configuration Checklist Description Format)

---

## Pass 3 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P3-01: 암호학 | 14 |
| P3-02: AD/Windows | 21 |
| P3-03: 네트워크 | 21 |
| P3-04: 웹 | 24 |
| P3-05: 클라우드 | 17 |
| P3-06: 컨테이너/K8s | 20 |
| P3-07: AI/ML | 10 |
| P3-08: 무선 | 11 |
| P3-09: DevSecOps | 13 |
| P3-10: SOC/탐지 | 18 |
| P3-11: 포렌식 | 14 |
| P3-12: GRC | 20 |
| P3-13: 기타 | 14 |
| **Pass 3 합계** | **~217** |

---

## 전체 누적 통계

| Pass | 신규 | 누적 (원시) | 증가율 |
|------|------|-------------|--------|
| v1 (10 시드) | 323 | 323 | — |
| v2 (18 카테고리) | 349 | 672 | +108% |
| v3 (Pass 2) | 349 | 1,021 | +52% |
| **v4 (Pass 3)** | **217** | **1,238** | **+21%** ← 급감 |

| 측정 | 값 |
|------|-----|
| 원시 합계 | 1,238 |
| 기존 KB | 560 |
| 전체 (원시) | 1,798 |
| 중복 예상 | ~250 |
| **예상 고유 전체** | **~1,550** |
| **증가율 추이** | 108% → 52% → **21%** |
| **예상 수렴점** | **~1,600** |

```
증가율
108%│██████████████████████
 52%│███████████
 21%│████           ← Pass 3
 ~8%│██             ← Pass 4 예상
 ~3%│█              ← Pass 5 예상 (수렴)
    └──────────────────
     v2   v3   v4   v5   v6
```

---

*2026-02-05 v4 Pass 3 — 증가율 21%로 급감, 수렴 접근 중*
