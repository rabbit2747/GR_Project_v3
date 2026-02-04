# GR 마스터플랜 (통합본)

> **"Foundation, not Product - AI를 위한 보안 지능의 토대"**
> **버전**: 3.0 (통합본)
> **최종 수정**: 2026-02-04

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 마스터플랜 (통합본) |
| **목적** | GR 생태계의 비전, 아키텍처, 비즈니스 모델, 실행 계획 통합 |
| **대상 독자** | 모든 이해관계자 (기술자, 비기술자, 투자자) |
| **통합 원본** | 5개 마스터플랜 문서 통합 |

---

# Part 1: 비전 & 전략

## 1. Executive Summary

### 1.1 한 줄 요약

> **보안 컨설팅 회사의 전문 지식을 DB화하여, 하나의 Core로 여러 사업을 만드는 프로젝트**

### 1.2 프로젝트 정체성

```
GR = 인프라 맥락 기반 통합 보안 온톨로지

"보안은 인프라 위에서 일어난다"
모든 공격/방어/취약점에 WHERE(인프라 맥락)를 부여하여
AI가 맥락을 이해하고 추론할 수 있게 하는 지식 체계
```

### 1.3 핵심 가치 제안

| 기존 문제 | GR 솔루션 |
|-----------|-----------|
| MITRE ATT&CK: 공격 기법만, 인프라 맥락 없음 | 모든 기법에 WHERE 부여 |
| CVE: 취약점 나열, 관계 부족 | 인프라-취약점-공격-방어 연결 |
| 상용 LLM 의존 | 자체 LLM/RAG용 지식베이스 |
| 파편화된 보안 지식 | 통합 온톨로지로 연결 |

### 1.4 최종 산출물

```
GR Ontology (Core)
    │
    ├─→ 자체 LLM / RAG 시스템
    ├─→ 자동화 진단 도구 (DAST, SAST, ...)
    ├─→ 보안 관리 솔루션
    ├─→ 교육 시스템 (GR Edu)
    └─→ 신뢰성 높은 IaC 생성
```

---

## 2. 비전 & 철학

### 2.1 비전

> **"보안 지식의 표준 온톨로지를 구축하여, 인프라 맥락 기반의 AI 추론을 가능하게 한다"**

### 2.2 핵심 철학

**1. Foundation, not Product (토대, 제품이 아님)**
- 우리는 특정 보안 솔루션을 만들지 않습니다
- 모든 보안 제품이 공통으로 사용할 **'보안의 표준 언어와 좌표계'**를 만듭니다
- GR DB와 GR Framework는 상품이 아니라 **생태계의 기초 인프라**입니다

**2. Context-Aware Security (맥락 기반 보안)**
- 제품 자체가 아니라, 그 제품이 **'어디서(Zone/Layer) 무엇을(Function) 하는가'**에 따라 보안 정책을 결정합니다
- 같은 Nginx라도 프록시로 쓰면 Layer 2, 웹서버로 쓰면 Layer 7의 보안 정책을 적용합니다

**3. AI-First Architecture (AI 우선 설계)**
- 사람이 읽기 위한 문서가 아니라, **AI가 학습하고 추론하기 위한 데이터셋**으로 설계합니다
- RAG를 통해 할루시네이션 없는 정확한 보안 진단을 제공합니다

**4. 인프라가 앵커(Anchor)**
- 모든 보안 지식은 인프라 위에서 맥락을 가짐
- 공격/방어/취약점 모두 "어디서(WHERE)"와 연결

**5. 관계 중심 (Ontology)**
- 단순 나열이 아닌 연결된 지식 그래프
- AI가 관계를 통해 추론 가능

**6. 실용성 우선**
- 학술적 완벽성보다 실무 적용 가능성
- 진단 도구, 교육 시스템에 바로 사용 가능

---

## 3. 왜 이 프로젝트인가?

### 3.1 문제: 컨설팅 비즈니스의 한계

```
일이 늘어나면 → 사람을 뽑아야 함 → 인건비 증가 → 수익률 정체
```

보안 컨설팅은 **"사람이 직접 하는 일"**입니다.
- 프로젝트 10개 하려면 → 10명 필요
- 프로젝트 100개 하려면 → 100명 필요

이것이 **선형 성장의 함정**입니다.

### 3.2 해결: 노하우를 "자산"으로 만들기

```
전문가의 머릿속 지식 → DB에 저장 → 여러 제품이 재사용 → 확장 가능한 사업
```

핵심 아이디어:
1. 컨설팅하면서 쌓은 **보안 노하우**를 체계적으로 정리
2. 이것을 **DB + Framework + 시각화(Atlas)**로 구축
3. 이 Core 위에 **여러 사업 아이템**을 올림

### 3.3 왜 지금인가? (2025년 AI 시대의 기회)

```
과거: 데이터 구축 = 사람이 직접 = 비용 막대
현재: 데이터 구축 = AI 자동화 = 비용 현실적
```

- LLM이 제품 문서를 읽고 분류 가능
- 크롤링 + AI로 대량 데이터 구축 가능
- 소규모 팀으로도 대규모 DB 구축 가능

### 3.4 보안 컨설팅 회사가 하기에 적합한 이유

1. **실무 데이터 접근성**: 매일 고객사 인프라를 봄
2. **검증 기회**: 컨설팅하면서 Framework 테스트 가능
3. **즉시 사용자**: 본인 회사가 첫 번째 고객
4. **도메인 전문성**: 외부 개발사보다 보안을 잘 앎

---

## 4. MITRE ATT&CK과의 관계: WHERE + HOW

### 4.1 기존 보안 프레임워크의 한계

