# 누락 개념 로우 데이터

> 분류 없음. 순수 "이게 없다"만 나열.
> 소스 A: KB 내부 broken references (203개) — 원자가 참조하는데 실제로 없는 ID
> 소스 B: 재귀 분해로 발견 (L1~L5) — 설명에 필요하지만 참조조차 안 된 개념
> 생성일: 2026-02-05

---

## 소스 A: KB 내부 Broken References (203개)

### ATK-* (34개) — 참조됐지만 없는 공격 원자
- ATK-AUTH-JWTATTACK-001 — JWT 공격
- ATK-AUTH-OAUTH-001 — OAuth 공격
- ATK-AUTH-SAMLATTACK-001 — SAML 공격
- ATK-CONSOLE-001 — 콘솔 공격
- ATK-COVERT-CHANNEL-001 — 은닉 채널
- ATK-DATA-LEAK-001 — 데이터 유출
- ATK-EXEC-RCE-001 — 원격 코드 실행
- ATK-IOT-PROTOCOL-001 — IoT 프로토콜 공격
- ATK-JNDI-001 — JNDI Injection (Log4Shell)
- ATK-MITM-001 — Man-in-the-Middle
- ATK-MITRE-IMPACT-001 — Impact (TA0040)
- ATK-MITRE-INITIAL-ACCESS-001 — Initial Access (중복 ID?)
- ATK-MITRE-TA0001-001 — Initial Access (Tactic ID 형태)
- ATK-MITRE-TA0003-001 — Persistence
- ATK-MITRE-TA0005-001 — Defense Evasion
- ATK-MITRE-TA0007-001 — Discovery
- ATK-MITRE-TA0010-001 — Exfiltration
- ATK-MOBILE-MALWARE-001 — 모바일 맬웨어
- ATK-MOBILE-REVERSING-001 — 모바일 리버싱
- ATK-NETWORK-SNIFF-001 — 네트워크 스니핑 (중복 ID?)
- ATK-PHISHING-SMISHING-001 — 스미싱
- ATK-PHISHING-SPEAR-001 — 스피어 피싱
- ATK-PHISHING-WHALING-001 — 웨일링
- ATK-POST-BACKDOOR-001 — 백도어
- ATK-POST-LATERAL-001 — 측면 이동 (중복 ID?)
- ATK-PRIV-ESCAPE-001 — 권한 탈출 (중복 ID?)
- ATK-RCE-DESER-001 — 역직렬화 RCE (중복 ID?)
- ATK-SUPPLY-TYPOSQUATTING-001 — 타이포스쿼팅 (중복 ID?)
- ATK-WEB-CORS-MISCONFIG-001 — CORS 설정 오류 공격
- ATK-WEB-MIME-SNIFF-001 — MIME 스니핑 공격
- ATK-WEB-PROTOTYPE-POLLUTION-001 — Prototype Pollution (중복 ID?)
- ATK-WIN-SERVICE-ABUSE-001 — Windows 서비스 악용
- ATK-WIN-TOKEN-MANIP-001 — 토큰 조작
- ATK-WIN-UAC-BYPASS-001 — UAC 우회

### COMP-* (14개) — 참조됐지만 없는 컴플라이언스 원자
- COMP-AUDIT-EXTERNAL-001 — 외부 감사
- COMP-AUDIT-INTERNAL-001 — 내부 감사
- COMP-CERTIFICATION-001 — 인증
- COMP-FRAMEWORK-CIS-001 — CIS Benchmark
- COMP-GOV-POLICY-001 — 거버넌스 정책
- COMP-GOV-RISK-001 — 리스크 관리
- COMP-INDUSTRY-HIPAA-001 — HIPAA (중복 ID?)
- COMP-INDUSTRY-PCI-001 — PCI (중복 ID?)
- COMP-INDUSTRY-SOX-001 — SOX
- COMP-PRIVACY-CCPA-001 — CCPA
- COMP-PRIVACY-GDPR-001 — GDPR (중복 ID?)
- COMP-PRIVACY-PIPA-001 — PIPA (개인정보보호법)
- COMP-REGULATION-001 — 규정
- COMP-STANDARD-001 — 표준

