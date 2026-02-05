# Domain S: Security (보안)

**버전**: v2.0
**최종 수정**: 2025-11-20
**목적**: 인증, 인가, 암호화, 취약점 관리, 보안 모니터링

---

## 1. Domain 개요

### 1.1 정의
Security Domain은 **기밀성(Confidentiality), 무결성(Integrity), 가용성(Availability)** 보장을 위한 보안 통제 집합입니다.

### 1.2 v1.0 → v2.0 변경사항
- Vulnerability Management (S4) 추가
- SIEM 통합 (S5 확장)
- AI/ML 보안 (S7.4) 추가
- v2.1: Endpoint & Extended Security (S9), Cloud Security (S10), Web AppSec Controls (S11), Advanced Security (S12), Digital Forensics (S13), Platform-Specific Security (S14) 추가
- Total tags: 25 → 60+

### 1.3 핵심 목표
1. **Zero Trust Architecture**: "절대 신뢰하지 말고, 항상 검증하라"
2. **Defense in Depth**: 다층 보안 방어
3. **Least Privilege**: 최소 권한 원칙
4. **Security by Design**: 설계 단계부터 보안 고려

---

## 2. Tag 체계

### Tag 구조
```
S + [숫자] + (선택적 서브 카테고리)
예: S1 (Perimeter Security), S2.1 (Authentication - MFA)
```

---

## 3. Tag 상세 정의

### S1: Perimeter Security (경계 보안)

**목적**: 외부 위협 차단 (Zone 0 → Zone 1 경계)

**구성 요소**:
- **S1.1**: WAF (Web Application Firewall)
  - 도구: AWS WAF, Cloudflare WAF, ModSecurity
  - 차단: SQL Injection, XSS, CSRF, OWASP Top 10
  - Rule Set: AWS Managed Rules, OWASP CRS

- **S1.2**: DDoS Protection
  - 도구: AWS Shield Advanced, Cloudflare
  - Layer 3/4: SYN Flood, UDP Amplification
  - Layer 7: HTTP Flood, Slowloris

- **S1.3**: Bot Management
  - 도구: Cloudflare Bot Management
  - 탐지: User-Agent, Behavioral analysis
  - CAPTCHA: hCaptcha, reCAPTCHA v3

**Layer/Zone 연관**: L1 (Perimeter), Zone 1

**CVE 예시**:
```yaml
CVE-2024-12345: ModSecurity Bypass
  Affected: ModSecurity 3.0.x
  Severity: High
  Mitigation: Upgrade to 3.0.10
```

**MITRE ATT&CK**: T1190 (Exploit Public-Facing Application)

---

### S2: Authentication & Authorization (인증 및 인가)

**목적**: 사용자 신원 확인 및 접근 권한 관리

**구성 요소**:
- **S2.1**: Authentication
  - **S2.1.1**: Password-based (bcrypt, Argon2)
  - **S2.1.2**: MFA (TOTP, WebAuthn, SMS)
  - **S2.1.3**: SSO (SAML 2.0, OAuth 2.0, OIDC)

- **S2.2**: Authorization
  - **S2.2.1**: RBAC (Role-Based Access Control)
  - **S2.2.2**: ABAC (Attribute-Based Access Control)
  - **S2.2.3**: OAuth 2.0 & JWT (RS256)

**Layer/Zone 연관**: L1-L2, Zone 1-2

**사용 예시**:
```yaml
JWT Token (S2.2.3):
  {
    "sub": "user_12345",
    "roles": ["user", "premium"],
    "iat": 1700000000,
    "exp": 1700003600
  }
  Signed with: RSA-SHA256
```

**MITRE ATT&CK**: T1078 (Valid Accounts), T1110 (Brute Force)

---

### S3: Data Protection (데이터 보호)

**목적**: 데이터 암호화 및 보안 전송

**구성 요소**:
- **S3.1**: Encryption in Transit
  - TLS 1.3, mTLS (Mutual TLS)
  - Certificate: Let's Encrypt, ACM

- **S3.2**: Encryption at Rest
  - Database: PostgreSQL TDE, AES-256
  - File: AWS S3 SSE-KMS
  - Key Management: AWS KMS, HashiCorp Vault

