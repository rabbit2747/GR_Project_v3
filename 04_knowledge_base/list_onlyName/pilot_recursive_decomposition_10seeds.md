# 🧪 재귀적 개념 분해 — 10개 시드 종합 분석

> **시드 선정 기준**: 서로 다른 공격 카테고리 (웹/네트워크/AD/클라우드/컨테이너/맬웨어/사회공학/앱)
> **방법**: 각 시드 → Level 1 분해 → KB 대조 → Level 2 분해 (필요시)
> **범위**: ✅ 존재 / ❌ 누락 / 🔶 부분 존재 / ⛔ 범위 밖

---

## 시드 1: SQL Injection (ATK-INJECT-SQL-001)
> 별도 분석 완료 → `pilot_recursive_decomposition_sqli.md` 참조
> 누락: ~50개 (필수 13, 권장 19, TODO 18)

---

## 시드 2: XSS (ATK-INJECT-XSS-001) — 웹 클라이언트 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| HTML | ✅ | `TECH-LANG-HTML-001` |
| JavaScript | ✅ | `TECH-LANG-JAVASCRIPT-001` |
| DOM | ✅ | `TECH-CONCEPT-DOM-001` |
| Web Browser | ✅ | `TECH-CONCEPT-BROWSER-001` |
| Cookie | ✅ | `TECH-CONCEPT-COOKIE-001` |
| Web Session | ✅ | `TECH-CONCEPT-SESSION-001` |
| Web Application | ✅ | `INFRA-APP-WEBAPP-001` |
| Session Hijacking | ✅ | `ATK-SESSION-HIJACK-001` |
| CSRF | ✅ | `ATK-AUTH-CSRF-001` |
| Output Encoding | ✅ | `DEF-PREVENT-OUTPUTENC-001` |
| CSP | ✅ | `DEF-PREVENT-CSP-001` |
| OWASP Top 10 | ❌ | |
| CWE | ❌ | |
| **Same-Origin Policy (SOP)** | ❌ | XSS의 핵심 — SOP 우회가 본질 |
| **HttpOnly / Secure 플래그** | ❌ | 쿠키 보안 속성 |
| **DOM Sink/Source 모델** | ❌ | DOM XSS 이해에 필수 |
| **Event Handler (JS)** | ❌ | XSS 페이로드의 핵심 벡터 |
| **Content-Type / MIME** | ❌ | 브라우저 렌더링 판단 기준 |
| **innerHTML / document.write** | ❌ | DOM XSS의 위험 API |
| URL 구조 | ❌ | Reflected XSS 벡터 |
| HTML Encoding/Entity | ❌ | 방어의 핵심 메커니즘 |
| **X-XSS-Protection 헤더** | ❌ | (deprecated지만 개념적 의미) |

### 누락 요약: **11개** (SOP, HttpOnly, DOM Sink, Event Handler, MIME, innerHTML, URL, HTML Encoding 등)

---

## 시드 3: Kerberoasting (ATK-WIN-KERBEROASTING-001) — AD 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Kerberos Protocol | ✅ | `TECH-PROTOCOL-KERBEROS-001` / `INFRA-KERBEROS-001` |
| Active Directory | ✅ | `INFRA-AD-001` / `TECH-CONCEPT-AD-SECURITY-001` |
| LDAP | ✅ | `TECH-PROTOCOL-LDAP-001` / `INFRA-LDAP-001` |
| Credential Access | ✅ | `ATK-MITRE-CREDENTIAL-001` |
| Mimikatz | ✅ | `TOOL-PENTEST-MIMIKATZ-001` |
| Rubeus | ✅ | `TOOL-PENTEST-RUBEUS-001` |
| Hashcat | ✅ | `TOOL-PENTEST-HASHCAT-001` |
| Impacket | ✅ | `TOOL-PENTEST-IMPACKET-001` |
| **SPN (Service Principal Name)** | ❌ | Kerberoasting의 핵심 전제 |
| **TGT (Ticket Granting Ticket)** | ❌ | Kerberos 인증 흐름 핵심 |
| **TGS (Ticket Granting Service)** | ❌ | 서비스 티켓 발급 |
| **KDC (Key Distribution Center)** | ❌ | Kerberos 아키텍처 핵심 |
| **RC4 vs AES 암호화** | ❌ | 왜 RC4 티켓이 크래킹 가능한지 |
| **Service Account** | ❌ | 타겟 계정 유형 |
| **gMSA (Group Managed Service Account)** | ❌ | 핵심 방어 메커니즘 |
| **Password Hash / Hash Cracking** | ❌ | 오프라인 크래킹 개념 |
| **Windows Event Log (4769)** | ❌ | 탐지 메커니즘 |
| **Domain Controller** | ❌ | AD 인프라 핵심 |
| **PowerShell** | ❌ | 공격/관리 도구 |
| **WMI** | ❌ | 관리 인터페이스 |

