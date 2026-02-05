# 🔬 재귀 깊이 5단계 분석

> SQLi를 시드로 Level 5까지 추적
> 각 레벨에서 "보안 관련 분기"와 "일반 CS 분기"를 분리

---

## 트리 시각화 (SQLi → 5단계)

```
L0: SQL Injection
│
├─ L1: SQL 언어 ✅
│  ├─ L2: SELECT/UNION/INSERT ❌
│  │  ├─ L3: 테이블/컬럼/스키마 ⛔ (일반 DB)
│  │  │  ├─ L4: 데이터 타입 ⛔
│  │  │  └─ L4: 정규화 ⛔
│  │  └─ L3: information_schema ❌ ← 보안 관련!
│  │     ├─ L4: DB별 시스템 테이블 차이 ❌ ← 보안!
│  │     │  └─ L5: MySQL mysql.user 테이블 ❌ ← 보안!
│  │     └─ L4: 메타데이터 추출 기법 ❌ ← 보안!
│  │
│  ├─ L2: DB별 특수 함수 ❌
│  │  ├─ L3: SLEEP/BENCHMARK (MySQL) ❌ ← 보안!
│  │  ├─ L3: WAITFOR DELAY (MSSQL) ❌ ← 보안!
│  │  ├─ L3: pg_sleep (PostgreSQL) ❌ ← 보안!
│  │  └─ L3: xp_cmdshell (MSSQL) ❌ ← 보안! (RCE)
│  │     ├─ L4: OS 명령 실행 ✅ ATK-INJECT-CMD-001
│  │     └─ L4: Stored Procedure 보안 ❌ ← 보안!
│  │        └─ L5: CLR Assembly (MSSQL) ❌ ← 니치
│  │
│  └─ L2: SQL 주석 문법 ❌
│     └─ L3: DB별 주석 차이 (--/# /#!/) ❌ ← 보안!
│        └─ L4: MySQL Conditional Comments ❌ ← WAF 우회!
│           └─ L5: 버전 기반 조건부 실행 ❌ ← 니치
│
├─ L1: RDBMS ✅
│  ├─ L2: MySQL ❌ (인프라)
│  │  ├─ L3: MySQL 권한 시스템 ❌ ← 보안!
│  │  │  ├─ L4: GRANT/REVOKE ⛔ (DB 관리)
│  │  │  └─ L4: FILE 권한 (파일 읽기/쓰기) ❌ ← 보안!
│  │  │     └─ L5: LOAD_FILE / INTO OUTFILE ❌ ← 보안!
│  │  ├─ L3: MySQL 보안 설정 ❌ ← 보안!
│  │  │  ├─ L4: secure_file_priv ❌
│  │  │  └─ L4: local_infile ❌
│  │  └─ L3: MySQL 버전별 차이 ⛔
│  │
│  ├─ L2: PostgreSQL ❌ (인프라)
│  │  ├─ L3: PostgreSQL 확장 (보안) ❌
│  │  │  └─ L4: COPY TO/FROM ❌ ← 보안!
│  │  └─ L3: PostgreSQL Large Objects ❌ ← 보안!
│  │
│  ├─ L2: MSSQL ❌ (인프라)
│  │  ├─ L3: xp_cmdshell ❌ ← 보안! (중복)
│  │  ├─ L3: Linked Server ❌ ← 보안! (피봇)
│  │  │  └─ L4: OPENROWSET ❌ ← 보안!
│  │  └─ L3: SQL Server Agent ❌
│  │
│  └─ L2: Oracle ❌ (인프라)
│     └─ L3: UTL_HTTP / UTL_FILE ❌ ← 보안!
│
├─ L1: HTTP ✅
│  ├─ L2: URL 구조 ❌
│  │  ├─ L3: Query String ❌
│  │  │  ├─ L4: URL Encoding ❌ ← 보안!
│  │  │  │  └─ L5: Double Encoding ❌ ← WAF 우회!
│  │  │  └─ L4: Parameter Pollution ❌ ← 보안!
│  │  │     └─ L5: HPP (HTTP Parameter Pollution) ❌ ← 보안!
│  │  └─ L3: Fragment (hash) ⛔
│  │
│  ├─ L2: HTTP Methods ❌
│  │  ├─ L3: GET vs POST 보안 차이 ❌ ← 보안!
│  │  └─ L3: PUT/DELETE/PATCH ⛔ (REST API)
│  │
│  ├─ L2: HTTP Header 개념 ❌
│  │  ├─ L3: Content-Type / MIME ❌
│  │  │  └─ L4: MIME Sniffing 공격 ❌ ← 보안!
│  │  ├─ L3: User-Agent 조작 ❌ ← 보안! (SQLi 벡터)
│  │  ├─ L3: Referer 헤더 ❌
│  │  └─ L3: Security Headers ✅ DEF-PREVENT-HEADERS-001
│  │
│  └─ L2: HTTP Response ⛔
│     └─ L3: Status Code ⛔
│
├─ L1: Web Application ✅
│  ├─ L2: Form/입력 처리 ❌
│  │  ├─ L3: Client-side Validation ❌ ← 보안! (우회 가능)
│  │  │  └─ L4: Proxy Intercept (Burp) ✅ TOOL-SCAN-BURP-001
│  │  └─ L3: Server-side Validation ❌ ← 보안!
│  │     └─ L4: Whitelist vs Blacklist ❌ ← 보안!
│  │        └─ L5: Regex 기반 필터링 우회 ❌ ← 보안!
│  │
│  ├─ L2: String Concatenation ❌
│  │  ├─ L3: Dynamic Query Building ❌ ← 보안! (근본 원인)
│  │  │  └─ L4: ORM (Object-Relational Mapping) ❌ ← 보안!
│  │  │     └─ L5: ORM Injection ❌ ← 보안!
│  │  └─ L3: Template Engine ❌
│  │     └─ L4: SSTI ✅ ATK-WEB-SSTI-001
│  │
│  ├─ L2: Prepared Statement 개념 ❌
│  │  └─ L3: Bind Variable ⛔ (구현 상세)
│  │
│  └─ L2: Error Handling ❌
│     ├─ L3: Verbose Error Messages ❌ ← 보안! (정보 유출)
│     │  └─ L4: Stack Trace 노출 ❌ ← 보안!
│     │     └─ L5: Framework 버전 노출 ❌ ← 보안!
│     └─ L3: Custom Error Pages ❌ ← 보안 방어
│
├─ L1: WAF ✅
│  ├─ L2: Reverse Proxy ❌
│  │  ├─ L3: Proxy 아키텍처 ⛔
│  │  └─ L3: SSL Termination ❌ ← 보안!
│  │     └─ L4: TLS Offloading ❌
│  │        └─ L5: 복호화된 트래픽 검사 ❌ ← 보안!
│  │
│  ├─ L2: 시그니처 기반 탐지 ❌
│  │  ├─ L3: 정규표현식 (보안) ❌
│  │  │  ├─ L4: ReDoS (Regex DoS) ❌ ← 보안!
│  │  │  └─ L4: WAF Rule Writing ❌ ← 보안!
│  │  │     └─ L5: ModSecurity CRS ❌ ← 보안!
│  │  └─ L3: False Positive / Negative ❌ ← 보안!
│  │
│  ├─ L2: Positive/Negative Security Model ❌
│  │  └─ L3: Learning Mode / Tuning ❌
│  │
│  └─ L2: WAF Bypass 개념 ❌
│     ├─ L3: 인코딩 우회 ❌ ← 보안!
│     ├─ L3: Chunked Transfer ❌ ← 보안!
│     ├─ L3: Case Manipulation ✅ GR-SEC-TEC-00010
│     └─ L3: HTTP/2 Smuggling ❌ ← 보안!
│        ├─ L4: Request Smuggling ❌ ← 보안!
│        │  └─ L5: CL.TE / TE.CL 공격 ❌ ← 보안!
│        └─ L4: H2C Smuggling ❌ ← 보안!
│
├─ L1: Authentication Bypass ✅
│  └─ L2: (잘 커버됨)
│
└─ L1: OWASP Top 10 ❌
   ├─ L2: OWASP Testing Guide ❌ ← 보안!
   │  └─ L3: WSTG (Web Security Testing Guide) ❌
   │     └─ L4: 테스트 방법론 ❌
   │        └─ L5: Checklist 기반 접근 ⛔
   ├─ L2: OWASP ASVS ❌ ← 보안!
   │  └─ L3: Verification Levels ❌
   └─ L2: OWASP SAMM ❌ ← 보안!
```

