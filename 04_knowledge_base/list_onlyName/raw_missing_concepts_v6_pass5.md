# 누락 개념 로우 데이터 v6 (Pass 5)

> v5의 ~147개 항목을 재분해
> 이미 ~1,635 + KB 560 에 없는 것만 추출
> 생성일: 2026-02-05

---

## Pass 5: v5 항목 재분해에서 나온 신규 개념

### [P5-01] 암호/PKI 말단
- DANE (DNS-Based Authentication of Named Entities)
- CAA (Certification Authority Authorization) DNS Record
- CT Precertificate
- Short-Lived Certificate (보안 이점)
- mTLS (Mutual TLS)
- TLS Fingerprinting Evasion (JA3 randomization)
- Cryptographic Downgrade Prevention (TLS_FALLBACK_SCSV)
- HPKE (Hybrid Public Key Encryption)

### [P5-02] AD/Kerberos 극한
- Diamond Ticket
- Sapphire Ticket
- Golden Certificate (ADCS)
- ESC9 / ESC10 / ESC11 (최신 ADCS 벡터)
- Relay to ADCS (NTLM → Certificate)
- Shadow Credentials (msDS-KeyCredentialLink)
- PKINIT (Kerberos Certificate Auth)
- UnPAC-the-Hash (PKINIT 악용)
- sAMAccountName Spoofing (CVE-2021-42278/42287)
- AD Honeypot Account / Honeytoken SPN

### [P5-03] 프로토콜 극한
- LLMNR Poisoning (상세)
- mDNS Poisoning (상세)
- DHCPv6 Poisoning
- IPv6 Security (RA Guard, NDP)
- Neighbor Discovery Protocol (NDP) Attack
- Router Advertisement (RA) Attack
- SEND (SEcure Neighbor Discovery)
- DNS Cookie (RFC 7873)
- DNS EDNS Client Subnet (ECS) Privacy
- Happy Eyeballs (Dual Stack — 보안)

### [P5-04] 웹 극한
- HTTP/2 Rapid Reset Attack (CVE-2023-44487)
- WebTransport Security
- Web Bundle / Web Package (보안)
- Speculation Rules API (보안 관점)
- Sanitizer API (브라우저)
- Import Maps (보안 관점)
- Supply Chain Attack via CDN (cdn.js compromise)
- Subdomain Delegation Takeover (NS Record)
- Dangling CNAME Takeover
- Host Header Cache Poisoning
- Web Socket Smuggling
- H2C Smuggling (상세)

### [P5-05] 레드팀/이베이전 극한
- Sleep Obfuscation (Foliage, Ekko, Nighthawk — 개념)
- Stack Spoofing (Call Stack Masking)
- Thread Stack Spoofing
- User-Mode Hook Evasion (Manual Mapping)
- Kernel Callback Removal
- PPL (Protected Process Light) Bypass
- Token Duplication (from SYSTEM)
- Handle Inheritance Abuse
- Named Pipe Impersonation (상세)
- COM Object Abuse (DCOM Lateral)
- WMI Event Subscription Persistence (상세)
- Scheduled Task XML Modification
- Boot Configuration Data (BCD) Tampering
- Bootkit — UEFI Persistence

### [P5-06] 탐지/방어 극한
- YARA-L (Chronicle/Google SecOps)
- KQL Advanced Operators (Azure)
- SPL Subsearch / Macro (Splunk)
- Detection Gap Analysis
- Threat-Informed Defense
- MITRE ATT&CK Coverage Heatmap
- Purple Team Atomic Testing (Atomic Red Team)
- Breach and Attack Simulation (BAS) 상세
- Continuous Automated Red Teaming (CART)
- Adversary Emulation Plan
- C2 Matrix (C2 프레임워크 비교)
- Malleable C2 Profile
- Redirector (C2 인프라)

### [P5-07] 클라우드/K8s 극한
- Kubernetes Ephemeral Container (보안)
- Kubernetes Pod Security Admission (PSA)
- Kubernetes ValidatingAdmissionPolicy (CEL)
- AWS IMDSv2 Hop Limit
- AWS VPC Lattice (보안)
- AWS Verified Access
- Azure Entra Workload ID
- Azure Bicep / ARM Template (보안)
- GCP Binary Authorization
- Kubernetes CIS Benchmark
- kube-bench / kube-hunter