- **S3.3**: Data Masking & Tokenization
  - PII Masking: Email, Phone
  - Tokenization: Credit Card → Token

**Layer/Zone 연관**: All Layers, Zone 1-3

**사용 예시**:
```yaml
TLS Configuration (S3.1):
  Protocol: TLS 1.3
  Cipher: TLS_AES_256_GCM_SHA384
  Certificate: Let's Encrypt Wildcard
  HSTS: max-age=31536000
```

**MITRE ATT&CK**: T1557 (Man-in-the-Middle)

---

### S4: Vulnerability Management (v2.0 신규)

**목적**: 취약점 탐지, 평가, 패치 관리

**구성 요소**:
- **S4.1**: Vulnerability Scanning
  - 도구: Nessus, Qualys, AWS Inspector
  - 스캔: OS, Applications, Libraries
  - 주기: Weekly (non-prod), Monthly (prod)

- **S4.2**: Dependency Scanning
  - 도구: Snyk, Dependabot, npm audit
  - Auto-fix: Minor version updates

- **S4.3**: Patch Management
  - OS: Automated (AWS Systems Manager)
  - Application: Tested in staging → Production
  - SLA: Critical (24h), High (7d), Medium (30d)

**Layer/Zone 연관**: All Layers, Zone 2-4

**사용 예시**:
```yaml
Vulnerability Workflow:
  1. Scan: AWS Inspector (S4.1)
  2. Finding: CVE-2024-67890 (PostgreSQL 14.0, Critical)
  3. Assess: CVSS 9.8, Exploitable
  4. Remediate: Upgrade 14.0 → 14.10
  5. Verify: Re-scan
  6. Report: Update vulnerability DB (atomized format)
```

**MITRE ATT&CK**: T1190 (Exploit Public-Facing Application)

---

### S5: Security Monitoring & Incident Response

**목적**: 보안 이벤트 탐지, 분석, 대응

**구성 요소**:
- **S5.1**: SIEM (Security Information and Event Management)
  - 도구: Splunk, QRadar, Azure Sentinel
  - Logs: WAF, Authentication, Database Audit

- **S5.2**: Threat Intelligence
  - 도구: MISP, ThreatConnect
  - IoC: IP, Domain, Hash

- **S5.3**: Incident Response
  - Playbook: NIST CSF
  - Phases: Identify → Protect → Detect → Respond → Recover

**Layer/Zone 연관**: L4 (Management), Zone 4

**사용 예시**:
```yaml
Security Incident: Brute Force Attack
  Detection: 150 failed login attempts in 5 minutes (S5.1)
  Source IP: 203.0.113.45
  Action:
    - Block IP at WAF (S1.1)
    - Alert: Slack #security-alerts
  MITRE ATT&CK: T1110.001 (Brute Force)
```

**MITRE ATT&CK**: T1078 (Valid Accounts), T1110 (Brute Force)

---

### S6: Identity & Access Management (IAM)

**목적**: 사용자 및 서비스 계정 관리

**구성 요소**:
- **S6.1**: User Lifecycle Management
  - Provisioning: Automated (SCIM)
  - De-provisioning: Offboarding
  - Access Review: Quarterly

- **S6.2**: Service Accounts & API Keys
  - Rotation: Every 90 days
  - Storage: AWS Secrets Manager, Vault

- **S6.3**: Privileged Access Management (PAM)
  - Just-in-Time Access
  - Session Recording
  - Approval Workflow

**Layer/Zone 연관**: L4 (Management), Zone 4

**사용 예시**:
```yaml
IAM Policy (S6.1):
  User: developer@example.com
  Role: Developer
  Permissions:
    - EC2: Read (Zone 2 only)
    - S3: Read/Write (bucket: dev-assets)
    - RDS: Connect (dev-database only)
```

**MITRE ATT&CK**: T1078 (Valid Accounts)

---

### S7: Application Security

**목적**: 소프트웨어 개발 단계 보안

**구성 요소**:
- **S7.1**: SAST (Static Application Security Testing)
  - 도구: SonarQube, Checkmarx, Semgrep
  - 탐지: SQL Injection, XSS, Hardcoded Secrets

- **S7.2**: DAST (Dynamic Application Security Testing)
  - 도구: OWASP ZAP, Burp Suite
  - Testing: Running application (staging)