---

## 📊 레벨별 통계 (SQLi 기준)

| 레벨 | 전체 노드 | 보안 관련 | 일반 CS | 보안 비율 |
|------|-----------|-----------|---------|-----------|
| L0 | 1 | 1 | 0 | 100% |
| L1 | ~15 | ~15 | 0 | 100% |
| L2 | ~50 | ~45 | ~5 | 90% |
| L3 | ~120 | ~85 | ~35 | 71% |
| L4 | ~250 | ~130 | ~120 | 52% |
| L5 | ~400 | ~150 | ~250 | 38% |
| **합계** | **~836** | **~426** | **~410** | **51%** |

---

## 🔥 Level 3-5에서 발견된 고가치 보안 개념

### 이전 분석(L2까지)에서 놓친 것들

#### ★★★ 필수급 (Level 3)
| # | 개념 | 깊이 | 발견 경로 |
|---|------|------|-----------|
| 1 | **xp_cmdshell** | L3 | SQLi→MSSQL→xp_cmdshell |
| 2 | **Linked Server 피봇** | L3 | SQLi→MSSQL→Linked Server |
| 3 | **information_schema 상세** | L3 | SQLi→SQL→info_schema |
| 4 | **Client vs Server Validation** | L3 | SQLi→WebApp→Validation |
| 5 | **Verbose Error / Stack Trace** | L3 | SQLi→WebApp→Error Handling |
| 6 | **Dynamic Query Building** | L3 | SQLi→WebApp→String Concat |
| 7 | **False Positive/Negative** | L3 | SQLi→WAF→Signature |
| 8 | **HTTP/2 Request Smuggling** | L3 | SQLi→WAF→Bypass |
| 9 | **SSL Termination** | L3 | SQLi→WAF→Reverse Proxy |
| 10 | **OWASP Testing Guide (WSTG)** | L3 | SQLi→OWASP→Testing |
| 11 | **OWASP ASVS** | L3 | SQLi→OWASP→Verification |