### 누락 요약: **11개** (SPN, TGT/TGS, KDC, RC4/AES, Service Account, gMSA, Password Hash, Domain Controller, PowerShell, WMI 등)

---

## 시드 4: SSRF (ATK-SERVER-SSRF-001) — 서버측 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| HTTP | ✅ | `TECH-PROTOCOL-HTTP-001` |
| Web Application | ✅ | `INFRA-APP-WEBAPP-001` |
| API | ✅ | `INFRA-APP-API-001` |
| Cloud Metadata | ✅ | `ATK-CLOUD-METADATA-001` (공격) |
| AWS S3 | ✅ | `INFRA-CLOUD-AWS-S3-001` |
| Cloud IAM | ✅ | `INFRA-CLOUD-IAM-001` |
| DNS | ✅ | `TECH-PROTOCOL-DNS-001` |
| OWASP Top 10 | ❌ | |
| CWE | ❌ | |
| **Internal Network / Private IP** | ❌ | 10.x, 172.16.x, 192.168.x 개념 |
| **Cloud Metadata API (169.254.169.254)** | ❌ | SSRF 핵심 타겟 (인프라 개념) |
| **URL Parser / SSRF Bypass** | ❌ | IP 표기법 변환, DNS Rebinding |
| **Reverse Proxy** | ❌ | 서버 배치 아키텍처 |
| **Webhook** | ❌ | SSRF 발생 빈번 지점 |
| **DNS Rebinding** | ❌ | SSRF 우회 기법 |
| **IMDS v1 vs v2** | ❌ | AWS 메타데이터 보안 진화 |
| URL 구조 | ❌ | (XSS와 공유) |
| IP 표기법 (Hex/Octal/Decimal) | ❌ | SSRF 우회 기법 |

### 누락 요약: **10개** (Private IP, Metadata API 개념, URL Parser, Reverse Proxy, Webhook, DNS Rebinding, IMDS v1/v2 등)

---

## 시드 5: Container Escape (ATK-CONTAINER-ESCAPE-001) — 컨테이너 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Docker | ✅ | `INFRA-CONTAINER-DOCKER-001` |
| Kubernetes | ✅ | `INFRA-RUNTIME-K8S-001` / `INFRA-CONTAINER-K8S-001` |
| Container Runtime | ✅ | `INFRA-RUNTIME-CONTAINER-001` |
| Privilege Escalation | ✅ | `ATK-PRIVILEGE-ESCALATION-001` |
| Container Security (Falco) | ✅ | `TOOL-CONTAINER-FALCO-001` |
| K8s Network Policy | ✅ | `DEF-K8S-NETWORK-POLICY-001` |
| **Linux Namespace** | ❌ | 컨테이너 격리의 기반 기술 |
| **Linux Cgroup** | ❌ | 리소스 격리 |
| **Linux Capabilities** | ❌ | SYS_ADMIN, SYS_PTRACE 등 |
| **Seccomp** | ❌ | 시스템 콜 필터링 |
| **AppArmor / SELinux** | ❌ | 필수 접근 제어 |
| **Docker Socket** | ❌ | /var/run/docker.sock — 핵심 탈출 벡터 |
| **Privileged Mode** | ❌ | --privileged 플래그의 의미 |
| **Container Image** | ❌ | 이미지 빌드/보안 개념 |
| **Host Mount / Volume** | ❌ | 호스트 파일시스템 접근 |
| **OCI Runtime (runc, containerd)** | ❌ | 컨테이너 실행 엔진 |
| **Linux Kernel (보안 관점)** | ❌ | 커널 취약점 = 탈출 |
| **Process Isolation** | ❌ | |

### 누락 요약: **12개** (Namespace, Cgroup, Capabilities, Seccomp, AppArmor, Docker Socket, Privileged Mode, Container Image, Volume, OCI Runtime, Kernel, Process Isolation)

---

