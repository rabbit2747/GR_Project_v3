# MVP DAST SQLi Project

> AI-Driven Adaptive DAST for SQL Injection Detection
> GR Framework 기반 MVP 프로젝트

---

## 프로젝트 개요

기존의 룰셋 기반 자동화 진단툴이 아닌, **AI가 사람처럼 판단하고 적응하는** DAST(Dynamic Application Security Testing) 도구 개발

### 핵심 철학

```
기존 DAST:  Payload DB → 전부 발사 → 결과 매칭 (Brute Force)
AI DAST:    정찰 → 판단 → 시도 → 적응 (Adaptive Intelligence)
```

### 2-Layer 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                 Layer 2: AI Intelligence                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   Recon Agent │ Strategy Agent │ Injection │ Adapt     │   │
│  │   "이 지식을 바탕으로 상황에 맞게 판단"                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ▲                                   │
│                              │ 참조/학습                         │
├──────────────────────────────┼──────────────────────────────────┤
│                 Layer 1: Knowledge Foundation                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Payload DB │ Bypass DB │ DBMS DB │ Context DB │ Case DB│   │
│  │  "사람이 알고 있는 모든 SQLi 지식의 원자화"             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 폴더 구조

```
MVP_DAST_SQLi/
│
├── README.md                          # 이 파일
│
├── 00_Foundation/                     # 기초 지식 문서
│   ├── 01_SQLi_Complete_Guide.md     # SQLi 완전 정복 (본질+ORM+DAST탐지)
│   ├── 02_Bypass_Techniques.md       # 필터/WAF 우회 기법
│   ├── 03_DBMS_MySQL.md              # MySQL 상세
│   ├── 04_DBMS_PostgreSQL.md         # PostgreSQL 상세
│   ├── 05_DBMS_MSSQL.md              # MSSQL 상세
│   ├── 06_NoSQL_Injection.md         # NoSQL 인젝션 (MongoDB, Redis 등)
│   ├── 07_Advanced_Exploitation.md   # Post-SQLi 고급 공격
│   └── 08_Lateral_Movement.md        # DB Link & 내부 이동
│
├── 01_Knowledge_Base/                 # AI 학습용 Knowledge DB (예정)
│   ├── payloads/                     # Base Payloads
│   ├── bypasses/                     # Bypass Techniques
│   ├── dbms/                         # DBMS Specifics
│   ├── contexts/                     # Injection Contexts
│   ├── fingerprints/                 # Tech Fingerprinting
│   ├── filters/                      # Filter/WAF Signatures
│   └── cases/                        # Success/Failure Cases
│
├── 02_AI_Agents/                      # AI Agent 구현 (예정)
│   ├── recon_agent.py               # 정찰 Agent
│   ├── strategy_agent.py            # 전략 Agent
│   ├── injection_agent.py           # 주입 Agent
│   └── adapt_agent.py               # 적응 Agent
│
├── 03_Core_Engine/                    # 핵심 엔진 (예정)
│   ├── crawler.py                   # HTTP Crawler
│   ├── injector.py                  # Payload Injector
│   └── analyzer.py                  # Response Analyzer
│
└── 04_Tests/                          # 테스트 (예정)
    └── test_targets/                 # 테스트용 취약 앱
```

---

## 개발 로드맵

### Phase 1: Knowledge Foundation (현재)
- [x] SQLi 기초 지식 문서화 (01)
- [x] Bypass 기법 상세 문서화 (02)
- [x] DBMS별 특성 문서화 (03-05: MySQL, PostgreSQL, MSSQL)
- [x] NoSQL Injection 문서화 (06)
- [x] Advanced Exploitation 문서화 (07)
- [x] Lateral Movement 문서화 (08)
- [ ] Knowledge Base YAML 스키마 설계

### Phase 2: Knowledge Base 구축
- [ ] Payload DB 구축
- [ ] Bypass DB 구축
- [ ] Fingerprint DB 구축
- [ ] Case DB 구축

### Phase 3: AI Integration
- [ ] RAG/Vector DB 구축
- [ ] AI Agent 프롬프트 설계
- [ ] Agent 구현

### Phase 4: Engine Development
- [ ] Core Engine 구현
- [ ] Agent 연동
- [ ] MVP 테스트

---

## GR Framework 연동

이 프로젝트는 GR Framework의 분류 체계를 활용합니다:

- **Layer**: L7 (Application) ↔ L5 (Data)
- **Zone**: Zone 3-4 (Web Application Area)
- **Tags**: A-WEB-*, D-DB-*, S-VUL-INJ, T-LANG-SQL

---

## 관련 문서

- `../프로젝트2_GR FrameWork/` - GR Framework 메인 문서
- `../프로젝트2_GR FrameWork/GR_DB/05_Vulnerability_Catalog/` - 취약점 카탈로그

---

> 최종 수정: 2025-01-26