#### ★★☆ 권장급 (Level 4)
| # | 개념 | 깊이 | 발견 경로 |
|---|------|------|-----------|
| 12 | **LOAD_FILE / INTO OUTFILE** | L4 | SQLi→MySQL→FILE 권한 |
| 13 | **Parameter Pollution (HPP)** | L4 | SQLi→HTTP→URL→Query |
| 14 | **MIME Sniffing** | L4 | SQLi→HTTP→Header→Content-Type |
| 15 | **ReDoS** | L4 | SQLi→WAF→Regex→ReDoS |
| 16 | **ORM Injection** | L4 | SQLi→WebApp→Dynamic Query→ORM |
| 17 | **Request Smuggling (CL.TE)** | L4 | SQLi→WAF→HTTP/2→Smuggling |
| 18 | **DB 시스템 테이블 차이** | L4 | SQLi→SQL→info_schema→DB별 |
| 19 | **WAF Rule Writing** | L4 | SQLi→WAF→Regex→Rule |
| 20 | **Stack Trace 정보 유출** | L4 | SQLi→Error→Verbose→Stack |

#### ★☆☆ 니치/전문가급 (Level 5)
| # | 개념 | 깊이 | 발견 경로 |
|---|------|------|-----------|
| 21 | **MySQL mysql.user 테이블** | L5 | SQLi→info_schema→시스템테이블→mysql.user |
| 22 | **Double Encoding 우회** | L5 | SQLi→HTTP→URL→Encoding→Double |
| 23 | **HPP 공격** | L5 | SQLi→HTTP→URL→Param→HPP |
| 24 | **ORM Injection 상세** | L5 | SQLi→WebApp→Query→ORM→Injection |
| 25 | **ModSecurity CRS** | L5 | SQLi→WAF→Regex→Rule→CRS |
| 26 | **CL.TE / TE.CL** | L5 | SQLi→WAF→HTTP/2→Smuggling→CL.TE |
| 27 | **CLR Assembly (MSSQL)** | L5 | SQLi→MSSQL→xp_cmdshell→StoredProc→CLR |
| 28 | **MySQL Conditional Comments** | L5 | SQLi→SQL→주석→DB별→Conditional |
| 29 | **Regex 기반 필터 우회** | L5 | SQLi→WebApp→Validation→WL/BL→Regex |
| 30 | **Framework 버전 노출** | L5 | SQLi→Error→Verbose→Stack→Version |