**MITRE ATT&CK**은 업계 표준 공격 기법 분류체계입니다.
하지만 MITRE는 **"어떻게(HOW)"** 공격하는지만 알려줍니다.

```
MITRE ATT&CK이 알려주는 것:
- T1190: 공개된 애플리케이션 취약점 공격
- T1059: 명령어 실행
- T1003: 인증 정보 탈취

→ "어떻게 공격하는지"는 알지만
→ "어디를 공격하는지"는 모름
```

### 4.2 GR Framework의 역할: "WHERE"

```
┌─────────────────────────────────┬───────────────────────────────┐
│       MITRE ATT&CK              │        GR Framework           │
│         (HOW)                   │           (WHERE)             │
├─────────────────────────────────┼───────────────────────────────┤
│  "이렇게 공격한다"               │  "여기가 공격당한다"           │
│                                 │                               │
│  • 공격 기법 분류                │  • 인프라 위치 분류            │
│  • 공격 단계 정의                │  • 공격 대상 정의              │
│  • 방어 방법 제안                │  • 공격 경로 시각화            │
└─────────────────────────────────┴───────────────────────────────┘

                    ↓ 결합하면 ↓

        "어디에서 + 어떻게" = 실행 가능한 보안 전략
```

**GR Framework는 MITRE와 경쟁하지 않습니다. 보완합니다.**

### 4.3 실제 예시: Log4Shell 취약점

```
MITRE만 보면:
  "T1190 기법으로 공격할 수 있다" (끝)

GR + MITRE를 보면:
  1. [Z1 → Z2] 웹서버에서 Log4j 취약점 공격 (T1190)
  2. [Z2 → Z3] 내부 네트워크로 이동, DB 접근 시도 (T1003)
  3. 구체적 대응: Z2에 WAF 강화, Z3 접근 제어 강화
```

---

## 5. GR Core: 모든 것의 토대

### 5.1 생태계 계층 구조

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: 제품 (Products) - 실제 수익 창출                    │
│  - 자동화 진단 솔루션                                         │
│  - GR IaC (Infrastructure as Code Generator)                │
│  - GR Edu (보안 교육 플랫폼)                                  │
│  - 컨설팅 서비스                                             │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (활용)
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: 지능 (Intelligence) - AI/RAG 엔진                  │
│  - GR AI Agent                                              │
│  - Vector Search Engine                                     │
│  - Graph Query Engine                                       │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (학습)
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: 문법 (Grammar) - GR Framework                     │
│  - 3차원 좌표계 (Layer × Zone × Function)                    │
│  - 보안 정책 규칙                                            │
│  - 원자화(Atomization) 방법론                                │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ (구조화)
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 토대 (Foundation) - GR DB                         │
│  - 전 세계 IT 제품의 메타데이터                               │
│  - 제품의 모든 가능한 역할(Archetypes)                        │
│  - CVE, 취약점, 보안 Best Practice                           │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 각 계층의 정의

| 계층 | 명칭 | 역할 | 비유 | 수익 모델 |
|------|------|------|------|----------|
| **Layer 1** | GR DB | 보안의 위키피디아, AI 학습 원천 데이터 | 도서관 | 무료 (투자 기반) |
| **Layer 2** | GR Framework | 데이터를 해석하는 규칙과 좌표계 | 문법책 | 무료 (오픈 스탠다드) |
| **Layer 3** | AI/RAG | GR DB를 참조하여 상황에 맞는 답을 추론 | 전문가 | API 사용료 |
| **Layer 4** | Products | 고객의 문제를 해결하는 구체적 서비스 | 의사/변호사 | SaaS 구독료 |

### 5.3 GR Atlas: 보안의 지도

**GR Atlas**는 인프라를 **지도처럼** 보여주는 시각화 기능입니다.

```
일반 지도                          GR Atlas
─────────────                      ─────────
• 지형, 도로, 건물                 • Layer, Zone, 서버
• 교통 흐름                        • 데이터 흐름
• 위험 지역 표시                   • 취약점 위치 표시
• 최적 경로 안내                   • 공격 경로 시각화
```

**Atlas는 제품이 아니라 기능(Feature)입니다** - 자동화 진단, IaC, Edu에 내장되는 공통 컴포넌트

---

# Part 2: 3D 프레임워크 & 아키텍처

## 6. 3차원 좌표계 (3D Framework)

AI가 인프라를 입체적으로 인식하기 위한 3축 좌표계입니다.

### 6.1 개념도

