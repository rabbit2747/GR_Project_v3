# Phase 1 원자 목록 - 웹 애플리케이션 보안

> **목표**: 100개 원자 완성
> **실제 완료**: 103개 원자 (목표 초과 달성)
> **도메인**: 웹 애플리케이션 보안
> **상태**: ✅ **Phase 1 완료** (2025-01-29)

---

## 진행 상태 요약

| 카테고리 | 목표 | 완료 | 진행률 |
|----------|------|------|--------|
| 기술 (TECH) | - | 12 | +12 (추가) |
| 인프라 (INFRA) | 35 | 11 | 31% |
| 공격 (ATK) | 25 | 16 | 64% |
| 취약점 (VUL) | 15 | 15 | 100% |
| 방어 (DEF) | 20 | 20 | 100% |
| 도구 (TOOL) | 5 | 8 | 160% |
| 레거시 (GR-SEC-*) | - | 21 | +21 (추가) |
| **총계** | **100** | **103** | **103%** |

---

## 1. 기술 원자 (TECH) - 12개 ✅ 완료

> 원래 계획에 없었으나 Phase 1에서 추가 생성됨

### 1.1 프로토콜 (3개)

| # | ID | 이름 | 상태 |
|---|-----|------|------|
| 1 | TECH-PROTOCOL-HTTP-001 | HTTP Protocol | 🟢 |
| 2 | TECH-PROTOCOL-HTTPS-001 | HTTPS (HTTP Secure) | 🟢 |
| 3 | TECH-PROTOCOL-TCP-001 | TCP Protocol | 🟢 |

### 1.2 언어 (3개)

| # | ID | 이름 | 상태 |
|---|-----|------|------|
| 4 | TECH-LANG-HTML-001 | HTML | 🟢 |
| 5 | TECH-LANG-JAVASCRIPT-001 | JavaScript | 🟢 |
| 6 | TECH-LANG-SQL-001 | SQL | 🟢 |

### 1.3 데이터 형식 (2개)

| # | ID | 이름 | 상태 |
|---|-----|------|------|
| 7 | TECH-FORMAT-JSON-001 | JSON | 🟢 |
| 8 | TECH-FORMAT-XML-001 | XML | 🟢 |

### 1.4 개념 (4개)

| # | ID | 이름 | 상태 |
|---|-----|------|------|
| 9 | TECH-CONCEPT-COOKIE-001 | Cookie | 🟢 |
| 10 | TECH-CONCEPT-DOM-001 | DOM | 🟢 |
| 11 | TECH-CONCEPT-SESSION-001 | Session | 🟢 |
| 12 | TECH-CONCEPT-SHELL-001 | Shell | 🟢 |

---

## 2. 인프라 원자 (INFRA) - 11개 완료 / 35개 계획

### 2.1 애플리케이션 계층 (L7) - 4개 완료

| # | ID | 이름 | 우선순위 | 상태 |
|---|-----|------|----------|------|
| 1 | INFRA-APP-WAS-001 | Web Application Server | P0 | 🟢 |
| 2 | INFRA-APP-WEBSERVER-001 | Web Server (Nginx/Apache) | P0 | 🟢 |
| 3 | INFRA-APP-API-001 | REST API Server | P0 | 🟢 |
| 4 | INFRA-APP-WEBAPP-001 | Web Application | P0 | 🟢 |
| 5 | INFRA-APP-SPA-001 | Single Page Application | P1 | ⬜ |
| 6 | INFRA-APP-MOBILE-API-001 | Mobile Backend API | P1 | ⬜ |
| 7 | INFRA-APP-GRAPHQL-001 | GraphQL Server | P1 | ⬜ |
| 8 | INFRA-APP-WEBSOCKET-001 | WebSocket Server | P2 | ⬜ |
| 9 | INFRA-APP-SSR-001 | Server-Side Rendering | P2 | ⬜ |
| 10 | INFRA-APP-MICROSERVICE-001 | Microservice | P1 | ⬜ |
| 11 | INFRA-APP-SERVERLESS-001 | Serverless Function | P2 | ⬜ |
| 12 | INFRA-APP-PROXY-001 | Reverse Proxy | P1 | ⬜ |

### 2.2 데이터 계층 (L5) - 2개 완료

