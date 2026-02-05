# GR 온톨로지 AI 에이전트 가이드
> **Version**: 1.0 | **Date**: 2026-02-05
> 
> 이 문서를 읽는 AI 에이전트는 이 가이드만으로 GR 온톨로지의 원자(Atom)를
> **동일한 기준으로 분류, 작성, 검증**할 수 있어야 합니다.
> 
> ⚠️ **이 문서가 최상위 권위입니다.** 다른 문서와 충돌 시 이 문서를 따르세요.

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [핵심 개념](#2-핵심-개념)
3. [원자(Atom) 구조](#3-원자atom-구조)
4. [분류 결정 트리](#4-분류-결정-트리)
5. [3D 좌표계](#5-3d-좌표계)
6. [atom_tags 배정 규칙](#6-atom_tags-배정-규칙)
7. [관계(Relations) 규칙](#7-관계relations-규칙)
8. [파일 명명 및 디렉토리](#8-파일-명명-및-디렉토리)
9. [완성 예시 (3가지)](#9-완성-예시)
10. [검증 체크리스트](#10-검증-체크리스트)
11. [금지 사항](#11-금지-사항)
12. [참조 파일 목록](#12-참조-파일-목록)

---

## 1. 프로젝트 개요

### 1.1 GR 온톨로지란?

GR(Gotroot) 온톨로지는 **보안 지식을 원자(Atom) 단위로 분해**하여 3D 좌표계에 배치하는 시스템입니다.

**핵심 차별점**: MITRE ATT&CK가 "WHAT(무엇을)" + "HOW(어떻게)"를 다룬다면, GR은 여기에 **"WHERE(어디서)"**를 추가합니다.

```
MITRE ATT&CK: 공격자가 [SQL Injection]을 [사용자 입력으로] 수행
GR 온톨로지:  공격자가 [SQL Injection]을 [L7-Z2-A2.1 위치의 API 서버에서] 수행
```

### 1.2 설계 원칙

| 원칙 | 설명 |
|------|------|
| **결정론적 분류** | 같은 입력 → 항상 같은 분류 결과 |
| **모호성 불허** | 판단이 애매하면 규칙이 불완전한 것 |
| **원자성** | 하나의 원자 = 하나의 독립적 지식 단위 |
| **좌표 기반** | 모든 인프라 원자는 3D 좌표를 가짐 |

### 1.3 저장소 구조

```
GR_project_v3/
├── 00_docs/                    # 문서 (이 가이드 포함)
├── 01_vision/                  # 비전, 마스터플랜
├── 02_framework/               # 3D 프레임워크 상세
│   └── GR_DB/
│       ├── 01_차원1_Deployment_Layer/
│       ├── 02_차원2_Security_Zone/
│       └── 03_차원3_Function/
├── 03_ontology/                # 온톨로지 정의
│   ├── constitution/           # 헌법 (최고 규범)
│   ├── guides/                 # 분류 규칙
│   ├── schema/core/            # atom_schema.yaml, relation_types.yaml
│   └── taxonomy/               # atom_tags.yaml, layers.yaml, zones.yaml
├── 04_knowledge_base/          # 지식 베이스
│   ├── atom_data/              # ★ 완성된 원자 파일들
│   │   ├── attacks/
│   │   ├── defenses/
│   │   ├── concepts/
│   │   ├── compliance/
│   │   ├── infrastructure/
│   │   ├── technology/
│   │   ├── tools/
│   │   └── vulnerabilities/
│   ├── list_onlyName/          # 이름만 있는 리스트
│   └── rawdata_pre_atom/       # 원자화 전 원시 데이터
├── 06_applications/            # Atlas 등 응용
└── 07_raw_sources/             # 외부 소스 (Sigma 룰 등)
```

---

## 2. 핵심 개념

### 2.1 원자(Atom)

온톨로지의 최소 지식 단위. 하나의 YAML 파일 = 하나의 원자.

### 2.2 인프라 vs 지식

GR 온톨로지의 **가장 중요한 이분법**:

| 구분 | 인프라 원자 | 지식 원자 |
|------|-----------|----------|
| `is_infrastructure` | `true` | `false` |
| 의미 | 배포 가능한 실체 | 개념/기법/정책 등 지식 |
| ID prefix | `INFRA-*` 만 | 나머지 전부 |
| 3D 좌표 | `gr_coordinates` 사용 | `scope` 사용 |
| Function 코드 | 필수 (단일 값) | 없음 |
| 예시 | WAF 장비, DB 서버, K8s | SQL Injection, Zero Trust, NIST |

### 2.3 is_infrastructure 판정 (4-Question Test)

아래 4개 질문 중 **하나라도 Yes**이면 `is_infrastructure: true`:

1. **네트워크 주소**를 가질 수 있는가? (IP, hostname)
2. **프로세스**로 실행될 수 있는가? (PID)
3. **물리적 형태**가 있을 수 있는가? (하드웨어)
4. **시스템 자원**을 소비하는가? (CPU, 메모리, 디스크)

> ⚠️ **주의**: 이 테스트는 참고용입니다. 실제 분류에서는 **Prefix 규칙이 우선**합니다.
> `INFRA-*` = true, 그 외 = false. 이 규칙은 예외 없이 절대적입니다.

---

## 3. 원자(Atom) 구조

### 3.1 필수 필드 요약

```yaml
# ── 식별 ──
identity:
  id: "PREFIX-CATEGORY-NAME-SEQ"     # 필수, 불변
  name: "Human Readable Name"        # 필수
  normalization:
    normalized_name: "lowercase no special chars"  # 필수 (시스템 생성 가능)
    normalization_version: "1.0"     # 필수
  aliases: []                        # 선택

# ── 분류 ──
classification:
  domain: security                   # 필수 (enum)
  type: technique                    # 필수 (enum, 아래 표 참조)
  is_infrastructure: false           # 필수 (prefix로 결정)
  abstraction_level: 2               # 필수 (1-4)
  gr_coordinates:                    # is_infrastructure: true일 때만
    layer: "L7"
    zone: "Z1"
    function: "S1.1"
    atom_tags: [...]                 # 필수 (모든 원자)
  scope:                             # is_infrastructure: false일 때만
    target_layers: ["L7"]
    target_zones: ["Z2"]
    target_functions: ["A2"]         # 선택

# ── 정의 ──
definition:
  what: "..."                        # 필수
  why: "..."                         # 선택
  how: "..."                         # 선택

# ── 관계 ──
relations:                           # 필수 (빈 객체 허용)
  structural: {}
  causal: {}
  conditional: {}
  applicability: {}

# ── 메타데이터 ──
metadata:
  trust:
    source: official                 # 필수
    confidence: 1.0                  # 필수
  temporal:
    created: 2026-02-05              # 필수
    modified: 2026-02-05             # 필수
    revision: 1                      # 필수
  security:
    sensitivity: public              # 필수
  ai:
    embedding_text: "..."            # 필수
    search_keywords: [...]           # 필수 (5개 이상)
```

### 3.2 domain 값

```yaml
values: [security, network, system, application, data, cloud, iot, ai]
```

대부분의 보안 원자는 `security`입니다. 특정 기술 영역에 집중된 원자만 다른 값을 사용합니다.

### 3.3 type 전체 목록 (11개)

#### 인프라 type (is_infrastructure: true, INFRA-* only)

| type | 의미 | 예시 |
|------|------|------|
| `component` | 핵심 인프라 구성요소 | 서버, DB, 라우터, VM |
| `component_tool` | 배포된 운영/보안 도구 | SIEM 인스턴스, EDR 에이전트 |
| `component_control` | 배포된 보안 통제 장치 | WAF 어플라이언스, IDS/IPS, 방화벽 |

#### 지식 type (is_infrastructure: false)

| type | 의미 | 예시 |
|------|------|------|
| `concept` | 개념, 사상, 카테고리 | Zero Trust, Network Attack, Blue Team |
| `technique` | 공격/방어 기법 | SQL Injection, Phishing, Port Scanning |
| `vulnerability` | 취약점 | CWE-89, Broken Authentication |
| `principle` | 보안 원칙/철학 | Least Privilege, Defense in Depth |
| `pattern` | 시그니처, 페이로드 | SQLi payload, DBMS fingerprint |
| `protocol` | 통신 프로토콜/표준 | HTTP, TLS, OAuth, LDAP |
| `tool_knowledge` | 도구 지식 (사용법) | Metasploit 가이드, Burp Suite 기능 |
| `control_policy` | 정책/절차/규정 | 접근통제 정책, NIST CSF, GDPR |

### 3.4 abstraction_level

| 레벨 | 의미 | 예시 |
|------|------|------|
| 1 | 인스턴스 (가장 구체적) | `' OR 1=1--` 페이로드, 특정 CVE |
| 2 | 기법/도구 (실행 가능) | SQL Injection, WAF, Nmap |
| 3 | 개념 (분류/카테고리) | Injection, Network Security |
| 4 | 원리 (가장 추상적) | Least Privilege, Defense in Depth |

---

## 4. 분류 결정 트리

### 4.1 Step 1: ID Prefix 결정

이것이 **가장 먼저** 결정해야 할 사항입니다.

```
                    원자의 본질은?
                        │
    ┌───────┬───────┬───┴───┬───────┬───────┬───────┐
    │       │       │       │       │       │       │
  공격?   방어?   취약점? 도구지식? 인프라?  규정?   기타?
    │       │       │       │       │       │       │
  ATK-    DEF-    VUL-    TOOL-   INFRA-  COMP-   TECH-
```

**판별 질문 (순서대로 적용)**:

| 순서 | 질문 | Yes → Prefix |
|------|------|-------------|
| 1 | 물리적/가상 인프라 구성요소인가? (배포 가능한 실체) | `INFRA-` |
| 2 | 공격 기법인가? (악의적 행위, 공격 방법론) | `ATK-` |
| 3 | 취약점인가? (시스템의 약점, CWE/CVE) | `VUL-` |
| 4 | 방어 정책/절차/통제인가? (보호, 탐지, 대응) | `DEF-` |
| 5 | 보안 도구의 사용법/지식인가? (도구 자체가 아닌 사용 지식) | `TOOL-` |
| 6 | 규정/프레임워크인가? (법규, 표준, 컴플라이언스) | `COMP-` |
| 7 | 위 어디에도 해당하지 않는 기술 개념 | `TECH-` |

> **핵심 구분**: "이것을 서버에 **설치**할 수 있는가?" → Yes: `INFRA-`, No: 지식 원자

### 4.2 Step 2: type 결정

#### 4.2.1 INFRA-* 원자 (is_infrastructure: true)

```
INFRA-* 원자의 주 목적은?
         │
    ┌────┴────┬──────────────┐
    │         │              │
  보안 통제?  보안/운영 도구?  그 외?
  (차단/탐지)  (분석/스캔)     (범용)
    │         │              │
component_  component_    component
control     tool
```

| 질문 | Yes → type |
|------|-----------|
| 주 목적이 보안 통제(차단/탐지/방지)인가? | `component_control` |
| 주 목적이 보안/운영 도구(분석/스캔/모니터링)인가? | `component_tool` |
| 그 외 인프라 구성요소인가? | `component` |

**예시**:
- WAF → `component_control` (웹 공격 차단이 주 목적)
- SIEM → `component_tool` (로그 분석/모니터링이 주 목적)
- PostgreSQL → `component` (데이터 저장이 주 목적)
- IDS/IPS → `component_control` (침입 탐지/방지가 주 목적)
- Nginx → `component` (웹 서빙/프록시가 주 목적)

#### 4.2.2 ATK-* 원자

```
ATK-* 원자가 구체적인 공격 기법인가?
         │
    ┌────┴────┐
    │         │
  구체적     카테고리
  (실행 가능) (분류/그룹)
    │         │
 technique   concept
```

- "SQL Injection" → `technique` (실행 가능한 구체적 기법)
- "Network Attack" → `concept` (여러 기법을 포함하는 상위 분류)
- "Collection (TA0009)" → `concept` (MITRE Tactic = 카테고리)

#### 4.2.3 DEF-* 원자

```
DEF-* 원자가 구체적인 방어 수단인가?
         │
    ┌────┴────┐
    │         │
  구체적      카테고리
  (적용 가능)  (분류/그룹)
    │         │
control_     concept
policy
```

- "Rate Limiting" → `control_policy` (구체적으로 적용 가능)
- "Email Defense" → `concept` (방어 전략의 상위 분류)
- "Input Validation" → `control_policy` (구체적 방어 절차)

#### 4.2.4 VUL-* 원자

```
VUL-* 원자가 구체적인 취약점인가?
         │
    ┌────┴────┐
    │         │
  구체적      카테고리
    │         │
vulnerability concept
```

- "SQL Injection Vulnerability" → `vulnerability`
- "Authentication Issues" → `concept` (취약점 카테고리)

#### 4.2.5 TOOL-* 원자

```
TOOL-* 원자가 구체적인 도구 지식인가?
         │
    ┌────┴────┐
    │         │
  구체적      카테고리
  (특정 도구)  (도구 그룹)
    │         │
tool_        concept
knowledge
```

- "Metasploit Framework" → `tool_knowledge` (구체적 도구)
- "Scanning Tools" → `concept` (도구 카테고리)

#### 4.2.6 COMP-* 원자

```
COMP-* 원자가 구체적인 규정/프레임워크인가?
         │
    ┌────┴────┐
    │         │
  구체적      카테고리
  (특정 규정)  (규정 그룹)
    │         │
control_     concept
policy
```

- "NIST CSF" → `control_policy` (구체적 프레임워크)
- "Industry Standards" → `concept` (규정 카테고리)

#### 4.2.7 TECH-* 원자

| 원자의 성격 | type |
|------------|------|
| 보안 원칙/철학 | `principle` |
| 통신 프로토콜/표준 | `protocol` |
| 시그니처/페이로드/패턴 | `pattern` |
| 기술 개념/이론 | `concept` |

### 4.3 Step 3: "카테고리" vs "구체적" 판별법

이 판별은 ATK, DEF, VUL, TOOL, COMP prefix에서 사용됩니다.

**3-Question Test** (순서대로):

| # | 질문 | Yes | No |
|---|------|-----|-----|
| 1 | 이것을 "실행"하거나 "적용"할 수 있는가? | → 구체적 (기본 type) | → 질문 2 |
| 2 | 이것은 다른 원자들을 "포함"하는 상위 분류인가? | → `concept` | → 질문 3 |
| 3 | 이것을 한 문장으로 구체적으로 설명할 수 있는가? | → 구체적 (기본 type) | → `concept` |

---

## 5. 3D 좌표계

### 5.1 개요

GR 3D 좌표계는 **인프라 원자(INFRA-*)에만 적용**됩니다.

```
3D 좌표 = Layer(수직) × Zone(수평) × Function(기능)
```

지식 원자(나머지)는 3D 좌표 대신 `scope`(적용 범위)를 사용합니다.

### 5.2 차원 1: Layer (수직 추상화)

| Layer | 이름 | 설명 | 예시 |
|-------|------|------|------|
| `L0` | External | 외부 환경 | 인터넷, 외부 API |
| `L1` | Physical | 물리적 인프라 | 하드웨어, 데이터센터 |
| `L2` | Network | 네트워크 | 라우터, 스위치, 방화벽 |
| `L3` | Compute | 컴퓨팅/OS | Linux, Windows, VM |
| `L4` | Platform | 플랫폼/미들웨어 | 웹 서버, WAS, K8s |
| `L5` | Data | 데이터 | RDBMS, NoSQL, 스토리지 |
| `L6` | Runtime | 런타임 | JVM, Node.js, .NET |
| `L7` | Application | 애플리케이션 | 웹앱, API, 마이크로서비스 |
| `Cross` | Cross-Layer | 여러 계층 관통 | IAM, 로깅, CI/CD |

**Layer 결정 질문**: "이 구성요소는 인프라 스택의 어느 높이에서 동작하는가?"

### 5.3 차원 2: Zone (수평 신뢰 경계)

| Zone | 이름 | 신뢰도 | 설명 | 예시 |
|------|------|--------|------|------|
| `Z0A` | External Untrusted | 0% | 외부 비신뢰 | 공격자, 익명 사용자 |
| `Z0B` | External Partners | 10% | 외부 파트너 | 협력업체, B2B |
| `Z1` | Perimeter/DMZ | 30% | 경계 | 웹 서버, WAF, 프록시 |
| `Z2` | Application | 50% | 애플리케이션 | WAS, API 서버 |
| `Z3` | Data | 80% | 데이터 | DB 서버, 스토리지 |
| `Z4` | Management | 90% | 관리 | 관리 콘솔, CI/CD |
| `Z5` | Core/Secrets | 100% | 핵심 비밀 | HSM, Vault |

**Zone 결정 질문**: "이 구성요소는 네트워크의 어떤 신뢰 영역에 위치하는가?"

### 5.4 차원 3: Function (기능적 역할)

Function 코드는 **계층적 형식**: `{Domain}{Category}.{Sequence}`

#### 10개 도메인

| 도메인 | 코드 | 설명 | Type |
|--------|------|------|------|
| Application | `A` | 애플리케이션 기능 | Capability |
| Compliance | `C` | 규제 준수 | Control |
| Data | `D` | 데이터 관리 | Capability |
| Interface | `I` | 통신 인터페이스 | Metadata |
| Monitoring | `M` | 모니터링 | Service |
| Networking | `N` | 네트워크 기능 | Capability |
| Platform | `P` | 플랫폼 서비스 | Service |
| Resource | `R` | 리소스 관리 | Capability |
| Security | `S` | 보안 통제 | Control |
| TechStack | `T` | 기술 스택 | Metadata |

#### 주요 Function 코드 (자주 사용)

```
S1.1  - Stateful Firewall        N1.1 - Routing
S1.3  - WAF                      N2.1 - L4 Load Balancing
S2.1  - RBAC                     N2.3 - Reverse Proxy
S3.1  - TLS/SSL                  N8.1 - Firewall (Network)
S4.2  - Secrets Management       
S5.1  - SIEM                     A2.1 - REST API Server
S5.2  - IDS/IPS                  A3.1 - Serverless
S6.1  - Vulnerability Scanner    A5.1 - API Gateway
S11.2 - Security Headers         A6.1 - Application Server
S11.4 - Input Sanitization       A7.1 - LLM Inference

D1.1  - RDBMS                    R2.1 - Virtual Machine
D2.1  - In-Memory Cache          R2.2 - Container
D3.1  - Message Queue            R3.1 - Kubernetes
D4.1  - Object Storage           R5.1 - Container Runtime

P1.1  - CI/CD                    M1.1 - Metrics Collection
P2.1  - Version Control          M2.1 - Log Aggregation
P3.1  - IaC                      M3.1 - APM

C1.1  - GDPR Compliance          I1.1 - HTTP/REST
C2.1  - SOC 2                    I4.1 - OAuth 2.0
C3.1  - PCI-DSS
```

> **전체 목록**: `02_framework/GR_DB/03_차원3_Function/` 디렉토리의 Domain별 문서 참조

#### Function 코드 결정 절차

```
1. "이 구성요소의 주 목적은?" → 도메인 결정 (S, N, A, D 등)
2. "어떤 종류의 기능?" → 카테고리 결정 (S1, S2, N2 등)  
3. "구체적으로 어떤 기능?" → 시퀀스 결정 (S1.1, S1.3 등)
```

> ⚠️ **Function 코드가 기존 택소노미에 없으면**: 가장 가까운 코드를 사용하되, 택소노미 확장이 필요하다는 주석을 남기세요.

### 5.5 scope (지식 원자용)

지식 원자(is_infrastructure: false)는 3D 좌표 대신 **적용 범위**를 기술합니다:

```yaml
scope:
  target_layers: ["L7"]          # 이 기법이 적용되는 Layer들
  target_zones: ["Z2"]           # 이 기법이 적용되는 Zone들
  target_functions: ["A2", "D1"] # 적용 대상 Function (선택)
```

---

## 6. atom_tags 배정 규칙

### 6.1 기본 원칙

- **통제된 어휘만 사용** (`03_ontology/taxonomy/atom_tags.yaml`에 정의된 태그)
- **최소 2개, 최대 10개**
- 카테고리 무관하게 자유 조합

### 6.2 태그 카테고리

| 카테고리 | 태그 예시 | 용도 |
|----------|----------|------|
| **attack_phase** | RECON, INITIAL, EXEC, PERSIST, PRIVESC, EVASION, CRED, LATERAL, EXFIL, IMPACT | 공격 단계 (MITRE Tactic 기반) |
| **vulnerability_type** | INJ, XSS, AUTHN, AUTHZ, CRYPTO, CONFIG, OVERFLOW, DESERIAL, SSRF, PATH, UPLOAD | 취약점 유형 (CWE 기반) |
| **technology_stack** | WEB, API, MOBILE, CLOUD, CONTAINER, IOT, NETWORK, EMBEDDED | 기술 스택 |
| **platform** | WINDOWS, LINUX, MACOS, AD, AWS, AZURE, GCP, K8S | 플랫폼/OS |
| **dbms** | MYSQL, MSSQL, ORACLE, PGSQL, SQLITE, MONGODB, REDIS | DBMS |
| **protocol** | HTTP, DNS, SMTP, SSH, RDP, SMB, LDAP, KERBEROS, TLS, TCP | 프로토콜 |
| **defense** | WAF, IDS, EDR, SIEM, DLP, AV, FW, IAM, PENTEST | 방어 도메인 |
| **general** | PROXY, CACHE, LOG, BACKUP, HA, LB | 일반 분류 |

### 6.3 5-Question 태그 배정법

모든 원자에 아래 질문을 순서대로 적용:

| # | 질문 | 해당 시 → 태그 카테고리 |
|---|------|----------------------|
| 1 | 어떤 공격 단계와 관련되는가? | `attack_phase` |
| 2 | 어떤 기술 스택에서 사용되는가? | `technology_stack` |
| 3 | 어떤 플랫폼에 해당하는가? | `platform` |
| 4 | 어떤 취약점 유형과 관련되는가? | `vulnerability_type` |
| 5 | 어떤 방어/프로토콜과 관련되는가? | `defense` 또는 `protocol` |

**예시**:

| 원자 | 태그 | 이유 |
|------|------|------|
| SQL Injection | `INJ, INITIAL, WEB, API` | 인젝션(Q4) + 초기접근(Q1) + 웹/API(Q2) |
| Kerberoasting | `CRED, AD, WINDOWS, KERBEROS` | 자격증명접근(Q1) + AD/Windows(Q3) + Kerberos(Q5) |
| WAF | `WAF, WEB, HTTP, FW, INJ, XSS` | 방어(Q5) + 웹(Q2) + 관련 취약점(Q4) |
| NIST CSF | `IAM, SIEM` | 관련 방어 도메인(Q5) |

---

## 7. 관계(Relations) 규칙

### 7.1 관계 유형 (7개 카테고리)

| 카테고리 | 관계 | 의미 | 예시 |
|----------|------|------|------|
| **structural** | `is_a` | 상위 개념이다 | SQLi is_a Injection |
| | `part_of` | 구성 요소다 | Payload part_of Attack |
| | `instance_of` | 사례다 | `' OR 1=1` instance_of SQLi |
| | `abstracts` | 추상화한다 | Principle abstracts Concept |
| **causal** | `causes` | 야기한다 | SQLi causes DataBreach |
| | `enables` | 가능케 한다 | FileRead enables CodeExec |
| | `prevents` | 방지한다 | WAF prevents SQLi |
| **conditional** | `requires` | 필요로 한다 | SQLi requires RDBMS |
| | `conflicts_with` | 상충한다 | 대칭 관계 |
| | `alternative_to` | 대체 가능 | 대칭 관계 |
| **temporal** | `precedes` | 선행한다 | Recon precedes Exploit |
| | `supersedes` | 대체한다 | NewVer supersedes OldVer |
| **applicability** | `applies_to` | 적용 대상 | Technique applies_to MySQL |
| | `effective_against` | 효과적 | Bypass effective_against WAF |
| **implementation** | `implements` | 구현한다 | Apache implements HTTP |
| **epistemic** | `contradicts` | 모순 | 대칭 |
| | `disputes` | 논쟁 | 대칭 |
| | `refines` | 정제 | NewResearch refines OldClaim |

### 7.2 관계 규칙

1. **Canonical 방향만 저장**: `is_a` 저장 ↔ `has_subtype`는 쿼리 시 역추적
2. **대칭 관계**: `conflicts_with`, `alternative_to`, `contradicts`, `disputes` — 한 번만 저장
3. **`related_to` 절대 금지**: 의미 모호, 무한 확장 가능 → 정밀 관계 사용

### 7.3 관계 배정 가이드

| 원자 type | 권장 관계 |
|-----------|----------|
| `technique` (ATK-) | `is_a`(상위 개념), `requires`(필요 조건), `applies_to`(대상) |
| `vulnerability` (VUL-) | `is_a`, `causes`(초래하는 결과) |
| `control_policy` (DEF-) | `prevents`(방지 대상), `applies_to`(적용 대상) |
| `component` (INFRA-) | `is_a`, `implements`(구현하는 프로토콜) |
| `tool_knowledge` (TOOL-) | `applies_to`(사용 대상), `effective_against` |
| `protocol` (TECH-) | `is_a`, `requires` |

---

## 8. 파일 명명 및 디렉토리

### 8.1 파일명 규칙

```
{PREFIX}-{CATEGORY}-{NAME}-{SEQ}.yaml
```

- **PREFIX**: 7개 중 하나 (ATK, DEF, VUL, TOOL, INFRA, COMP, TECH)
- **CATEGORY**: 주제별 분류 (선택적, 하이픈 구분)
- **NAME**: 원자 이름 (대문자, 하이픈 구분)
- **SEQ**: 3자리 시퀀스 (001, 002, ...)

**예시**:
```
ATK-INJECT-SQL-001.yaml
DEF-PREVENT-PARAMQUERY-001.yaml
INFRA-NET-WAF-001.yaml
VUL-WEB-XSS-001.yaml
TOOL-PENTEST-METASPLOIT-001.yaml
COMP-FRAMEWORK-NIST-001.yaml
TECH-PROTOCOL-HTTP-001.yaml
```

### 8.2 Prefix → 디렉토리 매핑 (1:1, 절대 규칙)

| Prefix | 디렉토리 |
|--------|----------|
| `ATK-` | `04_knowledge_base/atom_data/attacks/` |
| `DEF-` | `04_knowledge_base/atom_data/defenses/` |
| `VUL-` | `04_knowledge_base/atom_data/vulnerabilities/` |
| `TOOL-` | `04_knowledge_base/atom_data/tools/` |
| `INFRA-` | `04_knowledge_base/atom_data/infrastructure/` |
| `COMP-` | `04_knowledge_base/atom_data/compliance/` |
| `TECH-` | `04_knowledge_base/atom_data/technology/` |

### 8.3 서브디렉토리 규칙

각 디렉토리 내부는 **주제별 그룹핑** (분류에 영향 없음):

```
attacks/
├── web/          # 웹 공격
├── network/      # 네트워크 공격
├── cloud/        # 클라우드 공격
├── windows/      # Windows 공격
├── mitre/        # MITRE ATT&CK 매핑
└── ...
```

---

## 9. 완성 예시

### 예시 A: 인프라 원자 (INFRA-*)

```yaml
# GR Atom: PostgreSQL Database Server
identity:
  id: "INFRA-DATA-PGSQL-001"
  name: "PostgreSQL Database"
  normalization:
    normalized_name: "postgresql database"
    normalization_version: "1.0"
  aliases:
    - "PostgreSQL"
    - "Postgres"
    - "PgSQL"

classification:
  domain: data
  type: component                    # 핵심 인프라 구성요소
  is_infrastructure: true            # INFRA-* → 항상 true
  abstraction_level: 2               # 구체적 기술
  gr_coordinates:                    # 인프라이므로 3D 좌표 사용
    layer: "L5"                      # Data 계층
    zone: "Z3"                       # Data Zone
    function: "D1.1"                 # RDBMS
    atom_tags: ["PGSQL", "LINUX", "TLS"]

definition:
  what: |
    PostgreSQL은 오픈소스 객체-관계형 데이터베이스 관리 시스템(ORDBMS)이다.
    ACID 트랜잭션, MVCC, 확장성을 지원하며 엔터프라이즈 환경에서 널리 사용된다.
  why: |
    높은 안정성, SQL 표준 준수, 확장성으로 웹 애플리케이션부터
    대규모 데이터 분석까지 폭넓게 사용되는 핵심 데이터 인프라다.
  how: |
    1. 클라이언트 연결 수신 (TCP 5432)
    2. SQL 쿼리 파싱 및 실행 계획 수립
    3. MVCC 기반 동시성 제어
    4. WAL(Write-Ahead Logging)로 트랜잭션 보장
    5. 결과 반환

relations:
  structural:
    is_a: ["TECH-CONCEPT-DATABASE-001"]
  causal:
    enables:
      - "ATK-INJECT-SQL-001"         # SQL Injection 대상
  implementation:
    implements:
      - "TECH-LANG-SQL-001"          # SQL 구현

properties:
  technical:
    default_port: 5432
    supported_platforms: ["Linux", "Windows", "macOS"]

metadata:
  trust:
    source: official
    confidence: 1.0
    verified:
      status: verified
      date: 2026-02-05
      by: "GR System"
  temporal:
    created: 2026-02-05
    modified: 2026-02-05
    revision: 1
  security:
    sensitivity: public
  ai:
    embedding_text: |
      PostgreSQL Postgres는 오픈소스 객체-관계형 데이터베이스(ORDBMS)로,
      ACID 트랜잭션, MVCC, 확장성을 지원한다. TCP 5432 포트를 사용하며,
      웹 애플리케이션부터 대규모 분석까지 널리 쓰인다.
      SQL Injection 공격의 대상이 될 수 있다.
    search_keywords:
      - "PostgreSQL"
      - "Postgres"
      - "RDBMS"
      - "관계형 데이터베이스"
      - "SQL 데이터베이스"
    related_queries:
      - "PostgreSQL 보안 설정"
      - "PostgreSQL 취약점"
      - "PostgreSQL vs MySQL"
```

### 예시 B: 공격 기법 원자 (ATK-*)

```yaml
# GR Atom: Cross-Site Scripting (XSS)
identity:
  id: "ATK-WEB-XSS-001"
  name: "Cross-Site Scripting (XSS)"
  normalization:
    normalized_name: "cross site scripting xss"
    normalization_version: "1.0"
  aliases:
    - "XSS"
    - "크로스 사이트 스크립팅"

classification:
  domain: security
  type: technique                    # 구체적 공격 기법
  is_infrastructure: false           # ATK-* → 항상 false
  abstraction_level: 2               # 기법 수준
  scope:                             # 지식 원자이므로 scope 사용
    target_layers: ["L7"]
    target_zones: ["Z1", "Z2"]
    target_functions: ["A1", "A2"]
  atom_tags: ["XSS", "INITIAL", "WEB", "HTTP"]

definition:
  what: |
    XSS는 공격자가 웹 페이지에 악성 스크립트를 삽입하여
    다른 사용자의 브라우저에서 실행시키는 공격 기법이다.
  why: |
    OWASP Top 10에 꾸준히 포함되는 주요 웹 취약점으로,
    세션 탈취, 계정 장악, 악성코드 배포가 가능하다.
  how: |
    1. 공격자가 웹 입력 필드에 악성 JavaScript 삽입
    2. 서버가 입력을 검증 없이 페이지에 반영
    3. 피해자의 브라우저가 악성 스크립트 실행
    4. 쿠키 탈취, DOM 조작, 피싱 수행

relations:
  structural:
    is_a: ["GR-SEC-CON-00001"]       # Injection의 하위
  causal:
    causes:
      - "VUL-DATA-EXPOSURE-001"
  conditional:
    requires:
      - "TECH-LANG-JAVASCRIPT-001"
  applicability:
    applies_to:
      - "INFRA-APP-WEBAPP-001"

metadata:
  trust:
    source: official
    references:
      - "OWASP XSS Prevention Cheat Sheet"
      - "CWE-79"
    confidence: 1.0
    verified:
      status: verified
      date: 2026-02-05
      by: "GR System"
  temporal:
    created: 2026-02-05
    modified: 2026-02-05
    revision: 1
  security:
    sensitivity: public
    weaponization_risk: medium
  ai:
    embedding_text: |
      Cross-Site Scripting XSS는 웹 페이지에 악성 스크립트를 삽입하여
      다른 사용자의 브라우저에서 실행시키는 공격이다. Reflected, Stored,
      DOM-based 유형이 있으며, 세션 탈취와 계정 장악이 가능하다.
      OWASP Top 10, CWE-79에 해당한다.
    search_keywords:
      - "XSS"
      - "Cross-Site Scripting"
      - "크로스 사이트 스크립팅"
      - "스크립트 삽입"
      - "웹 공격"
    related_queries:
      - "XSS란?"
      - "XSS 공격 유형"
      - "XSS 방어 방법"
```

### 예시 C: 규정 원자 (COMP-*)

```yaml
# GR Atom: NIST Cybersecurity Framework
identity:
  id: "COMP-FRAMEWORK-NIST-001"
  name: "NIST Cybersecurity Framework (CSF)"
  normalization:
    normalized_name: "nist cybersecurity framework csf"
    normalization_version: "1.0"
  aliases:
    - "NIST CSF"
    - "NIST 사이버보안 프레임워크"

classification:
  domain: security
  type: control_policy               # 구체적 프레임워크
  is_infrastructure: false            # COMP-* → 항상 false
  abstraction_level: 3                # 개념/프레임워크 수준
  scope:
    target_layers: ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "Cross"]
    target_zones: ["Z0A", "Z0B", "Z1", "Z2", "Z3", "Z4", "Z5"]
  atom_tags: ["IAM", "SIEM", "EDR"]

definition:
  what: |
    NIST CSF는 미국 국립표준기술연구소(NIST)가 개발한 사이버보안 위험 관리
    프레임워크로, Identify/Protect/Detect/Respond/Recover 5개 핵심 기능으로 구성된다.
  why: |
    산업 표준으로 널리 채택되어 있으며, 조직의 사이버보안 성숙도를 평가하고
    개선하는 체계적 프레임워크를 제공한다.

relations:
  structural:
    is_a: ["TECH-CONCEPT-COMPLIANCE-001"]
  applicability:
    applies_to:
      - "INFRA-SECURITY-001"

metadata:
  trust:
    source: official
    references:
      - "https://www.nist.gov/cyberframework"
    confidence: 1.0
    verified:
      status: verified
      date: 2026-02-05
      by: "GR System"
  temporal:
    created: 2026-02-05
    modified: 2026-02-05
    revision: 1
  security:
    sensitivity: public
  ai:
    embedding_text: |
      NIST Cybersecurity Framework CSF는 미국 NIST의 사이버보안 프레임워크로,
      Identify, Protect, Detect, Respond, Recover 5개 기능으로 구성된다.
      조직의 보안 성숙도 평가와 위험 관리에 사용되는 산업 표준이다.
    search_keywords:
      - "NIST CSF"
      - "사이버보안 프레임워크"
      - "NIST"
      - "보안 프레임워크"
      - "위험 관리"
    related_queries:
      - "NIST CSF란?"
      - "NIST CSF 5대 기능"
      - "NIST CSF 도입 방법"
```

---

## 10. 검증 체크리스트

원자 파일을 작성하거나 검증할 때, 아래 항목을 **모두** 확인하세요:

### 10.1 필수 검증

| # | 항목 | 규칙 |
|---|------|------|
| 1 | ID prefix ↔ 디렉토리 | `ATK-` → `attacks/`, `DEF-` → `defenses/`, etc. |
| 2 | `is_infrastructure` | `INFRA-*` → `true`, 나머지 → `false` |
| 3 | `type` | prefix + 카테고리/구체적 판별에 따라 결정 |
| 4 | `atom_tags` | 최소 2개, `atom_tags.yaml` 통제 어휘만 |
| 5 | `function` | `is_infrastructure: true`인 경우만 존재, 계층적 형식 |
| 6 | `scope` | `is_infrastructure: false`인 경우만 존재 |
| 7 | `normalized_name` | 소문자, 특수문자 제거 |
| 8 | `definition.what` | 비어있지 않음 |
| 9 | `metadata.trust.source` | enum 값 |
| 10 | `metadata.trust.confidence` | 0.0-1.0 범위 |
| 11 | `metadata.ai.search_keywords` | 최소 5개 |

### 10.2 관계 검증

| # | 항목 | 규칙 |
|---|------|------|
| 12 | `related_to` 없음 | **절대 금지** |
| 13 | Inverse 관계 없음 | `has_subtype`, `caused_by` 등 저장 금지 |
| 14 | 참조 ID 존재 | 관계에 사용된 atom_id가 실제 존재 |
| 15 | 순환 참조 없음 | `is_a`, `part_of`, `requires` 순환 금지 |

### 10.3 구 type 확인 (마이그레이션 검증)

| # | 항목 | 규칙 |
|---|------|------|
| 16 | `type: control` 없음 | → `control_policy` 또는 `component_control`로 분리 |
| 17 | `type: tool` 없음 | → `tool_knowledge` 또는 `component_tool`로 분리 |
| 18 | `GR-SEC-*` ID 없음 | → 적절한 prefix로 변환 |

---

## 11. 금지 사항

| 금지 항목 | 이유 | 대안 |
|-----------|------|------|
| `related_to` 관계 | 의미 모호, 무한 확장 | 정밀 관계 사용 (`is_a`, `enables` 등) |
| 단일 문자 Function (`A`, `S`) | 계층적 형식 필수 | `A1.1`, `S2.1` 등 사용 |
| `type: control` (구 type) | v2.0에서 분리됨 | `component_control` 또는 `control_policy` |
| `type: tool` (구 type) | v2.0에서 분리됨 | `component_tool` 또는 `tool_knowledge` |
| 자유 태그 | 통제 어휘 위반 | `atom_tags.yaml`에 정의된 태그만 |
| INFRA-* 이외에 `function` 필드 | 인프라 좌표 전용 | `scope` 사용 |
| Inverse 관계 저장 | 쿼리 시 파생 | canonical 관계만 저장 |

---

## 12. 참조 파일 목록

| 파일 | 경로 | 내용 |
|------|------|------|
| **이 가이드** | `00_docs/GR_AGENT_GUIDE.md` | AI 에이전트 종합 가이드 |
| 원자 스키마 | `03_ontology/schema/core/atom_schema.yaml` | 필드 정의, 타입, 패턴 |
| 관계 타입 | `03_ontology/schema/core/relation_types.yaml` | 관계 정의 및 규칙 |
| 원자 태그 | `03_ontology/taxonomy/atom_tags.yaml` | 통제 어휘 (태그 목록) |
| Layer 정의 | `03_ontology/taxonomy/layers.yaml` | L0-L7, Cross |
| Zone 정의 | `03_ontology/taxonomy/zones.yaml` | Z0A-Z5 |
| Function 개요 | `02_framework/GR_DB/03_차원3_Function/00_차원3_개요.md` | 10개 도메인, 280+ 태그 |
| Function 상세 | `02_framework/GR_DB/03_차원3_Function/Domain_*.md` | 도메인별 코드 목록 |
| 헌법 | `03_ontology/constitution/GR_KNOWLEDGE_ATOMIZATION_CONSTITUTION.md` | 최고 규범 |
| 분류 규칙 | `03_ontology/guides/GR_CLASSIFICATION_RULES.md` | 상세 분류 규칙 |
| 기존 원자 | `04_knowledge_base/atom_data/` | 560+ 기존 원자 파일 |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                GR Ontology Quick Reference               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Prefix    Dir              is_infra   Default Type     │
│  ───────   ──────────────   ────────   ─────────────    │
│  INFRA-    infrastructure/  true       component        │
│  ATK-      attacks/         false      technique        │
│  DEF-      defenses/        false      control_policy   │
│  VUL-      vulnerabilities/ false      vulnerability    │
│  TOOL-     tools/           false      tool_knowledge   │
│  COMP-     compliance/      false      control_policy   │
│  TECH-     technology/      false      concept          │
│                                                         │
│  3D 좌표 (INFRA-* only):                                │
│    Layer: L0-L7, Cross                                  │
│    Zone:  Z0A, Z0B, Z1-Z5                              │
│    Function: {Domain}{Cat}.{Seq} (예: S1.1, A2.1)      │
│                                                         │
│  atom_tags: 2-10개, atom_tags.yaml 통제 어휘만           │
│  related_to: ❌ 절대 금지                                │
│  type: control / tool: ❌ 구 type, 분리 필수             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

> **문서 끝** | 이 가이드에 대한 질문이나 모호한 부분이 있으면, 즉시 GR 프로젝트 관리자에게 확인하세요.
> 모호성은 규칙의 결함이며, 해결해야 할 대상입니다.