```
┌─────────────────────────────────────────────────────────────┐
│                    GR Ontology                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│   │ INFRA       │────→│ VULNERABILITY│←────│ ATTACK      │  │
│   │ 인프라 요소  │     │ 취약점       │     │ 공격 기법    │  │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘  │
│          │                   │                   │          │
│          │    ┌──────────────┼──────────────┐    │          │
│          │    │              │              │    │          │
│          ▼    ▼              ▼              ▼    ▼          │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│   │ DEFENSE     │     │ TOOL        │     │ CONCEPT     │  │
│   │ 방어 기법    │     │ 도구        │     │ 개념        │  │
│   └─────────────┘     └─────────────┘     └─────────────┘  │
│                                                             │
│   ─────────────────────────────────────────────────────    │
│   모든 요소는 GR 좌표 (Layer/Zone/Function)를 가짐          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 축 1: Deployment Layer (기술 스택의 수직적 깊이)

**AI의 관점**: "이 구성요소는 하드웨어인가, 소프트웨어인가, 아니면 우리가 빌려 쓰는 서비스인가?"

| Layer | 명칭 (한글) | 명칭 (영문) | 설명 | 변경 빈도 | 예시 |
|-------|------------|-------------|------|----------|------|
| **L0** | 외부 서비스 | External Services | 관리 불필요, 계약 기반 사용 | - | OpenAI API, Salesforce, GitHub |
| **L1** | 물리 인프라 | Physical Infrastructure | 데이터센터, 하드웨어 | Low | Server, Storage, Data Center |
| **L2** | 네트워크 인프라 | Network Infrastructure | 연결 및 보호 | Medium | Firewall, LB, VPN, DNS |
| **L3** | 컴퓨팅 인프라 | Computing Infrastructure | 가상화 및 컴퓨팅 리소스 | Medium | VM, Cloud Platform, Hypervisor |
| **L4** | 플랫폼 서비스 | Platform Services | DevOps, IaC | High | CI/CD, Terraform, Git |
| **L5** | 데이터 서비스 | Data Services | 저장 및 처리 | Medium | Database, Storage, Backup |
| **L6** | 런타임 환경 | Runtime Environment | 컨테이너, 오케스트레이션 | High | Docker, Kubernetes, Message Queue |
| **L7** | 애플리케이션 & AI | Application & AI Logic | 비즈니스 로직 및 AI 워크로드 | Very High | Web App, LLM Model, Vector Search, RAG Pipeline |
| **Cross** | 관리 & 보안 | Management & Security | 모든 계층 관통 | Medium | Monitoring, IAM, SIEM, Testing |

### 6.3 축 2: Security Zone (보안 신뢰의 수평적 경계)

**AI의 관점**: "이곳은 얼마나 위험한가? 누구와 대화할 수 있는가?"

| Zone | 명칭 | 신뢰도 | 설명 | 보안 원칙 | 예시 구성요소 |
|------|------|--------|------|----------|--------------|
| **Z0A** | 비신뢰 외부 | 0% | 일반 인터넷, 해커, 익명 사용자 | Default Deny | - |
| **Z0B** | 신뢰 파트너 | 10% | API Key로 인증된 외부 SaaS/Partner | Allow with Auth | OpenAI API, GitHub, Slack |
| **Z1** | 경계 영역 (Perimeter) | 0-20% | 외부 위협 차단 최전선 (DMZ) | 최대 강도 필터링 | Firewall, WAF, DDoS 방어 |
| **Z2** | 애플리케이션 영역 | 30% | 비즈니스 로직 실행 영역 | 인증/인가 필수 | Web Server, API Server |
| **Z3** | 데이터 영역 | 60% | 가장 민감한 자산 보관 | 격리 + 암호화 | Database, 파일 스토리지 |
| **Z4** | 관리 영역 (Management) | 80% | 시스템 전체 통제 관제탑 | 최고 수준 접근 제어 | 모니터링, 로깅, CI/CD |
| **Z5** | 엔드포인트 영역 | 50% | 제로 트러스트 기반 사용자 단말 | 지속적 검증 | 사용자 PC, 모바일, VPN Client |

### 6.4 축 3: Function (기능적 역할)

**AI의 관점**: "이 녀석의 정체는 무엇이고, 어떤 기능을 수행하는가?"

#### 기능 도메인 (8개)

| 코드 | 도메인명 (한글) | 도메인명 (영문) | 설명 |
|------|----------------|----------------|------|
| **M** | 관리 기능 | Management | 모니터링, 로깅, 백업 |
| **N** | 네트워크 기능 | Network | 라우팅, 로드밸런싱, 프록시 |
| **S** | 보안 기능 | Security | 인증, 암호화, 위협 탐지 |
| **A** | 애플리케이션 기능 | Application | 웹서버, API, UI/UX |
| **D** | 데이터 기능 | Data | 저장, 처리, 분석 |
| **R** | 런타임 기능 | Runtime | 컨테이너, 메시징, 캐시 |
| **C** | 컴퓨팅 기능 | Computing | 가상화, 오케스트레이션 |
| **P** | 플랫폼 기능 | Platform | CI/CD, IaC, 버전 관리 |

#### 계층적 구조 (예: Application 도메인)

```
A: Application (애플리케이션)
├── A1: Web Services (웹 서비스)
│   ├── A1.1: Static Content (정적 콘텐츠)
│   ├── A1.2: Dynamic Content (동적 콘텐츠)
│   └── A1.3: Single Page App (SPA)
├── A2: API Services (API 서비스)
│   ├── A2.1: REST API
│   ├── A2.2: GraphQL
│   └── A2.3: gRPC
└── A3: Business Logic (비즈니스 로직)
    ├── A3.1: Transaction Processing
    └── A3.2: Workflow Engine