### DEF-* (21개) — 참조됐지만 없는 방어 원자
- DEF-ACCESS-CONTROL-001 — 접근 제어
- DEF-ARCHITECTURE-001 — 보안 아키텍처
- DEF-AUTOMATION-001 — 자동화
- DEF-CRYPTO-001 — 암호화 방어
- DEF-DATA-PROTECTION-001 — 데이터 보호
- DEF-DETECTION-001 — 탐지
- DEF-FORENSIC-ANALYSIS-001 — 포렌식 분석
- DEF-HUMAN-001 — 인적 보안
- DEF-OPERATIONS-001 — 보안 운영
- DEF-PREVENT-ARPINSPECT-001 — ARP Inspection
- DEF-PREVENT-AUTHZ-001 — 인가
- DEF-PREVENT-CRYPTO-001 — 암호화 적용
- DEF-PREVENT-DESER-001 — 역직렬화 방어
- DEF-PREVENT-DNSSEC-001 — DNSSEC
- DEF-PREVENT-HARDENING-001 — 하드닝
- DEF-PREVENT-NETWORK-001 — 네트워크 방어
- DEF-PREVENT-NONCE-001 — Nonce
- DEF-PREVENT-PATCH-001 — 패치
- DEF-PREVENT-SESSION-REGEN-001 — 세션 재생성
- DEF-RECOVER-001 — 복구
- DEF-WEB-001 — 웹 방어

### GR-SEC-* (23개) — TODO로 약속된 미생성 원자
- GR-SEC-CMP-00001 — SQL 데이터베이스 (컴포넌트)
- GR-SEC-CMP-00002 — 사용자 입력 처리
- GR-SEC-CMP-00010 — MySQL
- GR-SEC-CMP-00011 — PostgreSQL
- GR-SEC-CMP-00012 — MSSQL
- GR-SEC-CMP-00013 — Oracle
- GR-SEC-COMPLIANCE-001 — 보안 컴플라이언스
- GR-SEC-CON-00003 — WAF Bypass Technique
- GR-SEC-CON-00010 — 데이터 유출
- GR-SEC-CON-00011 — 인증 우회
- GR-SEC-CON-00012 — 시스템 장악
- GR-SEC-CON-00020 — Query Result Display
- GR-SEC-CON-00021 — Observable Response Difference
- GR-SEC-CON-00022 — Verbose Error Messages
- GR-SEC-CON-00023 — Multi-Statement Support
- GR-SEC-CON-00024 — Outbound Network Access
- GR-SEC-CON-00025 — Data Storage Capability
- GR-SEC-CON-00026 — Unsafe Data Retrieval
- GR-SEC-CTL-00010 — WAF UNION/Keyword Filter
- GR-SEC-CTL-00011 — Parameterized Queries (control)
- GR-SEC-INS-P0010 — (미정)
- GR-SEC-TEC-00050 — 권한 상승 (via SQLi)
- GR-SEC-TEC-00051 — OS 명령 실행 (via SQLi)

### INFRA-* (35개) — 참조됐지만 없는 인프라 원자
- INFRA-AD-DC-001 — Domain Controller
- INFRA-AD-FOREST-001 — AD Forest
- INFRA-APP-WAS-001 — WAS (일반)
- INFRA-CDN-001 — CDN (중복 ID?)
- INFRA-CLOUD-COMPUTE-001 — 클라우드 컴퓨트
- INFRA-CONTAINER-001 — 컨테이너 (일반)
- INFRA-DATABASE-001 — 데이터베이스 (일반)
- INFRA-DC-COOLING-001 — DC 냉각
- INFRA-DC-PHYSICAL-001 — DC 물리적
- INFRA-DC-POWER-001 — DC 전원
- INFRA-ENDPOINT-MOBILE-001 — 모바일 엔드포인트
- INFRA-ENDPOINT-WORKSTATION-001 — 워크스테이션
- INFRA-HYBRID-CONNECTIVITY-001 — 하이브리드 연결
- INFRA-HYBRID-MULTICLOUD-001 — 멀티클라우드
- INFRA-IDENTITY-DIRECTORY-001 — 디렉토리 서비스
- INFRA-IDENTITY-IDP-001 — IdP (Identity Provider)
- INFRA-IOT-CONSUMER-001 — 소비자 IoT
- INFRA-IOT-INDUSTRIAL-001 — 산업용 IoT
- INFRA-NET-001 — 네트워크 (일반)
- INFRA-NET-DMZ-001 — DMZ
- INFRA-NET-LAN-001 — LAN
- INFRA-NET-SERVER-001 — 네트워크 서버
- INFRA-NET-WAN-001 — WAN
- INFRA-OT-ICS-001 — ICS
- INFRA-OT-PLC-001 — PLC
- INFRA-OT-SCADA-001 — SCADA
- INFRA-PROTOCOL-001 — 프로토콜 (일반)
- INFRA-SEC-FIREWALL-001 — 보안 방화벽 (중복 ID?)
- INFRA-SEC-IDS-001 — IDS (중복 ID?)
- INFRA-SEC-SIEM-001 — SIEM (중복 ID?)
- INFRA-SERVER-PHYSICAL-001 — 물리 서버
- INFRA-SERVER-VIRTUAL-001 — 가상 서버
- INFRA-STORAGE-NAS-001 — NAS
- INFRA-STORAGE-OBJECT-001 — Object Storage
- INFRA-STORAGE-SAN-001 — SAN