## 시드 6: Ransomware (ATK-MALWARE-RANSOMWARE-001) — 맬웨어

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Lateral Movement | ✅ | `ATK-MITRE-LATERAL-001` / `ATK-LATERAL-001` |
| Persistence | ✅ | `ATK-MITRE-PERSISTENCE-001` |
| Phishing | ✅ | `ATK-SOCIAL-PHISHING-001` |
| Backup | ✅ | `DEF-BACKUP-001` / `TECH-BACKUP-001` |
| EDR | ✅ | `TOOL-DEFENSE-EDR-001` / `DEF-ENDPOINT-EDR-001` |
| Network Segmentation | ✅ | `DEF-NET-SEGMENTATION-001` |
| Incident Response | ✅ | `DEF-RESPOND-INCIDENT-001` |
| PAM | ✅ | `DEF-AUTH-PAM-001` |
| **암호화 (대칭/비대칭)** | ❌ | 랜섬웨어 동작 원리 (AES+RSA) |
| **암호화폐 (Bitcoin/Monero)** | ❌ | 몸값 결제 수단 |
| **C2 (Command & Control) 채널** | 🔶 | `ATK-MITRE-C2-001` 있으나 인프라 개념 없음 |
| **RDP (Remote Desktop)** | ❌ | 주요 초기 접근 벡터 |
| **Volume Shadow Copy** | ❌ | 랜섬웨어가 삭제하는 핵심 타겟 |
| **3-2-1 백업 규칙** | ❌ | 방어 전략의 핵심 |
| **Double Extortion** | ❌ | 현대 랜섬웨어의 핵심 전술 |
| **Ransomware-as-a-Service (RaaS)** | ❌ | 비즈니스 모델 |
| **Kill Chain / Attack Lifecycle** | ❌ | 단계별 방어 프레임워크 |
| **IOC (Indicator of Compromise)** | ❌ | 탐지 지표 |

### 누락 요약: **10개** (암호화 메커니즘, 암호화폐, RDP, VSS, 3-2-1, Double Extortion, RaaS, Kill Chain, IOC 등)

---

## 시드 7: Phishing (ATK-SOCIAL-PHISHING-001) — 사회공학

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| SMTP | ✅ | `TECH-PROTOCOL-SMTP-001` |
| Security Awareness | ✅ | `DEF-AWARENESS-001` |
| MFA | ✅ | `DEF-PREVENT-MFA-001` / `DEF-AUTH-MFA-001` |
| Email Security | ✅ | `DEF-EMAIL-SECURITY-001` |
| Credential Stuffing | ✅ | `ATK-AUTH-CREDSTUFF-001` |
| **SPF (Sender Policy Framework)** | ❌ | 이메일 인증 핵심 |
| **DKIM (DomainKeys)** | ❌ | 이메일 무결성 검증 |
| **DMARC** | ❌ | SPF+DKIM 정책 |
| **Domain Spoofing** | ❌ | 발신자 위장 기법 |
| **Typosquatting/Homoglyph** | 🔶 | `ATK-SUPPLY-TYPOSQUAT-001` (공급망 관점) |
| **MX Record** | ❌ | 이메일 라우팅 |
| **URL Shortener (보안 관점)** | ❌ | 피싱 링크 은닉 |
| **사회공학 심리 기법** | ❌ | 긴급성, 권위, 호기심 등 |
| **Attachment/Macro 악성코드** | ❌ | 피싱 페이로드 유형 |
| **Phishing Kit** | ❌ | 피싱 페이지 자동 생성 도구 |
| **OAuth Consent Phishing** | ❌ | 현대 피싱 기법 |

### 누락 요약: **11개** (SPF, DKIM, DMARC, Domain Spoofing, MX Record, URL Shortener, 사회공학 심리, Macro, Phishing Kit, OAuth Phishing 등)

---

