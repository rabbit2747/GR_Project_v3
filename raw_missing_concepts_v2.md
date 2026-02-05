# 누락 개념 로우 데이터 v2

> v1 + 추가 카테고리 확장
> 분류 없음. 이름만 나열.
> 생성일: 2026-02-05

---

## 소스 A: KB 내부 Broken References (203개, CVE/UUID 제외 173개)
> v1과 동일 — 생략 (raw_missing_concepts.md 참조)

---

## 소스 B: 재귀 분해 — 카테고리별 누락 개념

### [B-01] 보안 표준/프레임워크/공통 언어
- OWASP Top 10
- OWASP Testing Guide (WSTG)
- OWASP ASVS (Application Security Verification Standard)
- OWASP SAMM (Software Assurance Maturity Model)
- OWASP Cheat Sheet Series
- CWE (Common Weakness Enumeration)
- CVE (Common Vulnerabilities and Exposures) 시스템
- CVSS (Common Vulnerability Scoring System)
- NVD (National Vulnerability Database)
- EPSS (Exploit Prediction Scoring System)
- Cyber Kill Chain (Lockheed Martin)
- Diamond Model of Intrusion Analysis
- STRIDE (Threat Modeling)
- DREAD (Risk Rating)
- IOC (Indicator of Compromise)
- IOA (Indicator of Attack)
- TTP (Tactics, Techniques, Procedures)
- STIX/TAXII (Threat Intelligence Sharing)
- ATT&CK Navigator
- Sigma Rules (Detection)
- YARA Rules (Malware Detection)
- Snort/Suricata Rules