```

---

## 7. 원자(Atom) 구조

### 7.1 표준 구조 (스키마 v2.0)

```yaml
Atom:
  # ─── 정체성 ───
  id: "DOMAIN-TYPE-NAME-###"
  name: "정식 명칭"
  aliases: ["별칭들"]

  # ─── GR 분류 ───
  type: component | component_tool | component_control | concept | technique | vulnerability | principle | pattern | protocol | tool_knowledge | control_policy
  is_infrastructure: true | false  # 인프라 요소 여부

  # ─── GR 좌표 (인프라 요소만) ───
  gr_coordinates:  # is_infrastructure: true인 경우
    layer: "L0-L7 | Cross"
    zone: "Z0A | Z0B | Z1-Z5"
    function: "A1.1 | S2.1 | ..."

  # ─── 범위 (지식/개념만) ───
  scope:  # is_infrastructure: false인 경우
    layers: ["L5", "L7"]
    zones: ["Z2", "Z3"]

  # ─── 원자 태그 (모든 원자) ───
  atom_tags: ["INJ", "WEB", "AUTH"]

  # ─── 정의 (LLM 학습용) ───
  definition:
    what: "무엇인가 (200-300자)"
    why: "왜 중요한가 (150-200자)"
    how: "어떻게 작동하는가 (200-400자)"

  # ─── 핵심 개념 ───
  core_concepts:
    - name: "개념명"
      description: "설명"
      security_relevance: "보안 관련성"

  # ─── 관계 (온톨로지 핵심) ───
  relations:
    structural:
      is_a: []           # 상위 개념
      has_subtypes: []   # 하위 유형
    causal:
      requires: []       # 필요 조건
      enables: []        # 가능하게 하는 것
      prevents: []       # 방지하는 것
    security:
      targets: []        # 공격 대상 (공격 기법인 경우)
      mitigates: []      # 완화 대상 (방어 기법인 경우)
      vulnerable_to: []  # 취약한 공격/취약점
    implementation:
      implements: []     # 구현하는 프로토콜/표준

  # ─── 보안 프로파일 ───
  security:
    attack_surface: []
    common_vulnerabilities: []
    attack_techniques: []
    defenses: []

  # ─── 제품/인스턴스 ───
  products: []

  # ─── 프로토콜 ───
  protocols: []

  # ─── 메타데이터 ───
  metadata:
    trust:
      source: ""
      references: []
      confidence: 0.0-1.0
    temporal:
      created: ""
      modified: ""
      version: ""
```

### 7.2 is_infrastructure 판정 기준

**4가지 질문 (하나라도 Yes면 true)**:

| 질문 | Yes 예시 | No 예시 |
|------|---------|---------|
| 네트워크 주소를 가질 수 있는가? | Nginx (IP:Port), PostgreSQL | SQL Injection (기법) |
| 프로세스로 실행될 수 있는가? | Docker Container, Apache | OWASP Top 10 (개념) |
| 물리적 형태가 있을 수 있는가? | 서버, 네트워크 장비 | Zero Trust (원칙) |
| 시스템 자원을 소비하는가? | Redis (메모리), JVM | HTTP Protocol (표준) |

### 7.3 Type 분류 체계

**is_infrastructure: true (인프라 요소)**
- `component`: 일반 인프라 구성요소 (WAS, DB, 웹서버)
- `component_tool`: 배포된 보안/진단 도구 (Nmap 서버, Burp Suite)
- `component_control`: 배포된 보안 통제 (WAF, IDS, 방화벽)

**is_infrastructure: false (지식/개념)**
- `concept`: 추상적 개념 (Zero Trust, Defense in Depth)
- `technique`: 공격/방어 기법 (SQL Injection, Parameterized Query)
- `vulnerability`: 취약점 유형 (CWE-89, Buffer Overflow)
- `principle`: 보안 원칙 (최소 권한, 심층 방어)
- `pattern`: 설계 패턴 (MVC, Microservices)
- `protocol`: 통신 프로토콜 (HTTP, TLS, OAuth)
- `tool_knowledge`: 도구 사용법 지식 (Nmap 사용법)
- `control_policy`: 통제 정책 (접근 제어 정책)

### 7.4 원자 분량 가이드라인

| 섹션 | 목적 | 권장 분량 |
|------|------|-----------|
| definition | LLM 기본 이해 | 500-800자 |
| core_concepts | 심화 지식 | 개념당 100-200자 |
| relations | 온톨로지 추론 | 5-15개 관계 |
| security | 보안 실무 | 500-1000자 |
| products | 실제 적용 | 200-400자 |

**총 원자 분량**: A4 2-4페이지 (YAML 포함)

### 7.5 원자 유형별 ID 체계

```
INFRA-*     인프라 요소
  INFRA-NET-*     네트워크 (라우터, 방화벽, LB...)
  INFRA-COMPUTE-* 컴퓨팅 (서버, VM, 클라우드...)
  INFRA-DATA-*    데이터 (DB, 스토리지...)
  INFRA-APP-*     애플리케이션 (WAS, 웹서버...)
  INFRA-RUNTIME-* 런타임 (컨테이너, K8s...)
  INFRA-PLATFORM-* 플랫폼 (CI/CD, IaC...)
  INFRA-IAM-*     인증/인가 (AD, SSO, PKI...)
  INFRA-CLOUD-*   클라우드 서비스 (AWS, Azure, GCP...)

ATK-*       공격 기법
  ATK-RECON-*     정찰
  ATK-INIT-*      초기 접근
  ATK-EXEC-*      실행
  ATK-PERSIST-*   지속성
  ATK-PRIVESC-*   권한 상승
  ATK-EVASION-*   방어 회피
  ATK-CRED-*      자격증명 접근
  ATK-DISCOVERY-* 탐색
  ATK-LATERAL-*   측면 이동
  ATK-COLLECT-*   수집
  ATK-EXFIL-*     유출
  ATK-IMPACT-*    영향

DEF-*       방어 기법
  DEF-DETECT-*    탐지
  DEF-PREVENT-*   예방
  DEF-RESPOND-*   대응
  DEF-RECOVER-*   복구

VUL-*       취약점 유형
  VUL-INJECT-*    인젝션
  VUL-AUTH-*      인증
  VUL-CRYPTO-*    암호화
  VUL-CONFIG-*    설정
  VUL-MEMORY-*    메모리

TOOL-*      도구
  TOOL-OFFENSE-*  공격 도구
  TOOL-DEFENSE-*  방어 도구
  TOOL-AUDIT-*    감사 도구