| # | ID | 이름 | 우선순위 | 상태 |
|---|-----|------|----------|------|
| 13 | INFRA-DATA-RDBMS-001 | Relational Database | P0 | 🟢 |
| 14 | INFRA-DATA-NOSQL-001 | NoSQL Database | P1 | ⬜ |
| 15 | INFRA-DATA-CACHE-001 | Cache Server (Redis) | P0 | 🟢 |
| 16 | INFRA-DATA-SEARCH-001 | Search Engine (Elasticsearch) | P2 | ⬜ |
| 17 | INFRA-DATA-MQ-001 | Message Queue | P1 | ⬜ |
| 18 | INFRA-DATA-OBJECTSTORE-001 | Object Storage (S3) | P1 | ⬜ |
| 19 | INFRA-DATA-SESSION-001 | Session Store | P1 | ⬜ |
| 20 | INFRA-DATA-FILESERVER-001 | File Server | P2 | ⬜ |

### 2.3 런타임 계층 (L6) - 0개 완료

| # | ID | 이름 | 우선순위 | 상태 |
|---|-----|------|----------|------|
| 21 | INFRA-RUNTIME-CONTAINER-001 | Container (Docker) | P1 | ⬜ |
| 22 | INFRA-RUNTIME-K8S-001 | Kubernetes | P1 | ⬜ |
| 23 | INFRA-RUNTIME-JVM-001 | Java Virtual Machine | P1 | ⬜ |
| 24 | INFRA-RUNTIME-NODEJS-001 | Node.js Runtime | P1 | ⬜ |
| 25 | INFRA-RUNTIME-PYTHON-001 | Python Runtime | P2 | ⬜ |

### 2.4 네트워크/보안 계층 (L2/Cross) - 5개 완료

| # | ID | 이름 | 우선순위 | 상태 |
|---|-----|------|----------|------|
| 26 | INFRA-NET-LB-001 | Load Balancer | P0 | 🟢 |
| 27 | INFRA-NET-WAF-001 | Web Application Firewall | P0 | 🟢 |
| 28 | INFRA-NET-CDN-001 | Content Delivery Network | P1 | 🟢 |
| 29 | INFRA-NET-FIREWALL-001 | Network Firewall | P1 | 🟢 |
| 30 | INFRA-NET-DNS-001 | DNS Server | P1 | 🟢 |
| 31 | INFRA-NET-VPN-001 | VPN Gateway | P2 | ⬜ |
| 32 | INFRA-IAM-SSO-001 | Single Sign-On | P1 | ⬜ |
| 33 | INFRA-IAM-OAUTH-001 | OAuth Provider | P1 | ⬜ |
| 34 | INFRA-IAM-LDAP-001 | LDAP/Active Directory | P2 | ⬜ |
| 35 | INFRA-SEC-VAULT-001 | Secrets Management | P1 | ⬜ |

---

## 3. 공격 원자 (ATK) - 16개 완료 / 25개 계획

### 3.1 인젝션 공격 - 4개 완료

| # | ID | 이름 | MITRE ID | 우선순위 | 상태 |
|---|-----|------|----------|----------|------|
| 36 | ATK-INJECT-SQL-001 | SQL Injection | T1190 | P0 | 🟢 |
| 37 | ATK-INJECT-XSS-001 | Cross-Site Scripting | T1059.007 | P0 | 🟢 |
| 38 | ATK-INJECT-CMD-001 | Command Injection | T1059 | P0 | 🟢 |
| 39 | ATK-INJECT-LDAP-001 | LDAP Injection | T1190 | P1 | ⬜ |
| 40 | ATK-INJECT-XML-001 | XML Injection (XXE) | T1190 | P0 | 🟢 |
| 41 | ATK-INJECT-SSTI-001 | Server-Side Template Injection | T1190 | P1 | ⬜ |
| 42 | ATK-INJECT-NOSQL-001 | NoSQL Injection | T1190 | P1 | ⬜ |
| 43 | ATK-INJECT-HEADER-001 | HTTP Header Injection | T1190 | P2 | ⬜ |

### 3.2 인증/세션 공격 - 5개 완료

