# 🧪 파일럿 테스트: SQLi 재귀적 개념 분해

> **목적**: SQL Injection을 완전히 설명하려면 어떤 개념들이 필요한가?
> 현재 KB에 있는 것 ✅ / 없는 것 ❌ / 경계선 🔶 / 범위 밖 ⛔

---

## 시드: SQL Injection

**현재 KB 원자** (이미 존재):
- `ATK-INJECT-SQL-001` — SQL Injection (attack/technique)
- `VUL-WEB-SQLI-001` — SQL Injection (vulnerability)
- `VUL-INJECT-SQL-001` — SQL Injection Vulnerability (중복?)
- `GR-SEC-CON-00002` — SQL 인젝션 (concept)
- `ATK-INJECTION-001` — Injection Attack (상위 개념)
- `VUL-INJECTION-001` — Injection Vulnerability (상위 개념)
- `GR-SEC-CON-00001` — 인젝션 취약점 (상위 개념)

**SQLi 하위 기법** (이미 존재):
- `GR-SEC-TEC-00001` — UNION-based SQLi
- `GR-SEC-TEC-00002` — Blind Boolean-based SQLi
- `GR-SEC-TEC-00003` — Blind Time-based SQLi
- `GR-SEC-TEC-00004` — Error-based SQLi
- `GR-SEC-TEC-00005` — Stacked Queries SQLi
- `GR-SEC-TEC-00006` — Out-of-Band SQLi
- `GR-SEC-TEC-00007` — Second-Order SQLi
- `GR-SEC-TEC-00008` — Comment-based WAF Bypass
- `GR-SEC-TEC-00009` — Encoding-based WAF Bypass
- `GR-SEC-TEC-00010` — Case/Whitespace Manipulation Bypass

**SQLi 페이로드/핑거프린트** (이미 존재):
- `GR-SEC-INS-P0001` — Single Quote Error Payload
- `GR-SEC-INS-P0002` — Boolean True/False Detection
- `GR-SEC-INS-P0003` — Time-based SLEEP Detection
- `GR-SEC-INS-P0004` — UNION Column Count Detection
- `GR-SEC-INS-P0005` — UNION Data Extraction
- `GR-SEC-INS-F0001` — MySQL DBMS Fingerprint
- `GR-SEC-INS-F0002` — MSSQL DBMS Fingerprint
- `GR-SEC-INS-F0003` — PostgreSQL DBMS Fingerprint

---

## Level 1: SQLi를 설명하려면 필요한 개념

### A. 공격 대상 (WHERE)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| Web Application | ✅ | `INFRA-APP-WEBAPP-001` |
| REST API Server | ✅ | `INFRA-APP-API-001` |
| Web Server | ✅ | `INFRA-APP-WEBSERVER-001` |
| RDBMS (관계형 DB) | ✅ | `INFRA-DATA-RDBMS-001` |
| MySQL | ❌ | `GR-SEC-CMP-00010` (TODO 참조만) |
| PostgreSQL | ❌ | `GR-SEC-CMP-00011` (TODO 참조만) |
| MSSQL | ❌ | `GR-SEC-CMP-00012` (TODO 참조만) |
| Oracle DB | ❌ | `GR-SEC-CMP-00013` (TODO 참조만) |
| NoSQL DB (MongoDB 등) | 🔶 | 공격은 있음 `ATK-WEB-SQLI-NOSQL-001`, 인프라 원자 없음 |

### B. 전제 기술 지식 (WHAT)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| SQL 언어 | ✅ | `TECH-LANG-SQL-001` |
| HTTP 프로토콜 | ✅ | `TECH-PROTOCOL-HTTP-001` |
| HTML | ✅ | `TECH-LANG-HTML-001` |
| Cookie | ✅ | `TECH-CONCEPT-COOKIE-001` |
| Web Session | ✅ | `TECH-CONCEPT-SESSION-001` |
| URL/쿼리 파라미터 | ❌ | URL 구조, GET/POST 파라미터 |
| HTTP Header (개념) | ❌ | 공격은 있음 `ATK-INJECT-HEADER-001`, 개념 원자 없음 |
| HTTP Methods (GET/POST) | ❌ | |
| Form/입력 필드 | ❌ | 사용자 입력 처리 메커니즘 |
| String Concatenation | ❌ | SQLi 근본 원인 (문자열 결합) |
| SQL SELECT/UNION/INSERT | ❌ | SQL 세부 구문 (TECH-LANG-SQL-001에 포함?) |
| Prepared Statement | ❌ | 개념 원자 없음 (DEF-PREVENT-PARAMQUERY-001은 방어책) |
| Stored Procedure | ❌ | |
| 정규표현식 (Regex) | ❌ | WAF 룰 설명에 필요 |
| 인코딩 (URL/Base64/Hex) | ❌ | WAF 우회 설명에 필요 |
| 에러 메시지/Stack Trace | ❌ | `GR-SEC-CON-00022` (TODO 참조만) |