CON-*       개념
  CON-PRINCIPLE-* 원칙
  CON-PATTERN-*   패턴
  CON-PROTOCOL-*  프로토콜
```

---

## 8. 기존 표준 연동

### 8.1 MITRE ATT&CK 매핑

```yaml
# ATK 원자에 MITRE 매핑 포함
ATK-INJECT-SQL-001:
  name: "SQL Injection"
  mitre_mapping:
    technique_id: "T1190"
    technique_name: "Exploit Public-Facing Application"
    tactic: "Initial Access"
    sub_techniques: ["T1190.001"]

  # GR 확장: WHERE 정보 추가
  gr_extension:
    target_layers: ["L5", "L7"]
    target_zones: ["Z2", "Z3"]
    target_components: ["INFRA-DATA-RDBMS-*", "INFRA-APP-WAS-*"]
```

### 8.2 CVE/CWE 연동

```yaml
# VUL 원자에 CVE/CWE 연결
VUL-INJECT-SQL-001:
  name: "SQL Injection Vulnerability"
  cwe_id: "CWE-89"
  related_cves:
    - id: "CVE-2021-XXXXX"
      cvss: 9.8
      affected_products: ["INFRA-APP-WAS-*"]

  # GR 확장: 인프라 맥락
  gr_context:
    commonly_found_in:
      - layer: "L7"
        zone: "Z2"
        components: ["Web Application"]
    attack_path:
      entry: "Z0A"
      target: "Z3"
```

### 8.3 MITRE D3FEND 연동

```yaml
# DEF 원자에 D3FEND 매핑
DEF-PREVENT-PARAMQUERY-001:
  name: "Parameterized Query"
  d3fend_mapping:
    technique_id: "D3-PQ"
    technique_name: "Parameterized Query"
    tactic: "Application Hardening"

  # GR 확장: 적용 위치
  gr_application:
    target_layers: ["L7"]
    target_components: ["INFRA-APP-WAS-*", "INFRA-APP-API-*"]
    mitigates: ["VUL-INJECT-SQL-001", "ATK-INJECT-SQL-001"]
```

---

## 9. 데이터 아키텍처

### 9.1 하이브리드 데이터베이스 전략

GR DB는 **단일 DB가 아닌 3개 DB의 조합**입니다.

```
┌─────────────────────────────────────────────────────┐
│               API Gateway (FastAPI)                 │
│          단일 진입점, 쿼리 라우팅 및 조합             │
└────────────┬───────────────┬────────────────┬───────┘
             │               │                │
             ▼               ▼                ▼
    ┌─────────────┐  ┌──────────────┐  ┌─────────────┐
    │ PostgreSQL  │  │   Neo4j      │  │  Pinecone   │
    │  (Master)   │  │ (Graph DB)   │  │ (Vector DB) │
    └─────────────┘  └──────────────┘  └─────────────┘
         │                  │                  │
    [Product Info]    [Relationships]    [Embeddings]
    - Name            - Zone → Layer    - 설명 벡터
    - Vendor          - Function → Product   - 스펙 벡터
    - CPE             - Attack Path     - 유사도 검색
    - Version         - Dependency
    - License         - CVE Impact
```

### 9.2 DB별 역할 분담

| Database | 역할 | 저장 데이터 | 핵심 쿼리 | 선택 이유 |
|----------|------|------------|----------|----------|
| **PostgreSQL** | Master (불변 팩트) | Product 정보, Vendor, CPE, License, Version | `SELECT * WHERE vendor='Apache'` | ACID 보장, 트랜잭션 지원 |
| **Neo4j** | Relationships (관계) | Zone↔Layer 연결, Function 조합, 공격 경로, 의존성 | `MATCH (a)-[*]->(b) RETURN path` | 관계 탐색 최적화, 그래프 쿼리 |
| **Pinecone** | Semantics (의미) | 제품 설명 임베딩, 스펙 벡터 | `similarity_search(vector, k=10)` | 고속 벡터 검색, RAG 최적화 |

### 9.3 2-Tier 원자화 전략

#### Tier 1: Product Master (불변의 팩트)

**저장 위치**: PostgreSQL
**성격**: 변하지 않는 제품의 객관적 정보

```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    vendor VARCHAR(200),
    cpe VARCHAR(500),
    license VARCHAR(100),
    primary_language VARCHAR(50),
    release_date DATE,
    eol_date DATE,
    source_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tier 2: Component Archetypes (가능한 역할들)

**저장 위치**: Neo4j (Graph) + Pinecone (Vector)
**성격**: 하나의 제품이 가질 수 있는 **모든 변신 형태**

```
(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:Cache)
                                     ├─ layer: "L5"
                                     ├─ zone: "Z2"
                                     ├─ primary_function: "D3.1"
                                     └─ use_case: "Application cache"

(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:SessionStore)
                                     ├─ layer: "L5"
                                     ├─ zone: "Z3"
                                     ├─ primary_function: "D3.3"
                                     └─ use_case: "Session management"
```

---

## 10. LLM & AI 전략

### 10.1 Phase별 LLM 사용 구분

#### 구축 단계 (Phase 0-2)

**목표**: 10,000개 제품 × 평균 3개 Archetype = 30,000개 지식 노드 구축

**LLM 사용**:
- 외부 LLM API 자유 사용 (GPT-4, Claude, Gemini)
- 제품 설명 → Archetype 추론
- 공식 문서 → Function 추출
- CVE 설명 → MITRE Technique 매핑

**데이터 안전성**: 모두 공개 데이터 (제품 정보, CVE, 공식 문서) → 외부 API 사용 안전

#### 고객 배포 단계 (Phase 2+)