### [P5-08] AI/ML 극한
- Guardrails (LLM)
- Content Filtering (LLM)
- Red Teaming LLM (Methodology)
- AI Firewall / AI Gateway
- Prompt Leaking vs Prompt Injection 차이
- Fine-Tuning Attack (Backdoor via Training)
- RLHF (Reinforcement Learning from Human Feedback — 보안)
- Constitutional AI (보안 관점)

### [P5-09] IoT/OT 극한
- Modbus TCP Security (lack of auth)
- OPC UA Security Model (Certificates, Policies)
- IEC 62443 (Industrial Cybersecurity Standard)
- NERC CIP (전력 인프라 보안)
- DNP3 Secure Authentication
- CAN Bus Security (자동차)
- Automotive Ethernet Security
- V2X (Vehicle-to-Everything) Security
- Medical Device Security (FDA Guidance)
- DICOM Security (의료 영상)

### [P5-10] 개인정보/법률 극한
- Data Localization Requirements
- Schrems II (EU-US Data Transfer)
- PIPL (중국 개인정보보호법)
- APPI (일본 개인정보보호법)
- LGPD (브라질)
- DORA (Digital Operational Resilience Act — EU 금융)
- NIS2 Directive (EU)
- Cyber Resilience Act (EU — IoT)
- SEC Cybersecurity Disclosure Rules (미국)
- Korea ISMS-P 인증 기준 (상세)
- Korea 전자금융감독규정
- Korea 정보통신망법

### [P5-11] 블록체인 극한
- MEV (Maximal Extractable Value) 상세
- Sandwich Attack
- Time-Bandit Attack
- Governance Token Attack
- Cross-Chain Bridge Verification
- Zero-Knowledge Rollup Security
- Account Abstraction Security (ERC-4337)

### [P5-12] 기타 미분류 극한
- Satellite Communication Security
- Underwater Cable Security (개념)
- Space Cybersecurity
- Quantum Computing Threat Timeline
- Y2Q (Years to Quantum)
- Crypto-Agility Roadmap
- Digital Twin Security
- Operational Technology Honeypot (Conpot)
- Election Security
- Deepfake Detection
- Synthetic Identity Fraud

---

## Pass 5 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P5-01: 암호/PKI | 8 |
| P5-02: AD/Kerberos | 10 |
| P5-03: 프로토콜 | 10 |
| P5-04: 웹 | 12 |
| P5-05: 레드팀/이베이전 | 14 |
| P5-06: 탐지/방어 | 13 |
| P5-07: 클라우드/K8s | 11 |
| P5-08: AI/ML | 8 |
| P5-09: IoT/OT | 10 |
| P5-10: 개인정보/법률 | 12 |
| P5-11: 블록체인 | 7 |
| P5-12: 기타 | 11 |
| **Pass 5 합계** | **~126** |

---

## 전체 누적 통계

| Pass | 신규 | 누적 (원시) | 증가율 |
|------|------|-------------|--------|
| v1 | 323 | 323 | — |
| v2 | 349 | 672 | +108% |
| v3 | 349 | 1,021 | +52% |
| v4 | 217 | 1,238 | +21% |
| v5 | 147 | 1,385 | +12% |
| **v6 (Pass 5)** | **126** | **1,511** | **+9%** |

| 측정 | 값 |
|------|-----|
| 원시 합계 | 1,511 |
| 기존 KB | 560 |
| 전체 | 2,071 |
| 중복 예상 | ~350 |
| **예상 고유 전체** | **~1,720** |

```
증가율 추이
108% │████████████████████████████
 52% │██████████████
 21% │██████
 12% │███
  9% │██           ← Pass 5 (지금)
 ~4% │█            ← Pass 6 예상
 ~2% │             ← Pass 7 (수렴)
     └────────────────────────
      v2   v3   v4   v5   v6  v7
```

```
고유 개념 수
1750 │                                   ╌╌ 수렴 (~1,750)
1720 │                             ╭─────── ← 지금 여기
1635 │                        ╭────╯
1550 │                   ╭────╯
1400 │              ╭────╯
1100 │        ╭─────╯
 560 │────────╯
     └─────────────────────────────────
      KB   v1   v2   v3   v4  v5  수렴
```

**Pass 6 예상: +40~60개 → 수렴 직전**

---

*2026-02-05 v6 Pass 5 — 증가율 9%, 수렴 임박*
