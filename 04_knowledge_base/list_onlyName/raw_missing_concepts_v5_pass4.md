# 누락 개념 로우 데이터 v5 (Pass 4)

> v4의 ~217개 항목을 재분해
> 이미 발견된 ~1,550개 + 기존 KB 560개에 없는 것만 추출
> 생성일: 2026-02-05

---

## Pass 4: v4 항목 재분해에서 나온 신규 개념

### [P4-01] 암호 인프라/표준 (P3-01 재분해)
- PKCS#11 (Cryptographic Token Interface)
- PKCS#12 (.pfx/.p12 — 키+인증서 번들)
- JKS (Java Key Store)
- OpenSSL (보안 관점 — Heartbleed 등)
- LibreSSL / BoringSSL
- Certificate Lifecycle Management
- ACME Challenge Types (HTTP-01, DNS-01, TLS-ALPN-01)
- SCT (Signed Certificate Timestamp)
- Key Transparency
- MLS (Messaging Layer Security)
- Signal Protocol
- Noise Protocol Framework
- Double Ratchet Algorithm

### [P4-02] AD 공격 체인 말단 (P3-02 재분해)
- Whisker (Shadow Credentials Tool — 개념)
- KrbRelayUp
- Certifried (CVE-2022-26923)
- UnPAC-the-Hash
- S4U2Self / S4U2Proxy (Kerberos Extension)
- Bronze Bit Attack (CVE-2020-17049)
- AD ACL Abuse Patterns (WriteDACL → DCSync chain)
- LAPS Credential Reading
- gMSA Password Reading (msDS-ManagedPassword)
- Machine Account Quota Abuse
- ADCS Web Enrollment (보안)
- NTLMv1 Downgrade via GPO

### [P4-03] 프로토콜 엣지 케이스 (P3-03 재분해)
- TCP Simultaneous Open
- QUIC 0-RTT (보안 위험 — Replay)
- TLS Session Resumption (보안 관점)
- TLS False Start
- ALPN (Application-Layer Protocol Negotiation)
- SNI (Server Name Indication) — 도청/차단 관점
- ESNI / ECH (Encrypted Client Hello)
- DNS HTTPS Record (SVCB/HTTPS RR)
- Multicast DNS (mDNS) / LLMNR 보안
- NBNS (NetBIOS Name Service) — 포이즈닝
- WPAD (Web Proxy Auto-Discovery) 공격
- PAC File Injection

### [P4-04] 웹 엣지 케이스 (P3-04 재분해)
- HTTP Desync (Request Smuggling 변형)
- Transfer-Encoding Obfuscation
- HTTP/2 CONTINUATION Flood (CVE-2024)
- Browser-Based Desync
- Client-Side Prototype Pollution → DOM XSS
- Server-Side Prototype Pollution → RCE
- Class Pollution (Python)
- AST Injection
- ReDoS via Catastrophic Backtracking (상세)
- Regex Injection
- LDAP Injection via JNDI
- Log4Shell Kill Chain (JNDI → LDAP → Deserialization)
- Expression Language Injection (EL/SpEL/OGNL)
- Server-Side Include (SSI) Injection
- Edge-Side Include (ESI) Injection 상세

### [P4-05] 클라우드 엣지 케이스 (P3-05 재분해)
- AWS Confused Deputy Problem
- AWS Cross-Account Access Patterns
- AWS Resource Policy vs Identity Policy
- AWS Permission Boundary
- AWS Tag-Based Access Control
- AWS VPC Endpoint Policy
- Azure Conditional Access Policy
- Azure PIM (Privileged Identity Management)
- GCP Assured Workloads
- Kubernetes Secrets Encryption (상세 — KMS provider)
- Kubernetes External Secrets Operator
- Kubernetes Service Account Token Volume Projection
- Cloud Metadata Proxy (GKE, EKS)

### [P4-06] 맬웨어/레드팀 엣지 (P3-06 재분해)
- Direct Syscall (Nt*/Zw*)
- Indirect Syscall (via ntdll gadget)
- Callback-Based Shellcode Execution (EnumWindows 등)
- Fiber-Based Execution
- Hardware Breakpoint Hooking
- ETW Patching (NtTraceEvent)
- AMSI Bypass Techniques (상세 — AmsiScanBuffer patch)
- Unhooking (ntdll remapping)
- Phantom DLL Hollowing
- Transacted Hollowing
- Process Ghosting
- Process Doppelgänging
- Process Herpaderping
- Module Overloading
- Gargoyle (Timer-Based Sleep)
- Ekko / Nighthawk (Encrypted Sleep)
- Return-Oriented Programming (ROP)
- Jump-Oriented Programming (JOP)
- Sigreturn-Oriented Programming (SROP)