| # | ID | 이름 | MITRE ID | 우선순위 | 상태 |
|---|-----|------|----------|----------|------|
| 44 | ATK-AUTH-BRUTEFORCE-001 | Brute Force Attack | T1110 | P0 | 🟢 |
| 45 | ATK-AUTH-CREDSTUFF-001 | Credential Stuffing | T1110.004 | P1 | 🟢 |
| 46 | ATK-SESSION-HIJACK-001 | Session Hijacking | T1539 | P0 | 🟢 |
| 47 | ATK-SESSION-FIXATION-001 | Session Fixation | T1539 | P1 | ⬜ |
| 48 | ATK-AUTH-BYPASS-001 | Authentication Bypass | T1078 | P0 | 🟢 |
| 49 | ATK-AUTH-CSRF-001 | Cross-Site Request Forgery | T1185 | P0 | 🟢 |

### 3.3 서버 측 공격 - 5개 완료

| # | ID | 이름 | MITRE ID | 우선순위 | 상태 |
|---|-----|------|----------|----------|------|
| 50 | ATK-SERVER-SSRF-001 | Server-Side Request Forgery | T1090 | P0 | 🟢 |
| 51 | ATK-SERVER-DESER-001 | Insecure Deserialization | T1190 | P0 | 🟢 |
| 52 | ATK-SERVER-FILEUPLOAD-001 | Malicious File Upload | T1105 | P0 | 🟢 |
| 53 | ATK-SERVER-PATH-001 | Path Traversal | T1083 | P0 | 🟢 |
| 54 | ATK-SERVER-RFI-001 | Remote File Inclusion | T1105 | P0 | 🟢 |
| 55 | ATK-SERVER-IDOR-001 | Insecure Direct Object Reference | T1078 | P1 | ⬜ |
| 56 | ATK-SERVER-OPENREDIR-001 | Open Redirect | T1036 | P2 | ⬜ |

### 3.4 기타 공격 - 2개 완료

| # | ID | 이름 | MITRE ID | 우선순위 | 상태 |
|---|-----|------|----------|----------|------|
| 57 | ATK-WEB-CLICKJACK-001 | Clickjacking | T1185 | P2 | 🟢 |
| 58 | ATK-NET-MITM-001 | Man-in-the-Middle | T1557 | P1 | 🟢 |
| 59 | ATK-DOS-HTTP-001 | HTTP Flood (DDoS) | T1498 | P1 | ⬜ |
| 60 | ATK-DOS-SLOWLORIS-001 | Slowloris Attack | T1498 | P2 | ⬜ |

---

## 4. 취약점 원자 (VUL) - 15개 ✅ 완료

| # | ID | 이름 | CWE ID | 우선순위 | 상태 |
|---|-----|------|--------|----------|------|
| 61 | VUL-INJECT-SQL-001 | SQL Injection Vulnerability | CWE-89 | P0 | 🟢 |
| 62 | VUL-INJECT-XSS-001 | XSS Vulnerability | CWE-79 | P0 | 🟢 |
| 63 | VUL-INJECT-CMD-001 | Command Injection Vulnerability | CWE-78 | P0 | 🟢 |
| 64 | VUL-AUTH-BROKEN-001 | Broken Authentication | CWE-287 | P0 | 🟢 |
| 65 | VUL-AUTH-SESSION-001 | Session Management Flaw | CWE-384 | P1 | 🟢 |
| 66 | VUL-CRYPTO-WEAK-001 | Weak Cryptography | CWE-327 | P1 | 🟢 |
| 67 | VUL-CONFIG-MISCONFIG-001 | Security Misconfiguration | CWE-16 | P0 | 🟢 |
| 68 | VUL-ACCESS-BROKEN-001 | Broken Access Control | CWE-284 | P0 | 🟢 |
| 69 | VUL-DATA-EXPOSURE-001 | Sensitive Data Exposure | CWE-200 | P0 | 🟢 |
| 70 | VUL-DESER-INSECURE-001 | Insecure Deserialization | CWE-502 | P0 | 🟢 |
| 71 | VUL-COMPONENT-VULN-001 | Vulnerable Components | CWE-1035 | P1 | 🟢 |
| 72 | VUL-LOG-INSUFFICIENT-001 | Insufficient Logging | CWE-778 | P2 | 🟢 |
| 73 | VUL-SSRF-001 | SSRF Vulnerability | CWE-918 | P0 | 🟢 |
| 74 | VUL-XXE-001 | XXE Vulnerability | CWE-611 | P0 | 🟢 |
| 75 | VUL-PATH-TRAVERSAL-001 | Path Traversal Vulnerability | CWE-22 | P0 | 🟢 |