### TECH-* (51개) — 참조됐지만 없는 기술 원자
- TECH-API-GRAPHQL-001 — GraphQL
- TECH-API-GRPC-001 — gRPC
- TECH-API-REST-001 — REST API
- TECH-AUTH-KERBEROS-001 — Kerberos 인증
- TECH-AUTH-OAUTH-001 — OAuth
- TECH-AUTH-SAML-001 — SAML
- TECH-BACKUP-FULL-001 — Full Backup
- TECH-BACKUP-INCREMENTAL-001 — Incremental Backup
- TECH-CI-GITHUB-ACTIONS-001 — GitHub Actions
- TECH-CI-JENKINS-001 — Jenkins
- TECH-CLOUD-001 — 클라우드 (일반)
- TECH-CONCEPT-AUTH-001 — 인증 (개념)
- TECH-CONCEPT-DISCOVERY-001 — 정찰 (개념)
- TECH-CONCEPT-NETWORK-001 — 네트워크 (개념)
- TECH-CONCEPT-RISK-MANAGEMENT-001 — 리스크 관리
- TECH-CONCEPT-SECURITY-001 — 보안 (개념)
- TECH-CONCEPT-SECURITY-ARCHITECTURE-001 — 보안 아키텍처
- TECH-CONCEPT-SECURITY-OPERATIONS-001 — 보안 운영
- TECH-CONCEPT-SECURITY-PRINCIPLE-001 — 보안 원칙
- TECH-CONCEPT-SECURITY-TEAM-001 — 보안 팀
- TECH-CONCEPT-SECURITY-TESTING-001 — 보안 테스팅
- TECH-CONTAINER-DOCKER-001 — Docker (기술)
- TECH-CONTAINER-K8S-001 — Kubernetes (기술)
- TECH-CRYPTO-AES-001 — AES
- TECH-CRYPTO-HASH-001 — Hash
- TECH-CRYPTO-RSA-001 — RSA
- TECH-DB-NOSQL-001 — NoSQL
- TECH-DB-SQL-001 — SQL DB
- TECH-DEVSECOPS-001 — DevSecOps (기술)
- TECH-IAM-PAM-001 — PAM
- TECH-IAM-RBAC-001 — RBAC
- TECH-IAM-SSO-001 — SSO
- TECH-IOT-001 — IoT
- TECH-LINUX-001 — Linux
- TECH-LOG-ELK-001 — ELK Stack
- TECH-LOG-SIEM-001 — SIEM (기술)
- TECH-MOBILE-001 — 모바일
- TECH-NET-ROUTING-001 — 라우팅
- TECH-NET-SDN-001 — SDN
- TECH-NET-SWITCHING-001 — 스위칭
- TECH-OS-LINUX-001 — Linux OS
- TECH-OS-MACOS-001 — macOS
- TECH-OS-WINDOWS-001 — Windows OS
- TECH-PKI-CA-001 — CA (인증기관)
- TECH-PKI-CERT-001 — 인증서
- TECH-VIRT-HYPERVISOR-001 — 하이퍼바이저
- TECH-VIRT-VM-001 — 가상머신
- TECH-WEB-API-001 — Web API
- TECH-WEB-BACKEND-001 — 백엔드
- TECH-WEB-FRONTEND-001 — 프론트엔드
- TECH-WINDOWS-001 — Windows