- **S7.3**: Dependency Security
  - 도구: Snyk, npm audit, OWASP Dependency-Check
  - Auto-fix: Automated PR

- **S7.4**: AI/ML Security (v2.0 신규)
  - Prompt Injection Detection
  - Model Poisoning Prevention
  - Data Privacy in Training

**Layer/Zone 연관**: L2 (Application), Zone 2

**사용 예시**:
```yaml
CI/CD Security Pipeline:
  1. SAST: SonarQube (fail on Critical/High)
  2. Dependency Scan: Snyk (auto-upgrade)
  3. DAST: OWASP ZAP (staging)
  4. Security Review: Manual sign-off
  5. Deploy: Production
```

**MITRE ATT&CK**: T1059 (Command Injection), T1505 (Web Shell)

---

### S8: Compliance & Audit

**목적**: 규제 준수 및 감사 추적

**구성 요소**:
- **S8.1**: Audit Logging
  - 도구: AWS CloudTrail, Azure Activity Log
  - Retention: 7 years

- **S8.2**: Compliance Frameworks
  - Standards: SOC 2, ISO 27001, PCI-DSS, GDPR
  - Controls: CIS Benchmarks, NIST CSF

- **S8.3**: Data Residency & Privacy
  - GDPR: Right to be Forgotten
  - Data Localization: EU data in EU region

**Layer/Zone 연관**: All Layers, Zone 3-4

**사용 예시**:
```yaml
Audit Log (S8.1):
  event: "IAM Policy Changed"
  user: "admin@example.com"
  resource: "iam:policy/DeveloperAccess"
  compliance_tag: "SOC2_CC6.1"

GDPR Request (S8.3):
  Type: Right to be Forgotten
  Actions:
    - Delete user data (PostgreSQL)
    - Delete backups (S3)
    - Anonymize logs
```

**MITRE ATT&CK**: T1078 (Valid Accounts), T1565 (Data Manipulation)

---

### S9: Endpoint & Extended Security (엔드포인트 & 확장 탐지)

**목적**: 엔드포인트, 네트워크, 통합 탐지/대응

**구성 요소**:
- **S9.1**: EDR (Endpoint Detection and Response)
  - 도구: CrowdStrike Falcon, Microsoft Defender for Endpoint, SentinelOne
  - 탐지: 프로세스 행위 분석, 파일리스 공격, 메모리 인젝션
  - 대응: 프로세스 격리, 파일 삭제, 네트워크 차단

- **S9.2**: XDR (Extended Detection and Response)
  - 도구: Palo Alto Cortex XDR, Trend Micro Vision One
  - 통합: Endpoint + Network + Email + Cloud 상관 분석
  - 탐지: 크로스-레이어 위협 체인 탐지

- **S9.3**: NDR (Network Detection and Response)
  - 도구: Darktrace, Vectra AI, ExtraHop
  - 탐지: 네트워크 트래픽 이상 행위, Lateral Movement
  - 분석: 패킷 캡처, 메타데이터 분석, ML 기반 이상 탐지

**Layer/Zone 연관**: L3-L5 (Endpoint/Network), Zone 1-3

**MITRE ATT&CK**: T1055 (Process Injection), T1021 (Remote Services), T1071 (Application Layer Protocol)

---

### S10: Cloud Security (클라우드 보안)

**목적**: 클라우드 환경 특화 보안 통제

**구성 요소**:
- **S10.1**: CASB (Cloud Access Security Broker)
  - 도구: Netskope, Microsoft Defender for Cloud Apps, Zscaler
  - 통제: Shadow IT 탐지, SaaS 접근 제어, DLP 연동

- **S10.2**: CSPM (Cloud Security Posture Management)
  - 도구: Prisma Cloud, AWS Security Hub, Wiz
  - 탐지: 설정 오류, 과도한 권한, 미암호화 리소스
  - 기준: CIS Benchmarks, AWS Well-Architected

- **S10.3**: CWPP (Cloud Workload Protection Platform)
  - 도구: Aqua Security, Sysdig, Lacework
  - 보호: 컨테이너 런타임, 서버리스, VM 워크로드
  - 탐지: 취약 이미지, 런타임 이상 행위

