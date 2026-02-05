# 누락 개념 로우 데이터 v3 (Pass 2)

> v2의 ~550개 개념을 재분해하여 추가 발견된 개념
> + 아직 다루지 않은 전체 도메인 추가
> 생성일: 2026-02-05

---

## Pass 2: v2 항목 재분해에서 나온 신규 개념

### [P2-01] 암호학 깊이 확장 (v2 B-02 재분해)
- Block Cipher vs Stream Cipher
- Plaintext / Ciphertext
- Padding (PKCS#5, PKCS#7, OAEP)
- Padding Oracle (개념 — 공격은 있으나 메커니즘 개념 없음)
- Key Length (128/192/256-bit 보안 수준)
- Key Rotation / Key Lifecycle
- Key Escrow
- Hardware Security Module (HSM)
- Trusted Platform Module (TPM)
- Secure Enclave (SGX, ARM TrustZone)
- Post-Quantum Cryptography (PQC)
- Lattice-Based Cryptography
- Elliptic Curve (보안 관점)
- Certificate Transparency (CT)
- CT Log Monitor
- HPKP (HTTP Public Key Pinning) — deprecated but conceptual
- OCSP Stapling
- Certificate Authority (CA) 구조
- Root CA / Intermediate CA / Leaf Certificate
- X.509 Certificate 구조
- ASN.1 / DER / PEM (인증서 형식)
- Key Pair Generation
- Entropy Source (하드웨어/소프트웨어)
- Cryptographic Agility

### [P2-02] Windows/AD 깊이 확장 (v2 B-03 재분해)
- Kerberos Realm vs AD Domain
- Kerberos Delegation 총론 (Unconstrained/Constrained/RBCD)
- NTDS.dit (AD 데이터베이스)
- Active Directory Replication
- AD Sites and Services
- Organizational Unit (OU)
- Security Group vs Distribution Group
- Well-Known SIDs (S-1-5-18, S-1-5-21-...)
- RID (Relative Identifier)
- DSRM (Directory Services Restore Mode)
- AD Certificate Template
- ESC1-ESC8 (ADCS 공격 벡터)
- Kerberos Pre-Authentication
- AS-REQ / AS-REP / TGS-REQ / TGS-REP
- PAC (Privilege Attribute Certificate)
- MS-RPC / MS-DRSR / MS-NRPC
- NetLogon (Zerologon 관련)
- SYSVOL / NETLOGON Share
- Group Policy Preference (GPP) — 암호 노출
- Windows Credential Storage (Credential Manager, Vault)
- DPAPI (Data Protection API)
- LSA Secrets
- WDigest
- Credential Guard vs LSASS Protection
- Protected Users Group
- Tier Model (AD 관리 계층)
- Red Forest / ESAE (Enhanced Security Admin Environment)
- BloodHound (개념 — 도구는 있으나 그래프 이론 개념 없음)
- Attack Path Analysis
- AD Object Permissions (GenericAll, WriteDACL, etc.)

### [P2-03] 네트워크 깊이 확장 (v2 B-04 재분해)
- EAP (Extensible Authentication Protocol)
- EAP-TLS / PEAP / EAP-TTLS
- IKE (Internet Key Exchange) v1/v2
- ESP (Encapsulating Security Payload)
- SA (Security Association)
- NAT (Network Address Translation — 보안 관점)
- NAC (Network Access Control)
- Microsegmentation
- East-West Traffic vs North-South Traffic
- Network Tap vs SPAN Port 차이
- Deep Packet Inspection (DPI)
- TLS Inspection / SSL Decryption
- Proxy Chain / Proxy Hop
- Tor Circuit / Onion Routing
- I2P Network
- VPN Split Tunneling (보안 관점)
- Wireguard vs IPSec vs OpenVPN 비교
- DNS Sinkholing
- Passive DNS
- NetFlow / sFlow / IPFIX
- Network Baseline / Anomaly
- Honeypot / Honeynet
- Darknet / Unused IP Space Monitoring
- ARP Inspection (Dynamic ARP Inspection)
- DHCP Snooping
- Port Security (MAC address filtering)
- STP Attack (Spanning Tree Protocol)
- LLDP/CDP Reconnaissance

### [P2-04] 웹 보안 깊이 확장 (v2 B-05 재분해)
- Fetch API / XMLHttpRequest (보안 관점)
- Service Worker (보안 관점)
- Web Worker (보안 관점)
- postMessage (Cross-Origin Communication)
- window.opener (보안 관점)
- Blob URL / Data URL (보안 관점)
- SourceMap (정보 유출)
- Browser Extension Security
- Browser Storage (localStorage, sessionStorage, IndexedDB — 보안)
- Content Sniffing vs Content-Type
- HTTP Caching (Cache-Control, ETag — 보안 관점)
- HTTP Strict Transport Security (HSTS) Preload
- Cookie Scope / Cookie Tossing
- Cookie Jar Overflow
- Browser Fingerprinting
- Clickjacking Defense (frame-ancestors)
- SameSite Cookie Attribute (Strict/Lax/None)
- Spectre/Meltdown (브라우저 관점)
- Site Isolation
- Cross-Origin Embedder Policy (COEP)
- Cross-Origin Opener Policy (COOP)
- Cross-Origin Resource Policy (CORP)
- Trusted Types API
- Dangling Markup Injection
- CSS Injection
- Relative Path Overwrite (RPO)
- Web Cache Deception vs Cache Poisoning 차이
- Edge Side Include (ESI) Injection

### [P2-05] 클라우드 깊이 확장 (v2 B-07 재분해)
- AWS VPC 아키텍처 (Subnet, Route Table, IGW, NAT GW)
- AWS Security Group vs NACL 차이
- AWS KMS (Key Management Service)
- AWS CloudWatch / CloudWatch Logs
- AWS GuardDuty
- AWS Config / Config Rules
- AWS WAF vs Third-party WAF
- Azure NSG (Network Security Group)
- Azure Key Vault
- Azure Sentinel (SIEM)
- Azure Policy / Blueprint
- GCP VPC Service Controls
- GCP Security Command Center
- Multi-Account / Multi-Subscription Strategy
- Landing Zone (보안 관점)
- PrivateLink / Private Endpoint
- Cloud HSM
- Serverless Security 상세 (Cold Start, Event Injection)
- Container-as-a-Service Security (ECS, EKS, AKS, GKE)
- Cloud Run / Cloud Functions Security
- Object Storage Presigned URL (보안)
- CloudFormation / Terraform State File (보안)

### [P2-06] 맬웨어/위협 깊이 확장 (v2 B-10 재분해)
- Import Address Table (IAT) Hooking
- API Hooking (inline, trampoline)
- Syscall (Direct Syscall / Indirect Syscall)
- AMSI (Antimalware Scan Interface) Bypass
- ETW (Event Tracing for Windows) Evasion
- Windows API (CreateRemoteThread, NtCreateSection 등 — 보안 관점)
- Shellcode (개념)
- Shellcode Encoder/Decoder
- Position Independent Code (PIC)
- Reflective DLL Injection
- Module Stomping
- Heaven's Gate (WoW64 Abuse)
- Early Bird Injection
- APC Injection
- Thread Pool Injection
- PPID Spoofing
- Command Line Obfuscation
- LOLBas (상세 — certutil, mshta, regsvr32, rundll32)
- WDAC (Windows Defender Application Control)
- Constrained Language Mode (PowerShell)
- Script Block Logging
- Obfuscation (Base64, XOR, AES Encrypt)
- Packer (UPX, Themida, VMProtect)
- Anti-VM Detection (Registry, MAC, Timing)
- Sandbox Evasion (Sleep, User Interaction, Environment)

### [P2-07] 포렌식/IR 깊이 확장 (v2 B-14 재분해)
- Windows Prefetch
- Windows Amcache / Shimcache
- Windows Jump Lists
- Windows ShellBags
- $MFT / $UsnJrnl (NTFS Artifacts)
- Windows Event Log Channels (Security, System, PowerShell)
- Sysmon (System Monitor)
- Sysmon Event ID (1, 3, 7, 8, 10, 11, 22, 23)
- Linux /var/log/ 구조
- Linux .bash_history / auth.log / syslog
- Linux /proc 파일시스템 (포렌식)
- Memory Forensics (프로세스 목록, 네트워크 연결, 인젝션 탐지)
- Volatility Plugins (pslist, netscan, malfind)
- PCAP Analysis (Wireshark Filters)
- Zeek/Bro Logs
- Suricata / Snort Alert Analysis
- Threat Intelligence Platform (TIP) 아키텍처
- MISP (Malware Information Sharing Platform)
- Kill Chain Mapping
- ATT&CK Mapping
- Diamond Model Application

### [P2-08] 인증/접근 깊이 확장 (v2 B-18 재분해)
- OAuth 2.0 Token Types (Access, Refresh, ID)
- OAuth 2.0 Grant Types 상세 (Auth Code, Client Credentials, Device, PKCE)
- OAuth 2.0 Scope
- JWT Header / Payload / Signature 구조
- JWT Claims (iss, sub, aud, exp, nbf, iat, jti)
- JWK / JWKS (JSON Web Key Set)
- JWE (JSON Web Encryption)
- SAML Assertion Structure
- SAML Relay State
- SAML Response Wrapping Attack
- OpenID Connect Discovery
- OpenID Connect UserInfo Endpoint
- Bcrypt / Scrypt / Argon2 비교
- Password Hashing 원리
- Credential Database (Breach — Have I Been Pwned 등)
- U2F vs FIDO2 vs WebAuthn 관계
- TOTP / HOTP (Time-based / HMAC-based OTP)
- Authenticator App vs Hardware Key vs SMS
- Risk-Based Authentication
- Adaptive Authentication
- Step-Up Authentication
- Session Management Best Practices (Timeout, Rotation, Binding)

---

## Pass 2: 미탐색 도메인 (v2에서 아예 빠진 영역)

### [P2-09] AI/ML 보안 (신규 도메인)
- Adversarial Machine Learning
- Adversarial Examples (Evasion Attack)
- Data Poisoning
- Model Stealing / Model Extraction
- Membership Inference Attack
- Prompt Injection (LLM)
- Indirect Prompt Injection
- Jailbreaking (LLM)
- AI Hallucination (보안 관점)
- LLM Data Leakage
- Training Data Extraction
- AI Supply Chain (Model Zoo, Hugging Face)
- MLOps Security
- AI Red Teaming
- OWASP Top 10 for LLM
- Deepfake (보안 관점)
- Voice Cloning Attack
- AI-Generated Phishing

### [P2-10] 무선 보안 (신규 도메인)
- WPA2 / WPA3
- WPA2-PSK vs WPA2-Enterprise
- 4-Way Handshake (Wi-Fi)
- PMKID Attack
- Evil Twin Attack
- Karma Attack
- Rogue Access Point
- Deauthentication Attack
- KRACK Attack (WPA2)
- DragonBlood (WPA3)
- Wi-Fi Protected Setup (WPS) Attack
- Wireless IDS/IPS
- Bluetooth Security (Pairing, MITM)
- BLE (Bluetooth Low Energy) Attack
- NFC Security
- RFID Cloning
- RF Jamming
- War Driving / War Walking

### [P2-11] 물리적 보안 (신규 도메인)
- Physical Access Control
- Badge Cloning (HID, Proxmark)
- Tailgating / Piggybacking (물리)
- Lock Picking (보안 관점)
- USB Drop Attack
- Rubber Ducky / BadUSB 상세
- Network Implant (LAN Turtle, WiFi Pineapple)
- Screen Shoulder Surfing
- Dumpster Diving
- Clean Desk Policy
- TEMPEST / Van Eck Phreaking
- Electromagnetic Side Channel

### [P2-12] 개인정보보호 / 데이터 보안 (신규 도메인)
- PII (Personally Identifiable Information)
- PHI (Protected Health Information)
- Data Classification (Public/Internal/Confidential/Restricted)
- Data Masking / Tokenization
- Data Anonymization / Pseudonymization
- Data Retention Policy
- Right to Erasure (GDPR Art. 17)
- Data Subject Access Request (DSAR)
- Privacy by Design
- Privacy Impact Assessment (PIA)
- Data Protection Officer (DPO)
- Cross-Border Data Transfer (Adequacy Decision, SCCs)
- Cookie Consent / ePrivacy
- Differential Privacy
- Homomorphic Encryption
- Secure Multi-Party Computation (SMPC)
- Zero-Knowledge Proof (보안 관점)

### [P2-13] 보안 운영 (SOC) (신규 도메인)
- SOC Maturity Model
- SOC Analyst Tiers (L1/L2/L3)
- Alert Triage
- Alert Fatigue
- Mean Time to Detect (MTTD)
- Mean Time to Respond (MTTR)
- Security Metrics / KPI / KRI
- SLA for Security Incidents
- Severity Classification (P1-P4)
- Escalation Procedure
- War Room / Incident Bridge
- Communication Plan (Internal/External)
- Security Dashboard
- Threat Brief / Intelligence Report
- Purple Team Exercise
- Red Team Rules of Engagement
- Blue Team Playbook
- Deception Technology (상세 — Honeypot, Honeytoken, Canary)
- Canary Token

### [P2-14] DevSecOps 상세 (신규 도메인)
- Shift Left Security
- Security Champion Program
- Threat Modeling in SDLC (STRIDE, PASTA, LINDDUN)
- PASTA Threat Modeling
- Secure Code Review
- SAST Rule Customization
- DAST Crawling / Active Scan
- IAST (Interactive AST)
- RASP (Runtime Application Self-Protection)
- Dependency Vulnerability (CVE in Libraries)
- License Compliance (Open Source)
- Container Image Signing (Cosign, Notary)
- OPA (Open Policy Agent)
- Policy-as-Code
- GitOps Security Model
- Branch Protection / Code Review Requirements
- Secrets Detection (git-secrets, truffleHog, gitleaks)
- Pre-commit / Pre-push Hooks
- Deployment Gate / Security Gate
- Feature Flag Security
- Canary Deployment (보안 관점)
- Blue/Green Deployment (보안 관점)

### [P2-15] 취약점 관리 라이프사이클 (신규 도메인)
- Vulnerability Scanning (Authenticated vs Unauthenticated)
- Vulnerability Assessment vs Penetration Test
- Risk-Based Vulnerability Management
- Vulnerability Prioritization (CVSS + EPSS + Context)
- SLA-Based Patching
- Virtual Patching
- Compensating Control
- Exception / Risk Acceptance
- Asset Inventory / CMDB
- Attack Surface Management (External — EASM)
- Shadow IT Discovery
- Vulnerability Chaining
- Exploit Development Lifecycle
- Proof of Concept (PoC) vs Weaponized Exploit
- Exploit Broker / Zero-Day Market
- Responsible Disclosure vs Full Disclosure
- Bug Bounty Platform (HackerOne, Bugcrowd)
- VDP (Vulnerability Disclosure Program)

### [P2-16] Zero Trust 아키텍처 상세 (신규 도메인)
- Zero Trust Principles (Never Trust, Always Verify)
- Zero Trust Pillars (Identity, Device, Network, App, Data)
- NIST SP 800-207 (Zero Trust Architecture)
- Software-Defined Perimeter (SDP)
- BeyondCorp (Google)
- ZTNA (Zero Trust Network Access)
- Identity-Centric Security
- Device Trust / Device Posture
- Continuous Verification
- Micro-Perimeter
- Zero Trust Data Access (ZTDA)
- SASE (Secure Access Service Edge)
- SSE (Security Service Edge)

### [P2-17] Blockchain / Web3 보안 (신규 도메인)
- Smart Contract Vulnerability (Reentrancy, Integer Overflow)
- Flash Loan Attack
- Front-Running / MEV
- Rug Pull
- Private Key Management (Wallet)
- Seed Phrase Security
- Bridge Attack (Cross-chain)
- Oracle Manipulation
- 51% Attack
- Sybil Attack
- Governance Attack
- DeFi Exploit Patterns
- NFT Security
- Phishing (Web3 — Approve/SetApprovalForAll)

---

## Pass 2 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P2-01: 암호학 깊이 | 24 |
| P2-02: Windows/AD 깊이 | 30 |
| P2-03: 네트워크 깊이 | 28 |
| P2-04: 웹 보안 깊이 | 28 |
| P2-05: 클라우드 깊이 | 21 |
| P2-06: 맬웨어/위협 깊이 | 24 |
| P2-07: 포렌식/IR 깊이 | 21 |
| P2-08: 인증/접근 깊이 | 22 |
| P2-09: AI/ML 보안 ⭐신규 | 18 |
| P2-10: 무선 보안 ⭐신규 | 18 |
| P2-11: 물리적 보안 ⭐신규 | 12 |
| P2-12: 개인정보보호 ⭐신규 | 17 |
| P2-13: 보안 운영(SOC) ⭐신규 | 19 |
| P2-14: DevSecOps 상세 ⭐신규 | 22 |
| P2-15: 취약점 관리 ⭐신규 | 18 |
| P2-16: Zero Trust 상세 ⭐신규 | 13 |
| P2-17: Blockchain/Web3 ⭐신규 | 14 |
| **Pass 2 합계** | **~349** |

---

## 누적 통계

| 버전 | 소스 | 항목 수 | 누적 (원시) |
|------|------|---------|-------------|
| v1 | A: Broken refs | 173 | 173 |
| v1 | B: 10 시드 분해 | ~150 | 323 |
| v2 | B 확장: 18 카테고리 | +349 | 672 |
| **v3** | **Pass 2: 재분해 + 신규 도메인** | **+349** | **1,021** |

| 측정 | 값 |
|------|-----|
| 원시 합계 (A+B 전체) | ~1,021 |
| 기존 KB | 560 |
| 원시 합계 + 기존 | 1,581 |
| 중복 예상 (v3 내 + 기존 KB와) | ~180 |
| **예상 고유 전체** | **~1,400** |
| **성장률 (v2→v3)** | 550→840 (+290, 53% 증가) |
| **예상 수렴점** | ~1,500-1,600 |

---

*2026-02-05 v3 Pass 2 — 17개 서브카테고리, 9개 신규 도메인*
