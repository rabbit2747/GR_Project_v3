# 누락 개념 로우 데이터 v7 (Pass 6)

> v6의 ~126개 항목을 재분해
> 이미 ~1,720 + KB 560 에 없는 것만 추출
> 수렴 직전 — 깊은 니치/교차 도메인 중심
> 생성일: 2026-02-05

---

## Pass 6: v6 항목 재분해에서 나온 신규 개념

### [P6-01] 암호/통신 극극한
- Signal Double Ratchet (상세 — X3DH Key Agreement)
- Noise Protocol Handshake Patterns (NN, NK, XX)
- Kyber (Post-Quantum KEM — NIST 표준)
- Dilithium (Post-Quantum Signature — NIST 표준)
- SPHINCS+ (Post-Quantum Hash-Based Signature)
- Hybrid TLS (Classic + PQC)
- KEMTLS
- Certificate-less Authentication
- Threshold Cryptography
- Multi-Signature (Crypto)

### [P6-02] AD 극극한 / 방어 관점
- Tiered Administration Model (상세 — Tier 0/1/2 자산)
- Authentication Policy Silo (Windows Server 2012 R2+)
- Privileged Access Workstation (PAW)
- Just-In-Time Administration (AD)
- Credential Tiering
- AD Backup/Recovery Security
- DIT (Directory Information Tree) Extraction Prevention
- LDAP Firewall
- AD Certificate Enrollment Agent
- ADCS Auditing (Event 4886, 4887)

### [P6-03] 프로토콜 / 네트워크 방어
- RPKI ROA (Route Origin Authorization)
- RPKI ROV (Route Origin Validation)
- BGP ASPA (Autonomous System Provider Authorization)
- MANRS (Mutually Agreed Norms for Routing Security)
- BCP38 / BCP84 (Anti-Spoofing)
- Source Address Validation (SAV/uRPF)
- TCP-AO (TCP Authentication Option)
- MACsec (802.1AE)
- Encrypted DNS Bootstrapping
- DNS Firewall (RPZ — Response Policy Zone)

### [P6-04] 웹 / API 방어 극한
- Security.txt (RFC 9116)
- robots.txt Security (정보유출)
- .well-known URIs (보안 관점)
- API Discovery (보안 — Shadow API)
- API Posture Management
- GraphQL Persisted Queries (보안)
- Rate Limiting Algorithms (상세 — Fixed Window, Sliding Window, Token Bucket, Leaky Bucket)
- Bot Management (Advanced — Headless Browser Detection)
- Device Fingerprinting (보안)
- Client-Side Security Monitoring (CSP Report, NEL)
- Reporting API (Network Error Logging)

### [P6-05] 맬웨어 분석 방어 관점
- PE Section Analysis (.text, .data, .rdata — 보안)
- Import Table Reconstruction
- String Analysis (FLOSS)
- Behavioral Analysis Sandbox (Cuckoo, CAPE, Joe)
- Dynamic Analysis Evasion Indicators
- Code Similarity (ssdeep, TLSH, imphash)
- Malware Family Classification
- Threat Actor Profiling
- Campaign Infrastructure Analysis (Passive DNS, pDNS)
- Diamond Model — Infrastructure Pivot
- MITRE ATT&CK Software Mapping

### [P6-06] 법규/표준 교차 (한국 특화)
- 주요정보통신기반시설 보호 (한국)
- 정보보호 공시제도 (한국)
- 클라우드 보안인증 (CSAP — 한국)
- 소프트웨어 공급망 보안 가이드 (한국 KISA)
- 금융분야 클라우드 이용 가이드 (한국 금감원)
- 개인정보 영향평가 (PIA — 한국)
- 개인정보 처리방침 (한국 필수 공시)
- 개인정보보호 책임자 (CPO vs DPO)
- 망분리 / 망연계 (한국 특유)
- 보안관제 (한국 SOC — 특수성)