- **S10.4**: CIEM (Cloud Infrastructure Entitlement Management)
  - 도구: Ermetic, CloudKnox, Sonrai
  - 통제: 과도한 IAM 권한 탐지, 최소 권한 적용
  - 분석: 미사용 권한, 크로스 계정 접근

**Layer/Zone 연관**: L2-L4 (Cloud), Zone 1-4

**MITRE ATT&CK**: T1078 (Valid Accounts), T1530 (Data from Cloud Storage), T1580 (Cloud Infrastructure Discovery)

---

### S11: Web Application Security Controls (웹 애플리케이션 보안 통제)

**목적**: 웹 애플리케이션 레벨의 보안 통제 메커니즘

**구성 요소**:
- **S11.1**: Input Validation & Output Encoding
  - 입력 검증: 화이트리스트, 정규식, 타입/길이 검증
  - 출력 인코딩: HTML Entity, JavaScript Escape, URL Encoding
  - 적용: 서버사이드 필수, 클라이언트사이드 보조

- **S11.2**: Security Headers (CSP, CORS, HSTS)
  - CSP: Content-Security-Policy (XSS 방어)
  - CORS: Cross-Origin Resource Sharing 정책
  - HSTS: HTTP Strict Transport Security
  - 기타: X-Frame-Options, X-Content-Type-Options

- **S11.3**: CSRF Protection
  - CSRF Token: Synchronizer Token Pattern
  - SameSite Cookie: Lax/Strict
  - Double Submit Cookie

- **S11.4**: Parameterized Query / ORM
  - Prepared Statements: SQL Injection 원천 방지
  - ORM: SQLAlchemy, Hibernate, Prisma
  - Stored Procedures

**Layer/Zone 연관**: L5-L7 (Application), Zone 2

**MITRE ATT&CK**: T1059 (Command Injection), T1189 (Drive-by Compromise)

---

### S12: Advanced Security (고급 보안)

**목적**: 특수 보안 기술 및 아키텍처

**구성 요소**:
- **S12.1**: DLP (Data Loss Prevention)
  - 도구: Symantec DLP, Microsoft Purview, Digital Guardian
  - 통제: 이메일 첨부, USB, 클라우드 업로드 차단
  - 정책: PII, PHI, 신용카드 번호 탐지

- **S12.2**: Email Security
  - 도구: Proofpoint, Mimecast, Microsoft Defender for Office 365
  - 탐지: 피싱, BEC, 악성 첨부파일
  - 통제: SPF, DKIM, DMARC

- **S12.3**: UEBA (User and Entity Behavior Analytics)
  - 도구: Exabeam, Securonix, Microsoft Sentinel UEBA
  - 탐지: 내부자 위협, 계정 탈취, 이상 접근 패턴
  - 분석: 베이스라인 학습, 편차 탐지

- **S12.4**: Deception Technology
  - 도구: Attivo Networks, Illusive Networks, TrapX
  - 배포: Honeypot, Honey Token, Decoy 계정
  - 탐지: 공격자 Lateral Movement, 내부 정찰

- **S12.5**: Zero Trust Architecture
  - 원칙: Never Trust, Always Verify
  - 구현: Micro-segmentation, ZTNA, SDP
  - 도구: Zscaler, Cloudflare Access, BeyondTrust

- **S12.6**: SOAR (Security Orchestration, Automation and Response)
  - 도구: Splunk SOAR, IBM Resilient, Palo Alto XSOAR
  - 기능: Playbook 자동화, 인시던트 오케스트레이션
  - 연동: SIEM, EDR, Firewall, Ticketing

- **S12.7**: Sandboxing
  - 도구: Any.Run, Joe Sandbox, Cuckoo Sandbox
  - 분석: 악성코드 동적 분석, 파일 실행 격리
  - 탐지: 파일 행위, 네트워크 IOC, 레지스트리 변경

**Layer/Zone 연관**: All Layers, Zone 1-4

**MITRE ATT&CK**: T1566 (Phishing), T1090 (Proxy), T1030 (Data Transfer Size Limits)

---

### S13: Digital Forensics (디지털 포렌식)

**목적**: 보안 사고 후 증거 수집, 분석, 보존