### [P4-07] 포렌식/탐지 엣지 (P3-10, P3-11 재분해)
- ETW Provider Enumeration
- ETW Consumer (Trace Session)
- Sysmon Configuration Best Practices
- Sigma Rule Modifiers (all, base64offset, re)
- YARA Modules (pe, math, hash)
- Velociraptor (DFIR 도구 — 개념)
- GRR Rapid Response (개념)
- KAPE (Kroll Artifact Parser — 개념)
- Eric Zimmerman Tools (개념)
- Plaso/log2timeline (개념)
- OSQuery (엔드포인트 쿼리)
- Chainsaw (Windows Event Log — 개념)

### [P4-08] DevSecOps/공급망 엣지 (P3-09 재분해)
- SLSA Levels (L1-L4)
- Provenance (소프트웨어 출처)
- Build Reproducibility
- Hermetic Build
- Binary Authorization (GKE)
- Tekton Chains
- GUAC (Graph for Understanding Artifact Composition)
- Scorecard (OpenSSF)
- AllStar (OpenSSF)
- Dependency Track
- Renovate / Dependabot (보안 관점)
- Mend / Snyk (SCA 개념)

### [P4-09] GRC 말단 (P3-12 재분해)
- NIST RMF (Risk Management Framework) 7 Steps
- FAIR (Factor Analysis of Information Risk)
- Bow-Tie Risk Model
- Risk Heat Map / Risk Matrix
- Control Effectiveness Rating
- Residual Risk vs Inherent Risk
- Key Risk Indicator (KRI) Examples
- Cyber Risk Quantification
- TPRM (Third-Party Risk Management) Lifecycle
- SIG Questionnaire (Shared Assessments)
- CAIQ (Consensus Assessments Initiative Questionnaire)
- SOC 2 Type I vs Type II 차이 (상세)

### [P4-10] AI/ML 말단 (P3-07 재분해)
- Embedding Inversion Attack
- Model Backdoor (Trojan)
- Dataset Bias (보안 관점)
- Adversarial Patch (물리적)
- LLM Token Smuggling
- Indirect Prompt Injection via Retrieved Context
- Insecure Output Handling (LLM)
- Excessive Agency (LLM)
- OWASP Top 10 for LLM (상세 — LLM01~LLM10)

### [P4-11] 물리/하드웨어 말단 (P3-11 재분해)
- Glitching Attack (Voltage, Clock, EM)
- Cold Boot Attack
- Bus Snooping (SPI, I2C, JTAG)
- Firmware Rootkit
- BIOS/UEFI Secure Boot
- Measured Boot / Trusted Boot
- TPM Remote Attestation
- Intel ME / AMD PSP (보안 관점)

### [P4-12] 블록체인 말단 (v3 P2-17 재분해)
- EVM (Ethereum Virtual Machine) 보안
- Solidity Reentrancy Guard
- tx.origin vs msg.sender
- Delegatecall Vulnerability
- Selfdestruct Attack
- Storage Collision (Proxy Pattern)
- Signature Replay Attack (Web3)
- EIP-712 (Typed Data Signing)
- Permit/Permit2 Phishing
- Private Mempool / Flashbots

---

## Pass 4 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P4-01: 암호 인프라 | 13 |
| P4-02: AD 말단 | 12 |
| P4-03: 프로토콜 엣지 | 12 |
| P4-04: 웹 엣지 | 15 |
| P4-05: 클라우드 엣지 | 13 |
| P4-06: 맬웨어/레드팀 | 19 |
| P4-07: 포렌식/탐지 | 12 |
| P4-08: DevSecOps/공급망 | 12 |
| P4-09: GRC | 12 |
| P4-10: AI/ML | 9 |
| P4-11: 물리/하드웨어 | 8 |
| P4-12: 블록체인 | 10 |
| **Pass 4 합계** | **~147** |

---

## 전체 누적 통계

| Pass | 신규 | 누적 (원시) | 증가율 |
|------|------|-------------|--------|
| v1 | 323 | 323 | — |
| v2 | 349 | 672 | +108% |
| v3 (Pass 2) | 349 | 1,021 | +52% |
| v4 (Pass 3) | 217 | 1,238 | +21% |
| **v5 (Pass 4)** | **147** | **1,385** | **+12%** |

| 측정 | 값 |
|------|-----|
| 원시 합계 | 1,385 |
| 기존 KB | 560 |
| 전체 (원시) | 1,945 |
| 중복 예상 | ~310 |
| **예상 고유 전체** | **~1,635** |

```
증가율 추이
108% │████████████████████████████
 52% │██████████████
 21% │██████
 12% │███          ← Pass 4 (지금)
  5% │█            ← Pass 5 예상
  2% │             ← Pass 6 (수렴)
     └────────────────────────
      v2   v3   v4   v5   v6
```

```
고유 개념 수
1700 │                                ╌╌╌ 수렴 (~1,650-1,700)
1635 │                          ╭─────── ← 지금 여기
1550 │                     ╭────╯
1400 │                ╭────╯
1100 │          ╭─────╯
 560 │──────────╯
     └──────────────────────────────
      KB    v1   v2   v3   v4  수렴
```

**Pass 5 예상: +50~70개 (전문가급 니치), 그 후 수렴**

---

*2026-02-05 v5 Pass 4 — 증가율 12%, 수렴 근접*