**80/20 원칙**: Direct Query 80% + AI-Assisted 20%

**80% Direct Query (AI 불필요)**:
```python
# 제품 태그 조회 (단순 DB 쿼리)
def get_product_tags(product_name: str):
    """
    PostgreSQL + Neo4j 직접 쿼리
    - 응답 시간: 50ms
    - 정확도: 100%
    - 비용: $0
    - 기밀 안전: ✅
    """
```

**20% AI-Assisted (복잡한 추론 필요)**:
- 옵션 1: On-premise LLM (기밀 유지) - Llama 3.1, Mistral
- 옵션 2: 익명화 후 외부 LLM - 민감 정보 마스킹

### 10.2 비용 비교

| 방식 | 응답 속도 | 정확도 | 월 비용 | 기밀 안전성 |
|------|----------|--------|---------|------------|
| Direct Query (80%) | 50-100ms | 100% | $0 | 완벽 |
| On-premise LLM (20%) | 500ms-2s | 95% | $0 (운영비만) | 완벽 |
| External LLM (20%) | 1-3s | 98% | $100-$500 | 익명화 필요 |

### 10.3 자체 AI 모델 개발 계획 (Phase 3)

- GR DB 기반 Fine-tuned LLM 개발
- 30,000+ Archetype 데이터로 학습
- 보안 도메인 특화 모델
- Base 모델: Llama 3 / Mistral
- Serving: vLLM / TGI

---

# Part 3: 비즈니스 & 실행

## 11. 비즈니스 모델

### 11.1 수익 구조

GR은 **"토대는 무료, 지능과 제품은 유료"** 전략을 사용합니다.

```
┌─────────────────────────────────────────────────────────┐
│  Free Tier (무료)                                        │
│  - GR Framework 명세서 (오픈 스탠다드)                    │
│  - GR DB 일부 조회 (API, 제한적)                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Premium Tier (유료)                                     │
│  - GR DB 전체 접근 (API 무제한)                          │
│  - AI 추론 엔진 사용 (RAG 기반 답변)                     │
│  → 가격: $500/월 (B2B)                                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Products (제품)                                         │
│  - 자동화 진단 솔루션: $5,000~$50,000/년                │
│  - GR IaC: $10,000~$100,000/년                          │
│  - GR Edu: $2,000/년 (1인당)                            │
│  - 컨설팅: $200/시간                                     │
└─────────────────────────────────────────────────────────┘
```

### 11.2 제품 라인업

#### 11.2.1 자동화 진단 도구

**현재**: 컨설턴트가 직접 인프라 점검 → 보고서 작성 (2-4주)
**GR 적용 후**: 시스템이 자동 스캔 → 즉시 결과 (1-2일)

```
입력: 고객사 인프라 정보
        ↓
    [GR Framework]
    • 각 구성요소 좌표 자동 할당
    • 보안 정책 자동 적용
    • 취약점 자동 매칭
        ↓
출력: 상세 진단 보고서 + Atlas 시각화
```

#### 11.2.2 GR IaC (Infrastructure as Code)

**GR IaC의 차별점**:
```
입력: "3-tier 웹 서비스 만들어줘"
        ↓
    [GR IaC]
    • 인프라 코드 생성 (Terraform)
    • 각 구성요소에 GR 좌표 자동 할당
    • 좌표에 맞는 보안 설정 자동 포함
        ↓
출력: 보안이 내장된 인프라 코드
```

#### 11.2.3 GR Edu (보안 교육)

```
입력: "CVE-2021-44228 (Log4Shell) 실습하고 싶어"
        ↓
    [GR IaC Lab]
    • 해당 CVE가 발생하는 환경 자동 구축
    • 취약한 버전 + 공격 시나리오 준비
    • 방어 실습까지 포함
        ↓
출력: 즉시 사용 가능한 실습 환경
```

### 11.3 시너지: 순환하는 사업 구조

```
         ┌──────────────────┐
         │   자동화 진단     │
         │  (문제 발견)      │
         └────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             │             ▼
┌───────┐         │         ┌───────┐
│ 보안  │         │         │  IaC  │
│ 교육  │◀────────┼────────▶│       │
└───┬───┘         │         └───┬───┘
    │             ▼             │
    │      ┌───────────┐        │
    └─────▶│ 보안 솔루션 │◀──────┘
           │ (문제 해결) │
           └───────────┘
```

### 11.4 타겟 고객

| 고객 유형 | 니즈 | 제품 | ARR 예상 |
|----------|------|------|----------|
| **중견기업** | 인프라 현황 파악 | 자동화 진단 | $10K~$30K |
| **대기업** | 멀티클라우드 통합 관리 | 진단 + IaC | $50K~$200K |
| **보안 컨설팅사** | GR DB API 사용 | API 라이선스 | $6K~$20K |
| **교육기관** | 보안 실습 환경 | GR Edu | $2K~$10K |

### 11.5 단계별 ARR 목표

| 단계 | 고객 수 | 평균 단가 | ARR 목표 | 누적 투자 |
|------|---------|----------|---------|----------|
| 초기 단계 | 10 | $10K | $100K | $115K |
| 중기 단계 | 50 | $20K | $1M | $600K |
| 확장 단계 | 200 | $25K | $5M | $1.6M |
| 성장기 | 500 | $30K | $15M | $3M |
| 성숙기 | 1,000+ | $50K | $50M+ | $5M |

---

## 12. 실행 로드맵

### Phase 0: 토대 구축 (현재)

**목표**: Framework 설계 완성 + 500개 핵심 제품 DB화