### C. 방어 수단 (HOW TO DEFEND)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| Input Validation | ✅ | `DEF-PREVENT-INPUTVAL-001` |
| Parameterized Query | ✅ | `DEF-PREVENT-PARAMQUERY-001` |
| WAF (인프라) | ✅ | `INFRA-NET-WAF-001` |
| WAF (방어) | ✅ | `DEF-WAF-001` |
| WAF Rules | ✅ | `DEF-PREVENT-WAF-RULES-001` |
| Output Encoding | ✅ | `DEF-PREVENT-OUTPUTENC-001` |
| Least Privilege (DB 계정) | ✅ | `GR-SEC-PRI-LEAST-PRIVILEGE-001` |
| Whitelist vs Blacklist | ❌ | 입력 검증 전략 비교 |
| Escaping (이스케이핑) | ❌ | 문자열 이스케이프 처리 |
| DB 권한 관리 | ❌ | DB 사용자 권한 세분화 |

### D. 공격 결과/영향 (IMPACT)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| Data Exposure | ✅ | `VUL-DATA-EXPOSURE-001` |
| Authentication Bypass | ✅ | `ATK-AUTH-BYPASS-001` |
| 데이터 유출 | ❌ | `GR-SEC-CON-00010` (TODO 참조만) |
| 인증 우회 | ❌ | `GR-SEC-CON-00011` (TODO 참조만) |
| 시스템 장악 | ❌ | `GR-SEC-CON-00012` (TODO 참조만) |
| 권한 상승 | ✅ | `ATK-PRIVILEGE-ESCALATION-001` |
| OS 명령 실행 | ✅ | `ATK-INJECT-CMD-001` |

### E. 분류/참조 체계 (CONTEXT)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| MITRE ATT&CK | ✅ | `TECH-CONCEPT-MITRE-ATTACK-001` |
| OWASP Top 10 | ❌ | **참조만 다수, 전용 원자 없음** |
| CWE (Common Weakness Enumeration) | ❌ | **참조만 다수, 전용 원자 없음** |
| CVSS (점수 체계) | ❌ | 속성으로만 사용, 개념 원자 없음 |
| CVE (Common Vulnerabilities) | ❌ | |
| NVD (National Vulnerability DB) | ❌ | |

### F. 테스트 도구 (TOOLS)
| 개념 | KB 상태 | Atom ID |
|------|---------|---------|
| SQLMap | ✅ | `TOOL-PENTEST-SQLMAP-001` / `TOOL-OFFENSE-SQLMAP-001` |
| Burp Suite | ✅ | `TOOL-SCAN-BURP-001` / `TOOL-PENTEST-BURPSUITE-001` |
| OWASP ZAP | ✅ | `TOOL-SCAN-OWASP-ZAP-001` |
| ModSecurity | ✅ | `TOOL-DEFENSE-MODSEC-001` |
| Havij | ❌ | (구식이라 없어도 됨?) |

---

## Level 2: Level 1의 누락 개념을 설명하려면?