## 시드 8: DNS Spoofing (ATK-NET-DNSSPOOF-001) — 네트워크 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| DNS | ✅ | `TECH-PROTOCOL-DNS-001` / `INFRA-NET-DNS-001` |
| ARP Spoofing | ✅ | `ATK-NET-ARP-SPOOFING-001` |
| MITM | ✅ | `ATK-NET-MITM-001` |
| TLS/HTTPS | ✅ | `DEF-CRYPTO-TLS-001` / `TECH-PROTOCOL-TLS-001` |
| **DNSSEC** | ❌ | DNS 보안 확장 (핵심 방어) |
| **DNS 캐시/TTL** | ❌ | Cache Poisoning의 전제 |
| **DNS Record Types (A/AAAA/CNAME/MX/NS)** | ❌ | DNS 기본 구조 |
| **DNS Resolver vs Authoritative** | ❌ | DNS 아키텍처 |
| **Kaminsky Attack** | ❌ | 대표적 DNS 캐시 포이즈닝 |
| **DNS over HTTPS/TLS (DoH/DoT)** | ❌ | 현대 DNS 보안 |
| **ARP (Address Resolution Protocol)** | ❌ | ARP Spoofing 전제 |
| IP Address / Subnet | ⛔ | 일반 네트워크 기초 |

### 누락 요약: **7개** (DNSSEC, DNS 캐시/TTL, Record Types, Resolver/Auth, Kaminsky, DoH/DoT, ARP 프로토콜)

---

## 시드 9: DDoS (ATK-NET-DDOS-001) — 가용성 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Network Infrastructure | ✅ | `INFRA-NET-NETWORK-001` |
| Web Server | ✅ | `INFRA-APP-WEBSERVER-001` |
| Rate Limiting | ✅ | `DEF-PREVENT-RATELIMIT-001` |
| CDN | ✅ | `INFRA-NET-CDN-001` |
| Load Balancer | ✅ | `INFRA-NET-LB-001` |
| Botnet | ✅ | `ATK-MALWARE-BOTNET-001` |
| BGP Hijacking | ✅ | `ATK-NET-BGP-HIJACK-001` |
| SYN Flood | ✅ | `ATK-NET-SYN-FLOOD-001` |
| **TCP 3-Way Handshake** | ❌ | SYN Flood 이해에 필수 |
| **UDP Protocol** | ❌ | UDP Flood, Amplification 전제 |
| **NTP Protocol (보안 관점)** | ❌ | NTP Amplification (556x) |
| **DNS Amplification** | ❌ | 대표적 증폭 공격 |
| **Memcached Amplification** | ❌ | 51,000x 증폭 |
| **Anycast** | ❌ | DDoS 방어 핵심 기술 |
| **Traffic Scrubbing** | ❌ | DDoS 완화 서비스 |
| **BGP Blackholing** | ❌ | 긴급 DDoS 완화 |
| **Slowloris / Slow HTTP** | ❌ | Application Layer DDoS |
| **Bandwidth / Throughput** | ⛔ | 일반 네트워크 |

### 누락 요약: **9개** (TCP Handshake, UDP, NTP/DNS/Memcached Amplification, Anycast, Traffic Scrubbing, BGP Blackholing, Slowloris)

---

## 시드 10: Cloud IAM Misconfiguration (VUL-CLOUD-IAM-001) — 클라우드

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| Cloud Infrastructure | ✅ | `INFRA-CLOUD-001` |
| AWS IAM | ✅ | `INFRA-CLOUD-AWS-IAM-001` |
| GCP IAM | ✅ | `INFRA-CLOUD-GCP-IAM-001` |
| Azure AD | ✅ | `INFRA-CLOUD-AZURE-AD-001` |
| Security Misconfiguration | ✅ | `VUL-CONFIG-MISCONFIG-001` |
| Least Privilege | ✅ | `GR-SEC-PRI-LEAST-PRIVILEGE-001` |
| Cloud Posture (CSPM) | ✅ | `DEF-CLOUD-POSTURE-001` |
| CIEM | ✅ | `DEF-CLOUD-CIEM-001` |
| Prowler | ✅ | `TOOL-CLOUD-PROWLER-001` |
| **IAM Policy Language (JSON)** | ❌ | AWS IAM 정책 구조 |
| **RBAC vs ABAC** | ❌ | 접근 제어 모델 |
| **Service Account / Service Principal** | ❌ | 클라우드 머신 ID |
| **Access Key / Secret Key** | ❌ | 프로그래밍 방식 인증 |
| **AssumeRole / Cross-Account** | ❌ | AWS 역할 전환 메커니즘 |
| **Shared Responsibility Model** | ❌ | 클라우드 보안 근본 개념 |
| **Condition Key (IAM)** | ❌ | 세분화된 접근 제어 |
| **Cloud Trail / Audit Log** | ❌ | 감사 추적 |

### 누락 요약: **7개** (IAM Policy, RBAC/ABAC, Service Account, Access Key, AssumeRole, Shared Responsibility, Cloud Audit)