---

## 5. 방어 원자 (DEF) - 20개 ✅ 완료

### 5.1 예방 (Prevention) - 12개 완료

| # | ID | 이름 | D3FEND | 우선순위 | 상태 |
|---|-----|------|--------|----------|------|
| 76 | DEF-PREVENT-PARAMQUERY-001 | Parameterized Query | D3-PQ | P0 | 🟢 |
| 77 | DEF-PREVENT-INPUTVAL-001 | Input Validation | D3-IV | P0 | 🟢 |
| 78 | DEF-PREVENT-OUTPUTENC-001 | Output Encoding | D3-OE | P0 | 🟢 |
| 79 | DEF-PREVENT-CSP-001 | Content Security Policy | D3-CSP | P0 | 🟢 |
| 80 | DEF-PREVENT-CSRF-TOKEN-001 | CSRF Token | D3-CT | P0 | 🟢 |
| 81 | DEF-PREVENT-HTTPS-001 | HTTPS/TLS Enforcement | D3-TE | P0 | 🟢 |
| 82 | DEF-PREVENT-CORS-001 | CORS Configuration | - | P1 | 🟢 |
| 83 | DEF-PREVENT-HEADERS-001 | Security Headers | - | P1 | 🟢 |
| 84 | DEF-PREVENT-RATELIMIT-001 | Rate Limiting | D3-RL | P0 | 🟢 |
| 85 | DEF-PREVENT-MFA-001 | Multi-Factor Authentication | D3-MFA | P0 | 🟢 |
| 86 | DEF-PREVENT-ENCRYPT-001 | Data Encryption | D3-DE | P0 | 🟢 |
| 87 | DEF-PREVENT-SANDBOX-001 | Sandboxing | D3-SB | P2 | 🟢 |

### 5.2 탐지 (Detection) - 5개 완료

| # | ID | 이름 | D3FEND | 우선순위 | 상태 |
|---|-----|------|--------|----------|------|
| 88 | DEF-DETECT-WAF-001 | WAF Detection Rules | D3-WA | P0 | 🟢 |
| 89 | DEF-DETECT-IDS-001 | Intrusion Detection | D3-ID | P1 | 🟢 |
| 90 | DEF-DETECT-LOGGING-001 | Security Logging | D3-SL | P0 | 🟢 |
| 91 | DEF-DETECT-MONITORING-001 | Security Monitoring | D3-SM | P1 | 🟢 |
| 92 | DEF-DETECT-ANOMALY-001 | Anomaly Detection | D3-AD | P2 | 🟢 |

### 5.3 대응 (Response) - 3개 완료

| # | ID | 이름 | D3FEND | 우선순위 | 상태 |
|---|-----|------|--------|----------|------|
| 93 | DEF-RESPOND-INCIDENT-001 | Incident Response | D3-IR | P1 | 🟢 |
| 94 | DEF-RESPOND-BLOCK-001 | IP/Request Blocking | D3-BL | P1 | 🟢 |
| 95 | DEF-RESPOND-QUARANTINE-001 | Account Quarantine | D3-AQ | P2 | 🟢 |

---

## 6. 도구 원자 (TOOL) - 8개 완료 (목표 초과)

| # | ID | 이름 | 유형 | 우선순위 | 상태 |
|---|-----|------|------|----------|------|
| 96 | TOOL-OFFENSE-BURP-001 | Burp Suite | 공격/테스트 | P0 | 🟢 |
| 97 | TOOL-OFFENSE-SQLMAP-001 | SQLMap | 공격/테스트 | P0 | 🟢 |
| 98 | TOOL-OFFENSE-ZAP-001 | OWASP ZAP | 공격/테스트 | P1 | 🟢 |
| 99 | TOOL-OFFENSE-METASPLOIT-001 | Metasploit Framework | 공격/테스트 | P1 | 🟢 |
| 100 | TOOL-DEFENSE-MODSEC-001 | ModSecurity | 방어 | P1 | 🟢 |
| 101 | TOOL-AUDIT-NMAP-001 | Nmap | 감사 | P1 | 🟢 |
| 102 | TOOL-AUDIT-NIKTO-001 | Nikto | 감사 | P1 | 🟢 |
| 103 | TOOL-AUDIT-WIRESHARK-001 | Wireshark | 감사 | P1 | 🟢 |