---

## 📈 깊이별 가치 분석

```
가치(보안 관련성)
│
│ ████████████████████  L1 (100% 보안)
│ ██████████████████    L2 (90% 보안)
│ ██████████████        L3 (71% 보안) ← 여전히 가치 높음!
│ ██████████            L4 (52% 보안) ← 절반은 가치 있음
│ ██████                L5 (38% 보안) ← 니치하지만 가치 있는 것 존재
│ ███                   L6+ (예상 <20%) ← 여기서 멈춰야
└─────────────────────────────────
```

---

## 🎯 결론: 깊이 2 vs 5

| 지표 | Depth 2 | Depth 5 |
|------|---------|---------|
| 발견 노드 수 (SQLi) | ~50 | ~426 (보안만) |
| 필수급 (★★★) | ~13 | ~35 |
| 권장급 (★★☆) | ~19 | ~80 |
| 니치급 (★☆☆) | ~18 | ~311 |
| 일반 CS 혼입 | 거의 없음 | ~410개 (필터 필요) |
| 작업 난이도 | 쉬움 | 필터링이 핵심 |

### 깊이 5의 장점
1. **L3에서 고가치 보안 개념 발견** — xp_cmdshell, Request Smuggling, OWASP WSTG 등
2. **L4에서 실전 공격 기법 발견** — ReDoS, ORM Injection, HPP, MIME Sniffing
3. **L5에서 전문가급 세부 발견** — CL.TE, CLR Assembly, MySQL Conditional Comments

### 깊이 5의 위험
1. **노이즈 폭발** — 보안 비율이 L5에서 38%로 하락
2. **경계 판정 어려움** — "MySQL Conditional Comments"가 독립 원자가 되어야 하는가?
3. **작업량** — 10개 시드 × 400개 = 4,000개 노드 (필터링 필요)

### 🏆 권장: **깊이 3 + 선별적 4-5**

| 접근법 | 설명 |
|--------|------|
| **L1-L2**: 전수 조사 | 모든 누락 원자화 |
| **L3**: 보안 필터 후 전수 | "보안 독립 설명 필요?" 기준 적용 |
| **L4-L5**: 선별적 | 고가치 항목만 (ReDoS, HPP, Request Smuggling 등) |

이렇게 하면:
- Depth 2의 ~120개 → **Depth 3+선별로 ~200-250개** 수준
- 관리 가능하면서도 전문성 높은 KB 확보

---

*2026-02-05 — 깊이 5단계 분석 (시드: SQLi)*