### VUL-* (21개) — 참조됐지만 없는 취약점 원자
- VUL-ACCESS-001 — 접근 취약점
- VUL-API-RATE-LIMIT-001 — API Rate Limit
- VUL-AUTH-BYPASS-001 — 인증 우회
- VUL-BUFFER-OVERFLOW-001 — 버퍼 오버플로우
- VUL-CLOUD-STORAGE-001 — 클라우드 스토리지
- VUL-COMMAND-INJECTION-001 — 명령어 인젝션
- VUL-CONFIG-DEFAULT-001 — 기본 설정
- VUL-CONFIG-EXPOSED-001 — 설정 노출
- VUL-CRITICAL-001 — 크리티컬
- VUL-CRYPTO-KEY-MGMT-001 — 키 관리
- VUL-CRYPTO-WEAK-CIPHER-001 — 약한 암호
- VUL-HEAP-OVERFLOW-001 — 힙 오버플로우
- VUL-IDOR-001 — IDOR (중복 ID?)
- VUL-IOT-001 — IoT 취약점
- VUL-LDAP-INJECTION-001 — LDAP 인젝션
- VUL-LOGIC-RACE-001 — Race Condition
- VUL-LOGIC-WORKFLOW-001 — 워크플로우 로직
- VUL-MOBILE-001 — 모바일 취약점
- VUL-PRIVILEGE-ESCALATION-001 — 권한 상승
- VUL-SQLI-001 — SQLi (중복 ID?)
- VUL-USE-AFTER-FREE-001 — Use-After-Free

### TOOL-* (3개)
- TOOL-CLOUD-SCOUTSUITE-001 — ScoutSuite
- TOOL-FORENSIC-001 — 포렌식 (일반)
- TOOL-PENTEST-001 — 펜테스트 (일반)

### CON-* (1개)
- CON-MIDDLEWARE-001 — 미들웨어

### CVE (참고, 별도 관리)
- CVE-2010-3332, CVE-2011-3389, CVE-2012-4818, CVE-2014-0160
- CVE-2014-3566, CVE-2015-0204, CVE-2015-4000, CVE-2017-0144
- CVE-2017-12149, CVE-2017-12617, CVE-2017-5638, CVE-2018-13379
- CVE-2019-11510, CVE-2019-5736, CVE-2020-14750, CVE-2020-14882
- CVE-2020-15257, CVE-2020-1938, CVE-2020-2551, CVE-2020-2555
- CVE-2020-4450, CVE-2021-26855, CVE-2021-4034, CVE-2021-44228
- CVE-2022-0847, CVE-2022-22965
(26개 — 원자화 대상? 아니면 참조만?)

---

## 소스 B: 재귀 분해로 발견된 추가 개념 (소스 A에 없는 것)

> KB 내부에서 참조조차 안 했지만, 설명에 필수적인 개념들

### 보안 표준/프레임워크
- OWASP Top 10
- CWE (Common Weakness Enumeration)
- CVE (Common Vulnerabilities and Exposures) 시스템
- CVSS (Common Vulnerability Scoring System)
- NVD (National Vulnerability Database)
- Cyber Kill Chain
- OWASP Testing Guide (WSTG)
- OWASP ASVS
- OWASP SAMM
- IOC (Indicator of Compromise)

### 프로토콜/메커니즘 세부
- SPN (Service Principal Name)
- TGT (Ticket Granting Ticket)
- TGS (Ticket Granting Service)
- KDC (Key Distribution Center)
- SPF (Sender Policy Framework)
- DKIM (DomainKeys Identified Mail)
- DMARC
- DNSSEC (개념, DEF-PREVENT-DNSSEC-001과 별도)
- DNS 캐시/TTL
- DNS Record Types (A/AAAA/CNAME/MX/NS)
- DNS Resolver vs Authoritative
- DNS over HTTPS/TLS (DoH/DoT)
- ARP (Address Resolution Protocol)
- TCP 3-Way Handshake
- UDP Protocol
- NTP Protocol (보안 관점)