---

## 7. 레거시 원자 (GR-SEC-*) - 21개 ✅ 완료

> SQLi 상세 원자 (초기 Phase 0에서 생성)

### 7.1 원칙/개념 (3개)

| ID | 이름 | Level |
|-----|------|-------|
| GR-SEC-PRI-00001 | Untrusted Input-Code Mixing Danger | 4 (Principle) |
| GR-SEC-CON-00001 | Injection Vulnerability | 3 (Concept) |
| GR-SEC-CON-00002 | SQL Injection | 3 (Concept) |

### 7.2 기법 (10개)

| ID | 이름 | Category |
|-----|------|----------|
| GR-SEC-TEC-00001 | UNION-based SQL Injection | Exploitation |
| GR-SEC-TEC-00002 | Blind Boolean-based SQL Injection | Exploitation |
| GR-SEC-TEC-00003 | Blind Time-based SQL Injection | Exploitation |
| GR-SEC-TEC-00004 | Error-based SQL Injection | Exploitation |
| GR-SEC-TEC-00005 | Stacked Queries SQL Injection | Exploitation |
| GR-SEC-TEC-00006 | Out-of-Band SQL Injection | Exploitation |
| GR-SEC-TEC-00007 | Second-Order SQL Injection | Exploitation |
| GR-SEC-TEC-00008 | Comment-based WAF Bypass | Evasion |
| GR-SEC-TEC-00009 | Encoding-based WAF Bypass | Evasion |
| GR-SEC-TEC-00010 | Case and Whitespace Manipulation Bypass | Evasion |

### 7.3 인스턴스 (8개)

| ID | 이름 | Category |
|-----|------|----------|
| GR-SEC-INS-P0001 | Single Quote Error Payload | Detection |
| GR-SEC-INS-P0002 | Boolean True/False Detection Payload | Detection |
| GR-SEC-INS-P0003 | Time-based SLEEP Detection Payload | Detection |
| GR-SEC-INS-P0004 | UNION Column Count Detection Payload | Exploitation |
| GR-SEC-INS-P0005 | UNION Data Extraction Payload | Exploitation |
| GR-SEC-INS-F0001 | MySQL DBMS Fingerprint | Reconnaissance |
| GR-SEC-INS-F0002 | MSSQL DBMS Fingerprint | Reconnaissance |
| GR-SEC-INS-F0003 | PostgreSQL DBMS Fingerprint | Reconnaissance |

---

## 8. Phase 2 대상 (미완료 원자)

### P1 우선순위 미완료 항목

| 카테고리 | ID | 이름 |
|----------|-----|------|
| INFRA | INFRA-APP-SPA-001 | Single Page Application |
| INFRA | INFRA-APP-MOBILE-API-001 | Mobile Backend API |
| INFRA | INFRA-DATA-MQ-001 | Message Queue |
| INFRA | INFRA-RUNTIME-* | Container, K8s, JVM, Node.js |
| INFRA | INFRA-IAM-* | SSO, OAuth |
| ATK | ATK-INJECT-LDAP-001 | LDAP Injection |
| ATK | ATK-SESSION-FIXATION-001 | Session Fixation |
| ATK | ATK-SERVER-IDOR-001 | IDOR |

---

## 9. 상태 범례

| 아이콘 | 의미 |
|--------|------|
| ⬜ | 미시작 |
| 🟡 | 진행 중 |
| 🟢 | 완료 |
| 🔴 | 이슈 발생 |

---

## 10. 완료 기록

- **2025-01-29**: Phase 1 완료 - 103개 원자 달성 (목표 100개 초과)
- 취약점(VUL), 방어(DEF), 도구(TOOL) 카테고리 100% 완료
- Dangling Reference 59개 존재 (Phase 2에서 해결 예정)