```
작업:
  ✅ 3D 좌표 체계 설계
  ✅ DB 아키텍처 설계
  ✅ 초기 약 500개 atoms 생성
  ⬜ 기본 Atlas 프로토타입

결과물:
  • GR Framework 명세서 완성
  • GR DB v0.1 (500개+ Atom)
```

### Phase 1: MVP 검증 (4주)

**목표**: 웹 애플리케이션 보안 도메인 완성

```
Week 1-2: 인프라 원자 생성
  ├── INFRA-APP-WAS-001 (WAS)
  ├── INFRA-APP-WEBSERVER-001 (Web Server)
  ├── INFRA-DATA-RDBMS-001 (RDBMS)
  └── ... (총 30개)

Week 3: 공격/취약점 원자 생성
  ├── ATK-INJECT-SQL-001 (SQL Injection)
  ├── ATK-INJECT-XSS-001 (XSS)
  └── ... (총 30개)

Week 4: 방어 원자 + 관계 연결
  ├── DEF-PREVENT-* (예방 기법)
  └── RAG 테스트

결과물:
  • 원자 100개
  • 관계 500개 이상
  • 웹 보안 RAG 프로토타입
```

### Phase 2: 확장 (8주)

**목표**: 주요 도메인 확장 + MITRE 매핑

```
Week 1-4: 도메인 확장
  ├── 네트워크 보안 (30개)
  ├── 클라우드 보안 (30개)
  ├── 컨테이너/K8s 보안 (30개)
  └── 인증/인가 (30개)

Week 5-6: MITRE ATT&CK 매핑
  ├── Top 50 Techniques 완전 매핑
  └── 각 기법에 GR 좌표 부여

Week 7-8: D3FEND 연동 + 검증
  ├── 주요 방어 기법 매핑
  └── RAG 성능 A/B 테스트

결과물:
  • 원자 500개
  • MITRE Top 50 완전 매핑
  • RAG 성능 30% 향상 검증
```

### Phase 3: 지능 구축 (12주)

**목표**: AI 서비스 구축

```
Week 1-4: 자체 LLM 파인튜닝
  ├── Llama/Mistral 기반 실험
  └── GR 데이터로 파인튜닝

Week 5-8: 서비스 프로토타입
  ├── 진단 도구 RAG 연동
  ├── 교육 시스템 프로토타입
  └── IaC 생성 실험

Week 9-12: 통합 및 최적화
  ├── 서비스 통합
  └── 프로덕션 준비

결과물:
  • 자체 보안 LLM v1.0
  • 서비스 프로토타입 3개
  • 원자 2000개
```

### Phase 4: 생태계 확장

**목표**: 외부 파트너 생태계 구축

```
작업:
  ⬜ GR DB API 공개
  ⬜ 파트너사 통합
  ⬜ 커뮤니티 기여 모델

결과물:
  • "Powered by GR" 생태계
  • 플랫폼 비즈니스 전환
```

---

## 13. 기술 스택 & 인프라

### 13.1 개발 환경

```yaml
Language: Python 3.11+
Framework: FastAPI (API), Pydantic (Schema)
Database: PostgreSQL, Neo4j (Phase 2)
Vector DB: Pinecone / pgvector
Container: Docker, Kubernetes
CI/CD: GitHub Actions
Documentation: MkDocs
```

### 13.2 AI/LLM 스택

```yaml
원자 생성:
  - Claude API (Anthropic)
  - GPT-4 API (OpenAI)
  - LiteLLM (통합 인터페이스)

RAG 시스템:
  - LangChain / LlamaIndex
  - 자체 임베딩 파이프라인

자체 LLM (목표):
  - Base: Llama 3 / Mistral
  - Fine-tuning: GR 데이터
  - Serving: vLLM / TGI
```

### 13.3 인프라 비용 (초기)

| 항목 | 서비스 | 규모 | 월 비용 | 연 비용 |
|------|--------|------|---------|---------|
| PostgreSQL | AWS RDS | db.t3.medium | $50 | $600 |
| Neo4j | AuraDB Professional | 1 instance | $200 | $2,400 |
| Pinecone | Serverless (100k vectors) | 1 pod | $70 | $840 |
| OpenAI API | Embedding (ada-002) | 100개 제품 | $100 | $1,200 |
| **합계** | - | - | **$420** | **$5,040** |

---

## 14. 위험 요소 & 대응

### 14.1 위험 식별

| 위험 | 확률 | 영향도 | 대응 전략 |
|------|------|--------|----------|
| **데이터 구축 지연** | 높음 | 치명적 | AI 파이프라인 조기 투자, 외주 활용 |
| **초기 자본 부족** | 중간 | 높음 | Phase 0로 PoC 먼저 → 투자 유치 |
| **AI 할루시네이션** | 중간 | 중간 | 전문가 검증 필수화, 신뢰도 점수 표시 |
| **경쟁사 모방** | 낮음 | 중간 | 특허 출원, First-Mover Advantage 극대화 |
| **데이터 최신성 유지 실패** | 중간 | 높음 | 자동 크롤링 + 커뮤니티 기여 모델 |
| **범위 과다** | 높음 | 높음 | 도메인별 단계적 확장 |
| **품질 저하** | 중간 | 높음 | 검증 프로세스 강화 |
| **유지보수 부담** | 중간 | 중간 | 자동화 도구 개발 |

### 14.2 대응 전략

**Plan A (기본 계획)**:
- Phase 0 → PoC → 투자 유치 → Phase 1/2 진행

**Plan B (자본 부족 시)**:
- Phase 0만 완료 → 컨설팅 서비스로 먼저 수익 창출 → 데이터 구축 병행