---

## 시드 11: Insecure Deserialization (ATK-SERVER-DESER-001) — 앱 공격

### Level 1 필요 개념
| 개념 | KB 상태 | 비고 |
|------|---------|------|
| RCE | ✅ | `VUL-WEB-RCE-001` |
| Command Injection | ✅ | `ATK-INJECT-CMD-001` |
| API | ✅ | `INFRA-APP-API-001` |
| OWASP Top 10 | ❌ | |
| CWE | ❌ | |
| **Serialization/Deserialization 개념** | ❌ | 직렬화가 뭔지 |
| **Gadget Chain** | ❌ | 역직렬화 공격의 핵심 |
| **Java ClassLoader / Reflection** | ❌ | Java 역직렬화 메커니즘 |
| **Magic Bytes / File Signature** | ❌ | rO0AB, aced0005 식별 |
| **Object Injection (PHP)** | ❌ | PHP __wakeup, __destruct |
| **Python Pickle** | ❌ | __reduce__ 메서드 |
| **JSON vs Binary Serialization** | ❌ | 안전한 대안 이해 |
| **HMAC 무결성 검증** | ❌ | 방어 메커니즘 |
| **ysoserial / PHPGGC** | 🔶 | 언급되나 전용 원자 없음 |
| **Application Server (WAS)** | ✅ | `INFRA-APP-WAS-TOMCAT-001` 등 |

### 누락 요약: **9개** (Serialization 개념, Gadget Chain, Java Reflection, Magic Bytes, PHP Object Injection, Pickle, JSON vs Binary, HMAC, 도구)

---

## 📊 전체 종합 통계

### 시드별 누락 수
| # | 시드 | 카테고리 | 누락 수 |
|---|------|----------|---------|
| 1 | SQL Injection | 웹 인젝션 | ~50 (TODO 포함) |
| 2 | XSS | 웹 클라이언트 | 11 |
| 3 | Kerberoasting | AD/Windows | 11 |
| 4 | SSRF | 웹 서버측 | 10 |
| 5 | Container Escape | 컨테이너 | 12 |
| 6 | Ransomware | 맬웨어 | 10 |
| 7 | Phishing | 사회공학 | 11 |
| 8 | DNS Spoofing | 네트워크 | 7 |
| 9 | DDoS | 네트워크 가용성 | 9 |
| 10 | Cloud IAM | 클라우드 | 7 |
| 11 | Deserialization | 앱 | 9 |
| | **합계 (원시)** | | **~147** |

### 🔄 개념 공유 분석 (중복 제거)

여러 시드에서 **공통으로 누락**된 개념:

| 공유 개념 | 필요 시드 | 우선순위 |
|-----------|-----------|----------|
| **OWASP Top 10** | SQLi, XSS, SSRF, Deser | ★★★ |
| **CWE** | SQLi, XSS, SSRF, Deser | ★★★ |
| **CVSS** | SQLi + 전체 | ★★★ |
| **CVE** | SQLi + 전체 | ★★★ |
| **URL 구조/파라미터** | SQLi, XSS, SSRF | ★★★ |
| **HTTP Methods** | SQLi, XSS, SSRF | ★★☆ |
| **HTTP Header 개념** | SQLi, XSS | ★★☆ |
| **인코딩 (URL/Base64)** | SQLi, SSRF, XSS | ★★☆ |
| **Reverse Proxy** | SQLi(WAF), SSRF, DDoS | ★★☆ |
| **Private IP / Subnet** | SSRF, Container, Network | ★★☆ |
| **Service Account** | Kerberos, Cloud IAM | ★★☆ |
| **RBAC/ABAC** | K8s RBAC, Cloud IAM | ★★☆ |
| **Password Hash/Cracking** | Kerberos, Brute Force | ★★☆ |
| **RDP** | Ransomware, Lateral | ★★☆ |
| **Kill Chain / Attack Lifecycle** | Ransomware + 전체 | ★★☆ |
| **IOC** | Ransomware + 전체 | ★★☆ |
| **암호화 (대칭/비대칭)** | Ransomware, TLS, Kerberos | ★★☆ |

### 중복 제거 후 실제 누락 추정

| 카테고리 | 수량 |
|----------|------|
| 원시 합계 | ~147 |
| 공유 개념 중복 | ~25 |
| **실제 고유 누락** | **~120개** |
| 이 중 ★★★ 필수급 | **~35개** |
| 이 중 ★★☆ 권장급 | **~50개** |
| 이 중 ★☆☆ 선택급 | **~35개** |