### [P6-07] 클라우드/인프라 방어 극한
- Cloud Workload Fingerprinting
- Cloud Instance Metadata Hardening
- AWS Nitro Enclave
- Azure Confidential Computing
- GCP Confidential VMs
- Cloud Key Management (BYOK, HYOK, Hold Your Own Key)
- Customer Managed Key (CMK) vs Provider Managed
- Cloud HSM (CloudHSM, Azure Dedicated HSM)
- FinOps (비용 최적화 — 보안 관점)
- Cloud Governance Framework

### [P6-08] DevSecOps/공급망 방어 극한
- SLSA Provenance Verification
- Rekor Transparency Log
- Fulcio Keyless Signing
- Cosign Verification
- SBOM Enrichment (VEX + SBOM)
- Dependency Resolution Attack
- Manifest Confusion Attack (npm)
- RepoJacking (GitHub)
- Typosquatting Detection (Automated)
- Lockfile Injection

### [P6-09] SOC/탐지 극극한
- Detection Maturity Model
- DeTT&CT (Detection, Techniques & Controls)
- VECTR (Purple Team Tracking)
- Sigma Correlation Rules
- Sigma Pipelines (Backend Conversion)
- Chronicle YARA-L Rule Lifecycle
- Splunk Risk-Based Alerting (RBA)
- MITRE ATT&CK Evaluation (Vendor Comparison)
- Threat Intelligence Sharing (STIX/TAXII 상세 — STIX Bundle, Indicator, Relationship)
- OpenCTI / MISP Integration

### [P6-10] 교차 도메인 / 신흥 위협
- Deepfake Audio Detection (Watermark, Spectral)
- Synthetic Media Policy
- AI Governance Framework (NIST AI RMF)
- Autonomous Weapon System (보안 관점)
- Drone Security / Counter-UAS
- 5G Security Architecture (SBA, SEPP)
- Open RAN Security
- Edge Computing Security
- Digital Sovereignty
- Cyber-Physical System (CPS) Security

---

## Pass 6 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P6-01: 암호 극한 | 10 |
| P6-02: AD 방어 극한 | 10 |
| P6-03: 네트워크 방어 | 10 |
| P6-04: 웹/API 방어 | 11 |
| P6-05: 맬웨어 분석 | 11 |
| P6-06: 한국 법규/표준 | 10 |
| P6-07: 클라우드 방어 | 10 |
| P6-08: DevSecOps 방어 | 10 |
| P6-09: SOC/탐지 | 10 |
| P6-10: 신흥 위협 | 10 |
| **Pass 6 합계** | **~102** |

---

## 전체 누적 통계 (최종)

| Pass | 신규 | 누적 (원시) | 증가율 |
|------|------|-------------|--------|
| v1 | 323 | 323 | — |
| v2 | 349 | 672 | +108% |
| v3 | 349 | 1,021 | +52% |
| v4 | 217 | 1,238 | +21% |
| v5 | 147 | 1,385 | +12% |
| v6 | 126 | 1,511 | +9% |
| **v7 (Pass 6)** | **102** | **1,613** | **+7%** |

| 측정 | 값 |
|------|-----|
| 원시 합계 | 1,613 |
| 기존 KB | 560 |
| 전체 | 2,173 |
| 중복 예상 | ~380 |
| **예상 고유 전체** | **~1,793** |

```
증가율 추이
108% │████████████████████████████
 52% │██████████████
 21% │██████
 12% │███
  9% │██
  7% │██          ← Pass 6 (지금)
 ~3% │█           ← Pass 7 예상
 ~1% │            ← Pass 8 (수렴)
     └────────────────────────
      v2  v3  v4  v5  v6  v7  v8
```

```
고유 개념 수
1800 │                                      ╌╌ 수렴 (~1,800)
1793 │                                ╭─────── ← 지금 여기
1720 │                           ╭────╯
1635 │                      ╭────╯
1550 │                 ╭────╯
1400 │            ╭────╯
1100 │      ╭─────╯
 560 │──────╯
     └────────────────────────────────────
      KB  v1  v2  v3  v4  v5  v6  수렴
```

**수렴점 수정: ~1,800 (±50)**
**Pass 7: +30~50개 예상 → 사실상 수렴**

---

*2026-02-05 v7 Pass 6 — 증가율 7%, 한국 법규/표준 추가, 수렴 직전*