### [B-02] 암호학 (Crypto 공격 분해)
- 대칭 암호 (Symmetric Encryption) — AES, DES, 3DES, RC4, ChaCha20
- 비대칭 암호 (Asymmetric Encryption) — RSA, ECDSA, Ed25519
- 해시 함수 (Hash Function) — SHA-256, SHA-3, MD5, bcrypt, scrypt, Argon2
- MAC (Message Authentication Code) — HMAC
- 블록 암호 모드 (CBC, GCM, ECB, CTR)
- CBC 패딩 (PKCS#7)
- 난수 생성기 (CSPRNG, PRNG)
- 키 교환 (Key Exchange) — Diffie-Hellman, ECDH
- 키 파생 (Key Derivation) — PBKDF2, HKDF
- 디지털 서명 (Digital Signature)
- SSL/TLS 핸드셰이크
- TLS 1.2 vs TLS 1.3 차이
- Certificate Chain / Chain of Trust
- Certificate Revocation (CRL, OCSP)
- Perfect Forward Secrecy (PFS)
- Cipher Suite
- Side-Channel Attack
- Timing Attack
- Rainbow Table
- Salt (암호학)
- Nonce / IV (Initialization Vector)
- Key Stretching
- Entropy (보안 관점)

### [B-03] Windows/AD 공격 (전체 분해)
- SPN (Service Principal Name)
- TGT (Ticket Granting Ticket)
- TGS (Ticket Granting Service)
- KDC (Key Distribution Center)
- KRBTGT Account
- Domain Controller
- AD Forest / Domain / Trust
- Group Policy Object (GPO)
- gMSA (Group Managed Service Account)
- NTLM Protocol
- NTLM Hash (NT Hash / LM Hash)
- Net-NTLMv1 / Net-NTLMv2
- SMB Protocol (보안 관점)
- LDAP Signing / Channel Binding
- WinRM / PSRemoting
- PowerShell (보안 관점)
- WMI (Windows Management Instrumentation)
- DCOM (Distributed COM)
- Windows Event Log (보안 이벤트)
- Event ID 4624/4625/4768/4769/4771/4776
- Windows Registry (보안 관점)
- SAM Database
- LSASS Process
- Token / Token Privilege
- Access Token / Impersonation
- UAC (User Account Control)
- ACL / DACL / SACL
- SeDebugPrivilege / SeImpersonatePrivilege
- Named Pipe
- Service Control Manager (SCM)
- DLL Hijacking
- DLL Side-Loading
- COM Hijacking
- Unquoted Service Path
- Scheduled Task (보안 관점)
- Print Spooler (PrintNightmare)
- ADCS (Active Directory Certificate Services)
- Shadow Credentials
- Resource-Based Constrained Delegation (RBCD)
- Unconstrained Delegation
- Constrained Delegation
- AdminSDHolder
- DCSync Attack Prerequisites (Replication 권한)
- SID History Injection

### [B-04] 네트워크 프로토콜/공격
- TCP 3-Way Handshake
- UDP Protocol
- ARP (Address Resolution Protocol)
- ICMP Protocol
- BGP Protocol (보안 관점)
- NTP Protocol (보안 관점)
- SNMP Protocol (보안 관점)
- DNS 캐시/TTL
- DNS Record Types (A/AAAA/CNAME/MX/NS/TXT/SRV/PTR)
- DNS Resolver vs Authoritative Server
- DNS Recursion
- DNS Zone Transfer (AXFR)
- DNSSEC
- DNS over HTTPS (DoH) / DNS over TLS (DoT)
- Kaminsky Attack
- DNS Rebinding
- DNS Amplification
- NTP Amplification
- Memcached Amplification
- SSDP Amplification
- Anycast
- Traffic Scrubbing
- BGP Blackholing / RTBH
- Slowloris / Slow HTTP Attack
- HTTP/2 (보안 관점)
- HTTP/3 / QUIC (보안 관점)
- HTTP Request Smuggling (CL.TE, TE.CL, H2.CL)
- WebSocket Protocol (보안 관점)
- VLAN (보안 관점)
- 802.1X (Port-Based NAC)
- RADIUS / TACACS+
- IPSec
- GRE Tunnel
- WireGuard
- MPLS (보안 관점)
- SDN (보안 관점)
- Network TAP / SPAN Port
- Packet Capture / PCAP

### [B-05] 웹 보안 (전체 분해)
- Same-Origin Policy (SOP)
- CORS (Cross-Origin Resource Sharing) — 메커니즘 자체
- CSP Bypass Techniques
- HttpOnly / Secure / SameSite 쿠키 플래그
- DOM Sink / Source 모델
- Event Handler (JavaScript)
- innerHTML / document.write / eval
- Content-Type / MIME Type
- MIME Sniffing / X-Content-Type-Options
- Referrer Policy
- Feature Policy / Permissions Policy
- Subresource Integrity (SRI)
- X-Frame-Options
- iFrame Sandboxing
- URL 구조 (scheme://host:port/path?query#fragment)
- URL Encoding (Percent Encoding)
- Base64 Encoding
- Double Encoding
- Unicode Normalization Attack
- HTTP Parameter Pollution (HPP)
- HTTP Methods (GET/POST/PUT/DELETE — 보안 차이)
- HTTP Header 개념 (Request/Response)
- HTTP Status Code (보안 관점 — 403/401/500)
- Redirect (301/302/307/308 — 보안 차이)
- Client-side vs Server-side Validation
- Whitelist vs Blacklist (입력 필터링)
- Escaping (HTML/JS/SQL/URL/CSS)
- HTML Entity Encoding
- String Concatenation (보안 위험)
- Template Engine (보안 관점)
- Prepared Statement / Parameterized Query (개념)
- Stored Procedure (보안 관점)
- ORM (Object-Relational Mapping)
- ORM Injection
- Dynamic Query Building
- Error Handling / Custom Error Page
- Verbose Error Message / Stack Trace 노출
- Framework Version 노출
- Reverse Proxy (개념)
- SSL/TLS Termination
- Webhook (보안 관점)
- WebSocket Hijacking
- CRLF Injection
- HTTP Response Splitting
- Host Header Injection
- Cache Poisoning (Web)
- Cache Deception
- Path Normalization Attack
- API Gateway (보안 관점)
- GraphQL 보안 (Introspection, Batching, Depth Limit)
- REST vs GraphQL 보안 비교
- JWT (JSON Web Token) 공격 — alg:none, 키 혼동
- Session Token / Session ID
- CAPTCHA (보안 관점)
- Rate Limiting (개념)
- IP Reputation
- Bot Detection
- Content Delivery Network (보안 관점)
- File Upload Validation (Magic Bytes, Extension, MIME)
- File Inclusion (Wrapper — php://, data://, expect://)
- Null Byte Injection
- Regex 기반 필터링 / 우회
- ReDoS (Regular Expression DoS)
- Second-Order Injection (일반 개념)

### [B-06] 이메일 보안
- SPF (Sender Policy Framework)
- DKIM (DomainKeys Identified Mail)
- DMARC (Domain-based Message Auth)
- ARC (Authenticated Received Chain)
- MX Record
- SMTP Relay
- Email Header Analysis
- Domain Spoofing
- Display Name Spoofing
- Homoglyph Attack (유사 문자 도메인)
- URL Shortener (보안 관점)
- QR Code Phishing (Quishing)
- 사회공학 심리 기법 (긴급성/권위/호기심/공포)
- Pretexting (상세)
- Baiting
- Tailgating / Piggybacking
- Attachment Macro 악성코드
- Phishing Kit
- Phishing-as-a-Service (PhaaS)
- OAuth Consent Phishing
- MFA Fatigue Attack
- EvilGinx / Adversary-in-the-Middle Phishing
- Credential Harvesting Page
- Email Sandbox / Detonation

### [B-07] 클라우드 보안
- Shared Responsibility Model
- Cloud Metadata API (169.254.169.254)
- IMDS v1 vs IMDS v2
- IAM Policy Language (JSON/HCL)
- IAM Condition Key
- RBAC vs ABAC (접근 제어 모델)
- Service Account / Service Principal
- Access Key / Secret Key
- Temporary Credentials (STS)
- AssumeRole / Cross-Account Trust
- S3 Bucket Policy / ACL
- CloudTrail / Cloud Audit Log
- VPC (Virtual Private Cloud)
- Security Group vs NACL
- Cloud Native Application Protection Platform (CNAPP)
- Infrastructure as Code (IaC) — Terraform, CloudFormation
- IaC Security Scanning
- Cloud Workload Identity
- Kubernetes RBAC
- Kubernetes Service Account
- Kubernetes Secrets
- Kubernetes Admission Controller
- etcd (보안 관점)
- Istio / Envoy (Service Mesh 보안)
- AWS SCP (Service Control Policy)
- AWS Organizations
- Azure Managed Identity
- GCP Workload Identity Federation

### [B-08] 컨테이너/리눅스 보안
- Linux Namespace (PID, NET, MNT, IPC, UTS, USER)
- Linux Cgroup (v1, v2)
- Linux Capabilities (CAP_SYS_ADMIN, CAP_NET_RAW, ...)
- Seccomp (Secure Computing Mode)
- AppArmor
- SELinux
- Docker Socket (/var/run/docker.sock)
- Privileged Container / --privileged
- Container Image 보안
- Image Scanning
- Container Registry 보안
- Dockerfile Best Practices (보안)
- OCI Runtime (runc, containerd, CRI-O)
- Rootless Container
- Pod Security Standards (PSS) / Pod Security Policy
- Container Breakout (CVE-2019-5736 등)
- eBPF (보안 관점)
- Host PID / Host Network
- /proc, /sys 마운트 보안
- Supply Chain (Container Image)
- SBOM (Software Bill of Materials)
- Linux Kernel (보안 관점)
- Linux Audit (auditd)
- PAM (Linux Pluggable Authentication Modules)
- sudo 보안
- SUID/SGID (보안 관점)
- Cron Job (보안 관점)
- systemd (보안 관점)
- chroot (보안 관점)

### [B-09] 앱 보안 / 역직렬화 / 코드 보안
- Serialization / Deserialization (개념)
- Gadget Chain
- Java Reflection / ClassLoader
- Java SecurityManager
- Magic Bytes / File Signature
- ysoserial (개념 — 도구 원자 후보)
- PHPGGC (개념)
- Python Pickle
- .NET BinaryFormatter
- XML Parser (SAX, DOM, StAX)
- XML Entity (Internal/External/Parameter)
- DTD (Document Type Definition)
- XSLT (보안 관점)
- SOAP (보안 관점)
- JSON Parser 보안
- Prototype (JavaScript)
- __proto__ / constructor.prototype
- Buffer Overflow (Stack, Heap)
- Use-After-Free
- Format String Attack
- Integer Overflow
- Race Condition (TOCTOU)
- Memory Safety (Rust, Go vs C/C++)
- ASLR (Address Space Layout Randomization)
- DEP/NX (Data Execution Prevention)
- Stack Canary
- CFI (Control-Flow Integrity)
- Fuzzing (보안 테스팅)
- Symbolic Execution
- Taint Analysis

### [B-10] 랜섬웨어/맬웨어 상세
- RDP (Remote Desktop Protocol) — 보안 관점
- Volume Shadow Copy (VSS)
- 3-2-1 Backup Rule
- Double Extortion
- Triple Extortion
- Ransomware-as-a-Service (RaaS)
- 암호화폐 (Bitcoin/Monero — 몸값)
- Tor Network (C2 관점)
- Malware Packing / Obfuscation
- Polymorphic Malware
- Metamorphic Malware
- Fileless Malware
- Living off the Land (LOLBins)
- Process Hollowing
- Process Injection 기법 (DLL Injection 등)
- Anti-Sandbox Techniques
- Anti-Debug Techniques
- Malware Sandbox / Detonation
- PE File Format (보안 관점)
- ELF File Format (보안 관점)
- Dropper / Stager / Loader
- C2 Framework 아키텍처
- C2 Protocol (HTTP, DNS, ICMP, Encrypted)
- Beacon / Callback
- Domain Fronting
- Fast Flux DNS
- DGA (Domain Generation Algorithm)
- Bootkit / MBR Infection
- Firmware Malware
- Wiper Malware
- Cryptominer (Cryptojacking)
- RAT (Remote Access Trojan)
- Stealer Malware
- Spyware
- Adware (보안 관점)

### [B-11] 모바일 보안
- Android Security Architecture
- iOS Security Architecture
- Mobile App Sandboxing
- Android Permission Model
- iOS Entitlements
- APK / IPA File Structure
- Mobile Code Signing
- Root Detection / Jailbreak Detection
- Frida (Mobile Hooking Tool)
- Objection (Mobile Tool)
- Certificate Pinning (Mobile)
- Mobile API Key Exposure
- Insecure Data Storage (Mobile)
- Mobile Deep Link Exploitation
- WebView 보안
- Mobile DAST/SAST
- OWASP Mobile Top 10
- MASVS (Mobile Application Security Verification Standard)

### [B-12] IoT / OT 보안
- MQTT Protocol
- CoAP Protocol
- Modbus Protocol
- OPC UA Protocol
- Zigbee / Z-Wave / BLE (보안 관점)
- Firmware Extraction / Analysis
- JTAG / UART Debugging
- Hardware Hacking (Side Channel)
- Industrial Control System (ICS) 아키텍처
- SCADA Architecture
- PLC Programming (보안 관점)
- Purdue Model (OT 네트워크 모델)
- OT/IT Convergence
- Safety Instrumented Systems (SIS)

### [B-13] 공급망 보안
- SBOM (Software Bill of Materials)
- Software Composition Analysis (SCA — 개념)
- Dependency Confusion / Substitution
- Package Manager Security (npm, pip, Maven)
- Code Signing
- Build Pipeline Security
- CI/CD Security (개념)
- Infrastructure as Code Security
- GitOps Security
- Secret Scanning
- Pre-commit Hooks (보안)
- Artifact Repository Security (Nexus, Artifactory)
- Third-party Risk Management

### [B-14] 포렌식/IR (Incident Response)
- Chain of Custody
- Digital Evidence Handling
- Memory Acquisition
- Disk Imaging
- File Carving
- Timeline Analysis
- Log Analysis (포렌식)
- Artifact Analysis (Browser, Registry, Prefetch)
- Malware Analysis (Static, Dynamic, Behavioral)
- Reverse Engineering (보안 관점)
- Incident Response Lifecycle (NIST/SANS)
- Playbook / Runbook
- Tabletop Exercise
- Post-Incident Review / Lessons Learned
- Evidence Preservation
- Volatile Data Collection
- Live Forensics vs Dead Forensics
- Anti-Forensics Techniques

### [B-15] 거버넌스/리스크/컴플라이언스 (GRC)
- Risk Assessment (정량적/정성적)
- Risk Register
- Risk Appetite / Risk Tolerance
- Business Impact Analysis (BIA)
- Business Continuity Plan (BCP)
- Disaster Recovery Plan (DRP)
- RTO / RPO
- SOX Compliance
- CCPA (California Consumer Privacy Act)
- PIPA (한국 개인정보보호법)
- ISMS-P (한국 정보보호 관리체계)
- ISO 27002 (Controls)
- NIST SP 800-53
- NIST SP 800-61 (Incident Response)
- CIS Controls / CIS Benchmarks
- CSA CCM (Cloud Controls Matrix)
- SOC 2 Type I vs Type II
- Penetration Test Scope / Rules of Engagement
- Vulnerability Disclosure Policy
- Security Maturity Model
- Security Metrics / KPI / KRI

### [B-16] WAF/탐지/방어 상세
- WAF Positive/Negative Security Model
- WAF Learning Mode / Tuning
- WAF False Positive / False Negative
- ModSecurity CRS (Core Rule Set)
- WAF Rule Writing (SecRule)
- WAF Bypass 총론
- Chunked Transfer Encoding (우회)
- HTTP Request Smuggling 총론
- Protocol-Level Evasion
- Signature-Based Detection (개념)
- Anomaly-Based Detection (개념)
- Heuristic Detection
- Behavioral Detection
- Machine Learning Detection (보안)
- Threat Hunting Methodology
- SIEM Correlation Rules
- Use Case (SIEM)
- Log Source Integration
- EDR Telemetry
- XDR Architecture
- SOAR Playbook

### [B-17] DB 보안 상세
- information_schema
- DB별 시스템 테이블 차이
- MySQL FILE 권한 (LOAD_FILE/INTO OUTFILE)
- MySQL secure_file_priv
- MySQL Conditional Comments (/*!...*/)
- MySQL User-Defined Functions (UDF)
- MSSQL xp_cmdshell
- MSSQL Linked Server
- MSSQL OPENROWSET / OPENDATASOURCE
- MSSQL CLR Assembly
- MSSQL sp_configure
- PostgreSQL COPY TO/FROM
- PostgreSQL Large Objects
- PostgreSQL pg_execute_server_program
- Oracle UTL_HTTP / UTL_FILE
- Oracle DBMS_SCHEDULER
- DB별 특수 함수 (SLEEP, WAITFOR, pg_sleep)
- SQL 주석 문법 차이 (-- / # / /*! / ;%00)
- DB 권한 관리 (GRANT/REVOKE — 보안 관점)
- DB Audit / DB Activity Monitoring
- DB Encryption (TDE, Column-level)

### [B-18] 인증/세션/접근 제어
- OAuth 2.0 Flow (Authorization Code, Client Credentials, PKCE)
- OpenID Connect (OIDC) — 상세
- SAML Flow (SP-initiated, IdP-initiated)
- JWT Attack Vectors (alg:none, key confusion, kid injection)
- Session Token Generation
- Session Fixation 메커니즘
- Session Replay Attack
- Cookie Security Attributes (HttpOnly, Secure, SameSite, Domain, Path)
- Token-Based Auth vs Session-Based Auth
- API Key vs OAuth Token vs JWT
- MFA Bypass Techniques
- MFA Fatigue / Push Bombing
- FIDO2 / WebAuthn / Passkey
- Password Policy (NIST 800-63B)
- Password Spraying (vs Brute Force)
- Credential Stuffing (상세 — Combo List, Proxy Rotation)
- Account Lockout / Account Takeover
- Broken Access Control Patterns
- IDOR (상세 — UUID Enumeration, Predictable ID)
- Privilege Escalation (Vertical vs Horizontal)
- Role-Based Access Control (RBAC) — 상세
- Attribute-Based Access Control (ABAC) — 상세
- Permission Boundary
- Just-in-Time Access (JIT)

---

## 통계 v2

| 카테고리 | v1 수 | v2 추가 | v2 합계 |
|----------|-------|---------|---------|
| A: Broken refs | 173 | 0 | 173 |
| B-01: 표준/프레임워크 | 10 | 12 | 22 |
| B-02: 암호학 | 0 | 23 | 23 |
| B-03: Windows/AD | 11 | 33 | 44 |
| B-04: 네트워크 | 10 | 28 | 38 |
| B-05: 웹 보안 | 20 | 42 | 62 |
| B-06: 이메일/사회공학 | 11 | 13 | 24 |
| B-07: 클라우드 | 7 | 21 | 28 |
| B-08: 컨테이너/리눅스 | 12 | 17 | 29 |
| B-09: 앱/코드 보안 | 9 | 21 | 30 |
| B-10: 랜섬웨어/맬웨어 | 10 | 25 | 35 |
| B-11: 모바일 | 0 | 18 | 18 |
| B-12: IoT/OT | 0 | 14 | 14 |
| B-13: 공급망 | 0 | 13 | 13 |
| B-14: 포렌식/IR | 0 | 18 | 18 |
| B-15: GRC | 0 | 21 | 21 |
| B-16: WAF/탐지 | 5 | 16 | 21 |
| B-17: DB 보안 | 11 | 10 | 21 |
| B-18: 인증/세션 | 0 | 24 | 24 |
| **소스 B 합계** | ~150 | ~349 | **~499** |
| **A+B 원시 합계** | | | **~672** |
| 중복 예상 (A∩B + B내 중복) | | | ~120 |
| **예상 고유 합계** | | | **~550** |

---

*2026-02-05 v2 — 18개 카테고리 전면 확장*