### MySQL을 설명하려면 → (Level 2 분해)
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| RDBMS | ✅ | `INFRA-DATA-RDBMS-001` |
| SQL | ✅ | `TECH-LANG-SQL-001` |
| 테이블/스키마/인덱스 | ⛔ | 일반 DB 기초 → 범위 밖 |
| information_schema | ❌ | SQLi에서 핵심 (DB 구조 탐색) |
| MySQL 특수 함수 (SLEEP, BENCHMARK) | ❌ | Time-based SQLi에 필수 |
| MySQL 주석 문법 (-- , #, /**/) | ❌ | WAF bypass에 필수 |

### OWASP Top 10을 설명하려면 → (Level 2 분해)
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| OWASP 재단 | ⛔ | 조직 자체는 범위 밖 |
| 웹 취약점 분류 체계 | ❌ | Top 10 카테고리 |
| 보안 프레임워크 (일반) | ✅ | `COMP-FRAMEWORK-001` |

### CWE를 설명하려면 → (Level 2 분해)
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| 취약점 분류 체계 | ❌ | 약점(weakness) 열거 시스템 |
| MITRE (조직) | ⛔ | 조직 자체는 범위 밖 |
| CWE-89 (SQLi) | 🔶 | 속성으로만 참조됨 |

### WAF를 설명하려면 → (Level 2 분해)
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Firewall | ✅ | `INFRA-NET-FIREWALL-001` / `TECH-CONCEPT-FIREWALL-001` |
| HTTP 프로토콜 | ✅ | `TECH-PROTOCOL-HTTP-001` |
| 프록시/리버스 프록시 | ❌ | WAF 배치 구조 설명에 필수 |
| 시그니처 기반 탐지 | ❌ | 탐지 방식 |
| 정규표현식 | ❌ | 룰 작성 기반 기술 |
| ModSecurity CRS | ❌ | 대표적 룰셋 (도구는 있으나 룰셋 개념 없음) |
| Positive/Negative Security Model | ❌ | WAF 운영 모델 |

### 인코딩을 설명하려면 → (Level 2 분해)
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| URL Encoding (%xx) | ❌ | 웹 보안 기초 |
| Base64 | ❌ | |
| Hex Encoding | ❌ | |
| Double Encoding | ❌ | WAF 우회 |
| Unicode/UTF-8 | ⛔ | 일반 CS → 범위 밖 |

---

## Level 3: 여기서 멈춤 (경계선)

Level 2까지가 **보안 맥락에서 의미 있는 깊이**입니다.
Level 3부터는 일반 CS/IT 기초로 진입합니다:
- TCP/IP의 세부 → ⛔
- 데이터베이스 정규화 → ⛔
- 프로그래밍 언어 문법 → ⛔
- 바이너리/메모리 → ⛔

---

## 📊 누락 원자 요약 (GAP LIST)

### 🔴 반드시 필요 (보안 고유 개념, Level 1)
| # | 개념 | 유형 | 우선순위 |
|---|------|------|----------|
| 1 | **OWASP Top 10** | concept/framework | ★★★ |
| 2 | **CWE (Common Weakness Enumeration)** | concept/framework | ★★★ |
| 3 | **CVSS (Common Vulnerability Scoring System)** | concept/framework | ★★★ |
| 4 | **CVE (Common Vulnerabilities and Exposures)** | concept/framework | ★★★ |
| 5 | **MySQL** (인프라 컴포넌트) | component | ★★★ |
| 6 | **PostgreSQL** (인프라 컴포넌트) | component | ★★★ |
| 7 | **MSSQL** (인프라 컴포넌트) | component | ★★★ |
| 8 | **Oracle DB** (인프라 컴포넌트) | component | ★★★ |
| 9 | **information_schema** | concept | ★★★ |
| 10 | **DB별 특수 함수** (SLEEP, BENCHMARK 등) | concept | ★★☆ |
| 11 | **SQL 주석 문법** (DB별 차이) | concept | ★★☆ |
| 12 | **Whitelist vs Blacklist 필터링** | concept | ★★☆ |
| 13 | **Escaping (이스케이핑)** | concept/defense | ★★☆ |

### 🟡 있으면 좋음 (보안 맥락의 IT 개념, Level 1-2)
| # | 개념 | 유형 | 우선순위 |
|---|------|------|----------|
| 14 | **URL 구조/쿼리 파라미터** | concept | ★★☆ |
| 15 | **HTTP Methods (GET/POST)** | concept | ★★☆ |
| 16 | **HTTP Header (개념)** | concept | ★★☆ |
| 17 | **Form/사용자 입력 처리** | concept | ★★☆ |
| 18 | **String Concatenation (보안 관점)** | concept/principle | ★★☆ |
| 19 | **Prepared Statement (개념)** | concept | ★★☆ |
| 20 | **Stored Procedure** | concept | ★☆☆ |
| 21 | **Reverse Proxy** | component/concept | ★★☆ |
| 22 | **시그니처 기반 탐지** | concept | ★★☆ |
| 23 | **정규표현식 (보안 관점)** | concept | ★☆☆ |
| 24 | **URL Encoding** | concept | ★★☆ |
| 25 | **Base64 Encoding** | concept | ★☆☆ |
| 26 | **Double Encoding** | concept | ★★☆ |
| 27 | **Positive/Negative Security Model** | concept | ★☆☆ |
| 28 | **NVD (National Vulnerability Database)** | concept/framework | ★☆☆ |
| 29 | **NoSQL DB** (인프라: MongoDB 등) | component | ★★☆ |
| 30 | **DB 권한 관리** | concept/defense | ★★☆ |
| 31 | **Error Message/Stack Trace (보안)** | concept | ★★☆ |
| 32 | **ModSecurity CRS** | concept | ★☆☆ |

### 🔵 이미 TODO로 참조됨 (GR-SEC-* 원자 내 미생성 참조)
| # | TODO ID | 개념 | 비고 |
|---|---------|------|------|
| T1 | `GR-SEC-CON-00003` | WAF Bypass Technique | 3개 원자에서 참조 |
| T2 | `GR-SEC-CON-00010` | 데이터 유출 | 2개 원자에서 참조 |
| T3 | `GR-SEC-CON-00011` | 인증 우회 | 2개 원자에서 참조 |
| T4 | `GR-SEC-CON-00012` | 시스템 장악 | 1개 원자에서 참조 |
| T5 | `GR-SEC-CON-00020` | Query Result Display | UNION SQLi 전제조건 |
| T6 | `GR-SEC-CON-00021` | Observable Response Difference | Blind SQLi 전제조건 |
| T7 | `GR-SEC-CON-00022` | Verbose Error Messages | Error SQLi 전제조건 |
| T8 | `GR-SEC-CON-00023` | Multi-Statement Support | Stacked Queries 전제조건 |
| T9 | `GR-SEC-CON-00024` | Outbound Network Access | OOB SQLi 전제조건 |
| T10 | `GR-SEC-CON-00025` | Data Storage Capability | 2nd Order SQLi 전제조건 |
| T11 | `GR-SEC-CON-00026` | Unsafe Data Retrieval | 2nd Order SQLi 전제조건 |
| T12 | `GR-SEC-CTL-00010` | WAF UNION/Keyword Filter | 4개 원자에서 참조 |
| T13 | `GR-SEC-CTL-00011` | Parameterized Queries (control) | 1개 원자에서 참조 |
| T14 | `GR-SEC-CMP-00001` | SQL 데이터베이스 | = MySQL/PG/MSSQL 상위 |
| T15 | `GR-SEC-CMP-00002` | 사용자 입력 처리 | |
| T16 | `GR-SEC-CMP-00010~13` | MySQL/PG/MSSQL/Oracle | 4개 DB 컴포넌트 |
| T17 | `GR-SEC-TEC-00050` | 권한 상승 (via SQLi) | |
| T18 | `GR-SEC-TEC-00051` | OS 명령 실행 (via SQLi) | |

---

## 📈 통계

| 카테고리 | 수량 |
|----------|------|
| 현재 KB에 있는 SQLi 관련 원자 | **29개** |
| Level 1 누락 (반드시 필요) | **13개** |
| Level 1-2 누락 (있으면 좋음) | **19개** |
| TODO로 참조만 되는 미생성 원자 | **18개** (중복 제거) |
| **총 누락 추정** | **~50개** |
| 재귀 깊이 | **Level 2에서 중단** |
| 범위 밖 제외 (⛔) | ~15개 개념 |

---

## 🎯 파일럿 결론

1. **SQLi 하나에서 ~50개의 누락 원자 발견** — 이 중 13개는 필수급
2. **재귀 깊이 2단계면 충분** — Level 3부터는 일반 CS 영역
3. **경계선 판정 기준이 작동함**: "보안에서 이 개념이 독립적으로 설명되어야 하는가?"
4. **TODO 참조 정리**도 동시에 가능 — 이미 18개의 "약속된 원자"가 미생성

### 위험 평가
- ❌ 폭발 위험: **낮음** (Level 2에서 자연스럽게 수렴)
- ⚠️ 작업량: SQLi 하나에 50개면, 전체 KB에선 **수백~천 개 수준**
  - 단, 개념 공유 효과로 실제는 더 적을 것 (WAF, HTTP 등은 여러 공격이 공유)
- ✅ 가치: **매우 높음** — KB 완성도를 체계적으로 올리는 유일한 방법

---

*2026-02-05 생성 — 파일럿 테스트 (시드: SQL Injection)*