---

## 🏗️ 누락 개념 분류 (유형별)

### A. 보안 표준/프레임워크 (없으면 안 되는 것)
| 개념 | 참조 빈도 |
|------|-----------|
| OWASP Top 10 | 거의 전체 웹 원자 |
| CWE (Common Weakness Enumeration) | 거의 전체 원자 |
| CVE (Common Vulnerabilities) | 전체 |
| CVSS (Scoring System) | 전체 |
| NVD | 전체 |
| Cyber Kill Chain / MITRE ATT&CK Lifecycle | 전체 |
| IOC (Indicator of Compromise) | 전체 |

### B. 프로토콜/인프라 구성요소 (인프라 원자 후보)
| 개념 | 카테고리 |
|------|----------|
| MySQL, PostgreSQL, MSSQL, Oracle | DB 인프라 |
| RDP (Remote Desktop) | 원격 접속 |
| Domain Controller | AD 인프라 |
| NTP Server | 네트워크 인프라 |
| Reverse Proxy | 웹 인프라 |
| MongoDB / NoSQL DB | DB 인프라 |
| OCI Runtime (runc, containerd) | 컨테이너 인프라 |

### C. 보안 메커니즘/개념 (knowledge 원자 후보)
| 개념 | 카테고리 |
|------|----------|
| Same-Origin Policy (SOP) | 브라우저 보안 |
| DNSSEC | DNS 보안 |
| SPF/DKIM/DMARC | 이메일 보안 |
| Serialization/Deserialization | 앱 보안 |
| Linux Namespace/Cgroup/Capabilities | 컨테이너 보안 |
| Kerberos TGT/TGS/KDC/SPN | AD 보안 |
| RBAC/ABAC | 접근 제어 |
| Shared Responsibility Model | 클라우드 보안 |
| Gadget Chain | 역직렬화 |
| Double Extortion / RaaS | 랜섬웨어 |

### D. 기술 기초 (보안 맥락 포함)
| 개념 | 보안 맥락 |
|------|-----------|
| TCP 3-Way Handshake | SYN Flood |
| UDP Protocol | DDoS Amplification |
| URL 구조 | XSS, SSRF 벡터 |
| HTTP Methods | 웹 공격 전반 |
| 인코딩 (URL/Base64) | WAF 우회 |
| Password Hash / Cracking | 인증 공격 |
| 암호화 (대칭/비대칭) | 랜섬/TLS/Kerberos |

---

## 🎯 최종 결론

### 1. 방법론 검증 ✅
- **재귀 깊이 2단계면 충분** — 10개 시드 모두에서 확인
- **경계선 "보안에서 독립 설명 필요한가?"가 작동**
- **개념 공유 효과 실제 존재** — 147개 원시 → 120개 실제

### 2. 규모 예측
- 10개 시드 → ~120개 누락
- 전체 KB 시드 (~270개 technique/attack) → **추정 300~500개 누락**
  - 공유 효과가 갈수록 커지므로 선형 증가 아님
  - 실제 작업량은 관리 가능한 수준

### 3. 가장 시급한 누락 (전체 공통)
1. **OWASP, CWE, CVE, CVSS** — 보안의 공통 언어, 전체 원자가 참조
2. **주요 DB 컴포넌트** (MySQL, PostgreSQL, MSSQL) — 이미 TODO로 약속
3. **프로토콜 세부** (SPN/TGT/TGS, DNSSEC, SPF/DKIM/DMARC)
4. **리눅스 보안 기초** (Namespace, Cgroup, Capabilities)
5. **브라우저 보안 모델** (SOP, CORS, CSP 관계)

### 4. 권장 다음 단계
1. **경계 규칙 확정** → 위 결과를 바탕으로 Depth 2 + "보안 독립 설명" 기준
2. **전체 KB 자동 분해** → 스크립트로 모든 technique/attack 원자 분석
3. **누락 원자 생성** → ★★★ 필수급 35개부터 시작
4. **공유 개념 우선** → OWASP, CWE 같은 고빈도 공유 개념 먼저

---

*2026-02-05 생성 — 10개 시드 종합 분석*
*시드: SQLi, XSS, Kerberoasting, SSRF, Container Escape, Ransomware, Phishing, DNS Spoofing, DDoS, Cloud IAM, Deserialization*