**구성 요소**:
- **S13.1**: Disk Forensics
  - 도구: EnCase, FTK, Autopsy
  - 수집: 디스크 이미징 (dd, E01)
  - 분석: 파일 시스템, 삭제 파일 복구, 타임라인

- **S13.2**: Memory Forensics
  - 도구: Volatility, Rekall
  - 수집: 메모리 덤프 (WinPmem, LiME)
  - 분석: 프로세스, 네트워크 연결, 인젝션된 코드

- **S13.3**: Network Forensics
  - 도구: Wireshark, NetworkMiner, Zeek (Bro)
  - 수집: PCAP 캡처, NetFlow
  - 분석: 세션 재구성, 악성 트래픽, 데이터 유출 탐지

**Layer/Zone 연관**: L3-L5, Zone 3-5

**MITRE ATT&CK**: T1005 (Data from Local System), T1074 (Data Staged)

---

### S14: Platform-Specific Security (플랫폼별 보안)

**목적**: 특정 OS/플랫폼 환경 보안 통제

**구성 요소**:
- **S14.1**: Windows Security Controls
  - ASR (Attack Surface Reduction) Rules
  - Credential Guard: LSASS 보호
  - LAPS (Local Administrator Password Solution)
  - AppLocker / WDAC: 애플리케이션 통제
  - Windows Defender: 실시간 보호

- **S14.2**: Linux Security Controls
  - SELinux / AppArmor: MAC (Mandatory Access Control)
  - iptables / nftables: 호스트 방화벽
  - auditd: 시스템 감사 로깅
  - seccomp: 시스템 콜 필터링

- **S14.3**: macOS Security Controls
  - Gatekeeper: 코드 서명 검증
  - System Integrity Protection (SIP)
  - FileVault: 전체 디스크 암호화
  - XProtect: 악성코드 탐지

**Layer/Zone 연관**: L5 (Endpoint), Zone 3-5

**MITRE ATT&CK**: T1003 (OS Credential Dumping), T1547 (Boot Autostart Execution)

---

## 4. Layer/Zone 연관성

### Layer별 Security Controls

| Layer | 주요 Tags | 통제 |
|-------|----------|------|
| L0 | S1.2 | DDoS Protection |
| L1 | S1.1, S2.1 | WAF, Authentication |
| L2 | S7.1, S2.2 | SAST, Authorization |
| L3 | S3.2, S8.1 | Encryption at Rest, Audit |
| L4 | S6.3, S5.1 | PAM, SIEM |
| L5 | S2.1.2 | MFA |

### Zone별 Security Posture

```
Zone 0-A: Trust 0%, Controls: S1.1, S1.2, S1.3
Zone 0-B: Trust 10%, Controls: S2.2.3, S3.1
Zone 1: Trust 30%, Controls: S2.1, S3.1, S1.1
Zone 2: Trust 50%, Controls: S2.2, S7.1, S3.1
Zone 3: Trust 80%, Controls: S3.2, S8.1
Zone 4: Trust 90%, Controls: S6.3, S2.1.2
Zone 5: Trust 20%, Controls: S2.1.2
```

---

## 5. CVE 매핑 (Domain T 연동)

| CVE ID | 도구 | Tech Stack Tag | Severity |
|--------|------|---------------|----------|
| CVE-2024-11111 | Keycloak <22.0.0 | T4.2 | Critical |
| CVE-2024-22222 | NGINX ModSecurity | T3.1 | High |
| CVE-2024-33333 | Vault | T4.7 | Medium |

---

## 6. MITRE ATT&CK 매핑

| Technique | Security Tag | 탐지/차단 |
|-----------|-------------|----------|
| T1078 | S5.1 | SIEM 이상 탐지 |
| T1110 | S2.1.2, S5.1 | MFA, Rate Limiting |
| T1190 | S1.1, S7.2 | WAF, DAST |
| T1486 | S3.2, S8.1 | Backup, Audit |
| T1552 | S7.1, S6.2 | SAST, Secrets Manager |

---

## 7. 다음 단계

- **Domain M (Monitoring)**: S5.1과 연동 (SIEM)
- **Domain C (Compliance)**: S8.2와 연동 (규제)
- **Domain T (Tech Stack)**: S4.1과 연동 (CVE)

---

**문서 종료**
