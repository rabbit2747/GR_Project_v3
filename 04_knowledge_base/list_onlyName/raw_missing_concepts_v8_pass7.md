# 누락 개념 로우 데이터 v8 (Pass 7)

> v7의 ~102개 재분해 — 수렴 단계
> 대부분 이미 다른 개념에 흡수됨. 진짜 신규만 추출.
> 생성일: 2026-02-05

---

## Pass 7: 수렴 단계 — 잔여 신규 개념

### [P7-01] PQC/양자 관련 잔여
- CNSA 2.0 (NSA Commercial National Security Algorithm Suite)
- Harvest Now, Decrypt Later (HNDL) 위협
- Crypto-Agility Assessment Checklist
- PQC Migration Roadmap (단계별)
- Quantum Random Number Generator (QRNG)

### [P7-02] AD/인증 인프라 잔여
- Windows Hello for Business (WHfB)
- Passwordless Authentication Strategy
- FIDO Alliance Certification
- Passkey Syncing (보안 위험)
- Device-Bound Passkey vs Synced Passkey

### [P7-03] 한국 보안 생태계 잔여
- K-ISMS 인증 심사 절차
- 취약점 진단 기준 (KISA 주요정보통신기반시설 가이드)
- CC인증 (Common Criteria — 한국 적용)
- 국정원 보안적합성 검증
- 전자서명법 (한국)
- 공인전자서명 → 공동인증서 전환
- 보안관제 전문업체 지정제도
- 침해사고 신고 의무 (정보통신망법)
- 개인정보보호위원회 (PIPC) 역할
- 한국인터넷진흥원 (KISA) 역할

### [P7-04] 산업별 보안 잔여
- SWIFT CSP (Customer Security Programme)
- PCI PIN Security
- PCI P2PE (Point-to-Point Encryption)
- PCI 3DS (3-D Secure)
- EMV (Chip Card Security)
- ATM Security (Jackpotting, Skimming)
- SCADA Historian (보안)
- HMI (Human Machine Interface) 보안
- Safety vs Security (OT 관점 차이)
- Consequence-Driven Risk Assessment (OT)

### [P7-05] 물리/하드웨어 잔여
- Supply Chain Hardware Tampering
- Counterfeit Component Detection
- Hardware Trojan
- Chip Decapsulation / Microprobing
- Power Analysis Attack (SPA, DPA)
- Electromagnetic Analysis (EMA)
- Fault Injection (Laser, Voltage, Clock)
- Physical Unclonable Function (PUF)

### [P7-06] 프라이버시 기술 잔여
- k-Anonymity
- l-Diversity
- t-Closeness
- Synthetic Data (프라이버시)
- Data Clean Room
- Federated Analytics
- On-Device Processing (Privacy)
- Privacy Sandbox (Google Chrome)
- FLoC → Topics API

### [P7-07] 위협 인텔리전스 잔여
- Threat Actor Classification (APT, FIN, UNC)
- APT Group Naming Conventions (Microsoft/Mandiant/CrowdStrike)
- Cyber Threat Landscape Report (연례)
- Dark Web Monitoring
- Paste Site Monitoring
- Telegram Channel Monitoring (위협)
- Ransomware Negotiation
- Cryptocurrency Tracing (Chainalysis 등)
- Takedown (Domain, C2, Market)

### [P7-08] 보안 아키텍처 잔여
- Defense in Depth Layers (상세 — Perimeter/Network/Host/App/Data)
- Security Architecture Framework (SABSA, TOGAF+Security)
- Threat Model Review Process
- Security Requirements Engineering
- Secure Design Patterns (Compartmentalization, Fail-Safe Defaults)
- Attack Tree Modeling
- Abuse Case / Misuse Case
- Security User Story

---

## Pass 7 통계

| 카테고리 | 항목 수 |
|----------|---------|
| P7-01: PQC/양자 | 5 |
| P7-02: 인증 인프라 | 5 |
| P7-03: 한국 보안 생태계 | 10 |
| P7-04: 산업별 보안 | 10 |
| P7-05: 하드웨어 | 8 |
| P7-06: 프라이버시 기술 | 9 |
| P7-07: 위협 인텔리전스 | 9 |
| P7-08: 보안 아키텍처 | 8 |
| **Pass 7 합계** | **~64** |

---

## 전체 누적 통계 (최종)

| Pass | 신규 | 누적 (원시) | 증가율 |
|------|------|-------------|--------|
| v1 | 323 | 323 | — |
| v2 | +349 | 672 | +108% |
| v3 | +349 | 1,021 | +52% |
| v4 | +217 | 1,238 | +21% |
| v5 | +147 | 1,385 | +12% |
| v6 | +126 | 1,511 | +9% |
| v7 | +102 | 1,613 | +7% |
| **v8 (Pass 7)** | **+64** | **1,677** | **+4%** |

| 측정 | 값 |
|------|-----|
| 원시 합계 | 1,677 |
| 기존 KB | 560 |
| 전체 | 2,237 |
| 중복 예상 | ~400 |
| **예상 고유 전체** | **~1,837** |

```
증가율 추이 — 수렴 확정
108% │████████████████████████████
 52% │██████████████
 21% │██████
 12% │███
  9% │██
  7% │██
  4% │█            ← Pass 7 (지금)
 ~2% │             ← Pass 8 예상 (마지막)
     └────────────────────────
      v2  v3  v4  v5  v6  v7  v8
```

```
고유 개념 수
1850 │                                         ╌ 수렴 (~1,850)
1837 │                                   ╭───── ← 지금 여기
1793 │                              ╭────╯
1720 │                         ╭────╯
1635 │                    ╭────╯
1550 │               ╭────╯
1400 │          ╭────╯
1100 │    ╭─────╯
 560 │────╯
     └───────────────────────────────────────
      KB  v1  v2  v3  v4  v5  v6  v7  수렴
```

**수렴 확정: ~1,850 (±30)**
**Pass 8 하면 +20~30개 → 완전 수렴**

---

*2026-02-05 v8 Pass 7 — 증가율 4%, 수렴 단계 진입*