**Plan C (시장 반응 부진 시)**:
- GR DB를 오픈소스화 → 커뮤니티 기여로 데이터 확충 → API 유료화로 수익

---

## 15. 경쟁 우위 (Competitive Moat)

### 대체 불가능한 해자

**1. Pre-mapped 지식 베이스**
- 경쟁사는 "고객 데이터"를 분석하지만, 우리는 **"세상의 모든 제품"**을 미리 정의해뒀습니다
- 10,000개 제품 × 평균 3개 Archetype = 30,000개 지식 노드
- 이를 따라잡으려면 최소 2년 + 수백만 달러 필요

**2. 3D 좌표계 방법론**
- Layer × Zone × Function 조합은 GR만의 독창적 방법론
- 특허 출원 가능

**3. AI의 Ground Truth**
- 2025년 AI 시대, 모든 보안 솔루션이 AI를 사용하지만 **"정확한 학습 데이터"**가 없습니다
- GR DB는 AI의 할루시네이션을 잡는 유일한 검증된 데이터셋

**4. Network Effect**
- 더 많은 제품이 매핑될수록 → AI가 더 똑똑해짐
- 더 많은 고객이 사용할수록 → 피드백으로 데이터 품질 향상

**5. API Economy**
- GR DB를 다른 보안 솔루션 업체에게 API로 판매 가능
- "Powered by GR Data" 라벨링으로 B2B2B 시장 진출

---

## 16. 거버넌스 & 품질 관리

### 16.1 문서 체계

```
GR_PROJECT/
├── 00_docs/              # 마스터플랜, 가이드
├── 01_vision/            # (레거시 - 통합됨)
├── 02_framework/         # 프레임워크 상세
├── 03_ontology/          # 스키마, 헌법, 분류체계
│   ├── constitution/     # 헌법 (원자화 규칙)
│   ├── schema/           # 스키마 정의
│   └── taxonomy/         # 분류체계
├── 04_knowledge_base/    # 원자 저장소
│   ├── infrastructure/
│   ├── attacks/
│   ├── defenses/
│   └── vulnerabilities/
├── 05_tools/             # 도구
│   ├── generator/        # 원자 생성기
│   ├── validator/        # 검증기
│   └── migrator/         # 마이그레이션
└── 06_applications/      # 응용 (Atlas 등)
```

### 16.2 원자 생성 파이프라인

```
1. 주제 선정
   └── 우선순위 목록에서 선택

2. 자료 수집
   ├── 공식 문서
   ├── MITRE/CWE/CVE
   ├── OWASP
   └── 실무 경험

3. 초안 생성 (Claude/GPT 활용)
   ├── 표준 템플릿 적용
   ├── 정의/개념/관계 생성
   └── 보안 프로파일 작성

4. 검증 및 보완
   ├── 기술적 정확성 검토
   ├── 관계 일관성 확인
   └── 누락 정보 보완

5. 등록 및 연결
   ├── DB 저장
   ├── 기존 원자와 관계 연결
   └── 인덱스 업데이트
```

### 16.3 품질 기준

| 항목 | 기준 | 검증 방법 |
|------|------|-----------|
| 정의 완성도 | what/why/how 모두 작성 | 체크리스트 |
| 관계 밀도 | 최소 5개 관계 | 자동 검증 |
| GR 좌표 | Layer/Zone/Function 모두 지정 | 자동 검증 |
| 보안 정보 | 취약점 또는 방어 최소 3개 | 체크리스트 |
| 출처 명시 | 최소 2개 출처 | 메타데이터 확인 |

### 16.4 변경 관리

- **스키마 변경**: 헌법 수정 절차 적용
- **원자 추가**: PR 리뷰 후 머지
- **관계 수정**: 영향 분석 필수

---

## 17. 성공 지표 (KPI)

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| 원자 수 | Phase 1: 500개, Phase 2: 2000개 | DB count |
| 관계 밀도 | 원자당 평균 5개 이상 관계 | 관계수/원자수 |
| RAG 정확도 | 일반 RAG 대비 30% 향상 | A/B 테스트 |
| 커버리지 | MITRE Top 50 기법 100% 매핑 | 매핑 완료율 |

---

## 18. 핵심 메시지

### 이 프로젝트가 아닌 것

- 또 하나의 보안 제품
- MITRE ATT&CK의 경쟁자
- 단기 수익 프로젝트

### 이 프로젝트가 맞는 것

- 모든 보안 제품의 **토대**
- MITRE ATT&CK의 **보완재** (WHERE + HOW)
- 컨설팅 노하우의 **자산화**
- **확장 가능한** 사업 모델

---

## 결론

> **"우리는 제품을 만들지 않습니다. 모든 보안 제품이 서 있을 토대를 만듭니다."**

GR Framework는 보안 컨설팅 회사가 **"일 ↔ 인력"의 선형 성장**에서 벗어나,
**"Core ↔ 여러 제품"의 확장 가능한 성장**으로 전환하기 위한 프로젝트입니다.

```
Before: 일 10개 = 사람 10명 = 수익 10
After:  Core 1개 = 제품 4개 = 수익 40+
```

이것이 GR Framework의 본질입니다.

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 3.0 | 2026-02-04 | 5개 마스터플랜 문서 통합 |
| - | - | 원본: GR_마스터플랜_비전.md, GR_마스터플랜_아키텍처.md |
| - | - | 원본: GR_생태계_마스터플랜(일반용)v3.1.md |
| - | - | 원본: GR_생태계_마스터플랜_전문용_v2.2.md |
| - | - | 원본: GR_ONTOLOGY_MASTERPLAN_v1.0.md |

---

**문서 끝**