### 브라우저/웹 보안 모델
- Same-Origin Policy (SOP)
- HttpOnly / Secure 쿠키 플래그
- DOM Sink/Source 모델
- Content-Type / MIME Type
- MIME Sniffing
- Event Handler (JS)
- innerHTML / document.write

### 인코딩/우회
- URL Encoding
- Base64 Encoding
- Double Encoding
- Hex Encoding
- HTTP Parameter Pollution (HPP)

### 인증/접근 제어
- RBAC vs ABAC (개념 비교)
- Service Account / Service Principal
- Access Key / Secret Key
- AssumeRole / Cross-Account Trust
- gMSA (Group Managed Service Account)
- Password Hash / Hash Cracking
- RC4 vs AES 암호화

### 클라우드 보안
- Shared Responsibility Model
- Cloud Metadata API (169.254.169.254)
- IMDS v1 vs v2
- IAM Policy Language (JSON 구조)
- Condition Key

### 컨테이너/리눅스 보안
- Linux Namespace
- Linux Cgroup
- Linux Capabilities
- Seccomp
- AppArmor / SELinux
- Docker Socket
- Privileged Mode
- Container Image 보안
- OCI Runtime (runc, containerd)

### 앱 보안
- Serialization/Deserialization 개념
- Gadget Chain
- Java Reflection / ClassLoader
- Magic Bytes / File Signature
- ORM (Object-Relational Mapping)
- ORM Injection
- Dynamic Query Building
- Stored Procedure 보안

### 네트워크 공격
- DNS Amplification
- NTP Amplification
- Memcached Amplification
- Anycast
- Traffic Scrubbing
- BGP Blackholing
- Slowloris / Slow HTTP
- Kaminsky Attack
- DNS Rebinding

### 랜섬웨어/맬웨어
- 대칭/비대칭 암호화 (공격 관점)
- 암호화폐 (Bitcoin/Monero)
- RDP (Remote Desktop Protocol)
- Volume Shadow Copy (VSS)
- 3-2-1 백업 규칙
- Double Extortion
- Ransomware-as-a-Service (RaaS)

### 이메일 보안
- Domain Spoofing
- MX Record
- URL Shortener (보안 관점)
- 사회공학 심리 기법
- Attachment/Macro 악성코드
- Phishing Kit
- OAuth Consent Phishing

### 웹 인프라
- Reverse Proxy
- URL 구조 / Query Parameter
- HTTP Methods (GET/POST 보안 차이)
- HTTP Header (개념)
- Webhook
- SSL Termination
- Error Handling / Custom Error Page

### WAF 세부
- Positive/Negative Security Model
- False Positive / False Negative
- ModSecurity CRS
- WAF Rule Writing
- Chunked Transfer Encoding
- HTTP Request Smuggling (CL.TE, TE.CL)
- ReDoS (Regular Expression DoS)

### DB 보안 세부
- information_schema
- DB별 시스템 테이블 차이
- MySQL FILE 권한 (LOAD_FILE/INTO OUTFILE)
- MySQL secure_file_priv
- MSSQL Linked Server
- MSSQL OPENROWSET
- Oracle UTL_HTTP/UTL_FILE
- xp_cmdshell
- MySQL Conditional Comments
- DB별 특수 함수 (SLEEP, WAITFOR, pg_sleep)
- SQL 주석 문법 차이

### 입력 검증
- Client-side vs Server-side Validation
- Whitelist vs Blacklist
- Escaping (이스케이핑)
- String Concatenation (보안 관점)
- Prepared Statement (개념)
- Regex 기반 필터링

---

## 통계

| 소스 | 수량 |
|------|------|
| A: KB 내부 broken refs | 203개 |
| A: 그 중 CVE | 26개 |
| A: 그 중 UUID (노이즈) | 4개 |
| **A: 순수 누락 원자** | **173개** |
| B: 재귀 분해 추가 | **~150개** |
| **A+B 합계 (로우)** | **~323개** |
| 중복 추정 (A∩B) | ~30개 |
| **예상 고유 합계** | **~290개** |

---

*2026-02-05 생성 — 분류 없는 로우 데이터*
