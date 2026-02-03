# GR 분류 엔진 (Classification Engine) 기획서

> **"혼돈을 질서로, 원석을 보석으로, 그리고 경험을 자산으로"**
>
> 외부의 비정형 데이터를 GR Framework의 3D 좌표계로 정확히 배치하고,
> 그 과정에서 축적된 데이터로 자체 AI를 성장시키는 엔진

---

## Executive Summary

### 핵심 목표
분류 엔진은 **외부 비정형 데이터 → GR 3D 좌표계 매핑**을 수행하는 핵심 엔진으로, **4계층 Intelligent Ingestion 파이프라인**과 **Data Flywheel 전략**을 통해 장기적으로 자체 AI를 확보합니다.

### v1.3 핵심 변경사항
- **4계층 파이프라인**: Intake Router → Format Parser → AI Structurer → AI Classifier
- **AI 투입 지점 명확화**: Layer 1(의미 분할), Layer 2(좌표 분류)에만 AI 사용
- **비용 최적화**: 정형 데이터는 AI Structurer 스킵, 저비용 모델 활용

### 주요 지표 (KPI)
| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| **Layer 정확도** | ≥ 95% | 사람 검수 결과 대비 |
| **Zone 정확도** | ≥ 92% | 사람 검수 결과 대비 |
| **Primary Tag 정확도** | ≥ 90% | 사람 검수 결과 대비 |
| **UNKNOWN 비율** | < 15% | 전체 분류 중 |
| **자동 승인률** | ≥ 50% | Confidence ≥90% |

```

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 분류 엔진 (Classification Engine) 기획서 |
| **버전** | v1.3 |
| **작성일** | 2025-11-28 |
| **수정일** | 2025-12-01 |
| **목적** | 분류 엔진의 존재 이유, **4계층 Intelligent Ingestion 파이프라인**, Data Flywheel 전략, 보안/품질 기준 정립 |
| **대상 독자** | 기획자, 아키텍트, 개발팀 |
| **연관 문서** | Engine A 종합 계획서_v1.0.md, 00_분류체계_개요.md, 01_schema.sql |
| **구현 환경** | Ubuntu + Python |

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2025-11-28 | 최초 작성 (규칙 기반 분류 설계) |
| v1.1 | 2025-12-01 | LLM 기반 분류 + Data Flywheel 전략 추가 |
| v1.2 | 2025-12-01 | Dynamic Few-shot, UNKNOWN 태그, 보안/PII/멀티테넌트 고려 |
| v1.3 | 2025-12-01 | **4계층 Intelligent Ingestion 파이프라인, Intake Router, AI Structurer 명확화** |

---

## 1. 서론: 분류 엔진은 왜 필요한가?

### 1.1 Engine A에서의 위치

Engine A(GR Core Orchestrator)는 **2개의 핵심 축**을 가집니다:

```
┌────────────────────────────────────────────────────────────┐
│                   Engine A (GR Core Orchestrator)          │
│                                                            │
│   ┌─────────────────────┐    ┌─────────────────────┐      │
│   │   분류 엔진          │    │   추출 엔진          │      │
│   │   (Classification)   │    │   (Extraction)       │      │
│   │                     │    │                     │      │
│   │   "데이터 적재"      │    │   "데이터 조회"      │      │
│   │   외부 → 내부        │    │   내부 → 외부        │      │
│   └─────────────────────┘    └─────────────────────┘      │
│                                                            │
│            ↓ 본 문서의 범위                                 │
└────────────────────────────────────────────────────────────┘
```

**분류 엔진은 Engine A의 첫 번째 축으로**, 외부 세계의 다양한 데이터를 GR Framework의 표준 체계로 변환하여 DB에 적재하는 역할을 담당합니다.

### 1.2 분류 엔진 없이 발생하는 문제

#### 문제 1: 데이터 파편화
> "CVE-2024-12345는 NVD에서 가져왔고, CVE-2024-12346은 수동 입력했는데, 형식이 달라서 통합 분석이 안 됩니다."

- 소스마다 다른 데이터 포맷
- 같은 취약점이 다른 형태로 중복 저장
- 자동화된 분석 결과의 신뢰도 붕괴

#### 문제 2: 좌표 부재
> "Log4Shell 취약점이 어느 Layer에 해당하는지, 어느 Zone에 영향을 주는지 모릅니다."

- 취약점과 인프라 분류 체계의 연결 고리 부재
- 영향 범위 파악 불가
- 방어 전략 수립 곤란

#### 문제 3: 제품-취약점 매핑 혼란
> "Redis와 redis-server, REDIS는 같은 제품인데, DB에 3개의 별도 레코드로 존재합니다."

- 제품명 표기 불일치 (대소문자, 축약어, 버전 포함 여부)
- CPE 정규화 미흡
- 취약점-제품 매핑 누락 또는 중복

#### 문제 4: 규칙 기반 분류의 한계 (v1.1 추가)
> "새로 나온 'Valkey'라는 Redis 포크를 파서가 인식하지 못합니다."

- 규칙 기반 파서는 **추론 능력이 없음**
- 새로운 제품/취약점 유형에 대응 불가
- 문맥을 이해하지 못해 오분류 빈번

#### 문제 5: 파서의 형식 의존성 (v1.3 추가)
> "raw를 쪼개긴 하는데 우리가 원하는 방식으로 쪼개지지 않거나 형식에 구애를 받습니다."

- 줄바꿈(`\n`)이나 헤더(`##`) 기준으로 자르면 내용이 이어지는데도 잘리거나, 다른 내용이 섞임
- 규칙 기반 파서는 "의미 단위"를 이해하지 못함
- 물리적 구조(페이지, 섹션)와 의미적 구조(개념, 취약점)가 일치하지 않음

### 1.3 분류 엔진의 정의

**분류 엔진(Classification Engine)** 은 이러한 문제를 해결하기 위해:

1. **다양한 소스**의 비정형 데이터를 수신하고
2. **(v1.3) Intake Router**가 데이터 성격에 따라 처리 경로를 결정하며
3. **(v1.3) AI Structurer**가 의미 단위로 분할하고
4. **AI Classifier**가 GR 3D 좌표(Layer × Zone × Tag)를 할당하며
5. **중복/충돌을 처리**하여 DB에 적재하고
6. **이 과정을 학습 데이터로 축적**하여 자체 AI 성장의 기반을 마련합니다

---

## 2. 분류 대상: 무엇을 분류하는가?

### 2.1 분류 대상 개요

분류 엔진은 **2가지 핵심 대상**을 분류합니다:

| 대상 | 설명 | 예시 |
|------|------|------|
| **취약점 (Vulnerability)** | 보안 결함 및 위협 정보 | CVE, CWE, OWASP Top 10, Named Vulnerabilities |
| **제품 (Product)** | IT 인프라 구성요소 | Nginx, PostgreSQL, AWS EC2, OpenAI API |

```
┌─────────────────────────────────────────────────────────────┐
│                     분류 대상                                │
├─────────────────────────────┬───────────────────────────────┤
│        취약점               │          제품                  │
│    (Vulnerability)          │       (Product)               │
├─────────────────────────────┼───────────────────────────────┤
│ • CVE (공식 취약점)          │ • 소프트웨어 (Nginx, Redis)   │
│ • CWE (취약점 유형)          │ • 하드웨어 (서버, 네트워크)    │
│ • OWASP Top 10             │ • 클라우드 서비스 (AWS, GCP)   │
│ • Named (Heartbleed 등)     │ • SaaS (OpenAI, Salesforce)  │
│ • MITRE ATT&CK 기법         │ • 오픈소스 (Log4j, Spring)    │
└─────────────────────────────┴───────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   상호 참조 관계     │
              │  (N:M Mapping)      │
              │                     │
              │ 취약점 ←→ 제품      │
              │ CVE ←→ Tech Stack  │
              └─────────────────────┘
```

### 2.2 분류 대상 1: 취약점 (Vulnerability)

#### 2.2.1 취약점의 종류

| 종류 | 설명 | 출처 | 예시 |
|------|------|------|------|
| **CVE** | 공식 등록된 개별 취약점 | NVD, MITRE | CVE-2021-44228 (Log4Shell) |
| **CWE** | 취약점 유형/패턴 분류 | MITRE | CWE-79 (XSS), CWE-89 (SQL Injection) |
| **OWASP Top 10** | 웹 애플리케이션 주요 위협 | OWASP | A01:2021 - Broken Access Control |
| **Named Vulnerability** | 별칭이 붙은 유명 취약점 | 보안 커뮤니티 | Heartbleed, Shellshock, Log4Shell |
| **MITRE ATT&CK** | 공격 기법 분류 체계 | MITRE | T1190 (Exploit Public-Facing App) |
| **추가 가능** | 이후 추가 가능 | 

#### 2.2.2 취약점에 부여할 GR 좌표

취약점은 **영향받는 인프라 계층**과 **공격 가능한 보안 영역**에 따라 3D 좌표가 부여됩니다:

```yaml
CVE-2021-44228 (Log4Shell):
  차원 1 (Layer):
    - Layer 7 (Application) - 주 영향
    - Layer 6 (Runtime) - Java Runtime 영향
  차원 2 (Zone):
    - Zone 2 (Application Zone) - 애플리케이션 영역
    - Zone 0-A (Untrusted External) - 외부 공격 가능
  차원 3 (Tag):
    - A1.5 (Backend Server)
    - T1.2 (Java Runtime)
    - S1.3 (RCE Vulnerability)
  MITRE ATT&CK:
    - T1190 (Exploit Public-Facing Application)
    - T1059 (Command and Scripting Interpreter)
```

#### 2.2.3 취약점 분류의 목적

1. **영향 범위 파악**: 어떤 Layer/Zone이 위험에 노출되는가?
2. **우선순위 결정**: 어떤 취약점을 먼저 패치해야 하는가?
3. **방어 전략 수립**: 어떤 Zone 경계에서 차단할 수 있는가?
4. **교육 콘텐츠 연결**: 해당 취약점을 설명하는 교육 모듈은?

### 2.3 분류 대상 2: 제품 (Product)

#### 2.3.1 제품의 종류

| 종류 | 설명 | 예시 |
|------|------|------|
| **소프트웨어** | 설치형 애플리케이션 | Nginx, PostgreSQL, Redis, Apache |
| **라이브러리/프레임워크** | 개발 의존성 | Log4j, Spring, React, Django |
| **클라우드 서비스** | IaaS/PaaS | AWS EC2, GCP GKE, Azure Functions |
| **SaaS** | 외부 호스팅 서비스 | Salesforce, GitHub, OpenAI API |
| **하드웨어** | 물리 장비 | Cisco Router, Dell Server, Fortinet FW |
| **운영체제** | OS 및 런타임 | Ubuntu, Windows Server, Alpine Linux |

#### 2.3.2 제품에 부여할 GR 좌표

제품은 **배포 위치**와 **수행 기능**에 따라 3D 좌표가 부여됩니다:

```yaml
PostgreSQL:
  차원 1 (Layer): Layer 5 (Data Services)
  차원 2 (Zone): Zone 3 (Data Zone)
  차원 3 (Tag):
    Primary: D1.3 (Relational Storage)
    Secondary:
      - D5.2 (Vector Search) - pgvector 사용 시
      - S4.1 (Encryption at Rest) - TDE 활성화 시
    Tech Stack: T2.1 (SQL Database)
    Interface: I1.2 (TCP/PostgreSQL Protocol)
```

#### 2.3.3 제품 정규화의 필요성

같은 제품이 다양한 이름으로 불릴 수 있습니다:

| 정규 이름 | 별칭들 |
|----------|--------|
| PostgreSQL | postgres, pgsql, POSTGRESQL, pg |
| Nginx | nginx, NGINX, nginx-plus |
| Redis | redis, Redis, redis-server, REDIS |
| OpenAI GPT-4 | gpt-4, GPT4, openai-gpt-4 |

분류 엔진은 **LLM의 추론 능력**을 활용하여 문맥을 이해하고, 다양한 표기를 **정규 이름(Canonical Name)** 으로 통일합니다.

---

## 3. 핵심 전략: Data Flywheel

### 3.1 전략 개요

> **"현재는 LLM의 강력한 추론 능력을 빌려 쓰고, 그 결과를 쌓아서 나만의 AI를 만든다"**

이것이 **Data Flywheel (데이터 선순환)** 전략입니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Data Flywheel 전략                               │
└─────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐
     │  1. LLM 분류  │ ←── 외부 LLM (GPT-4, Claude) 활용
     │  (고비용)     │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ 2. 결과 저장  │ ←── 모든 분류 결과를 구조화하여 저장
     │ (학습 데이터) │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ 3. 사람 검수  │ ←── Human-in-the-loop: 정답 확정
     │ (품질 보증)   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ 4. 데이터 축적│ ←── 수천 건의 [입력 → 정답] 쌍
     │ (자산화)     │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ 5. 자체 모델  │ ←── Fine-tuned 모델 학습
     │ (저비용/고속) │     (Llama, Mistral 등)
     └──────────────┘

            ↓ 결과

     ┌──────────────────────────────────────────────────────────┐
     │  초기: LLM 의존 100% (고비용)                             │
     │  중기: 규칙 70% + LLM 30% (비용 절감)                     │
     │  장기: 자체 모델 90% + LLM 10% (Edge Case만)             │
     └──────────────────────────────────────────────────────────┘
```

### 3.2 왜 이 전략인가?

#### 규칙 기반 분류의 한계

| 문제 | 설명 |
|------|------|
| **추론 불가** | "Redis"와 "redis-server"가 같은 제품인지 판단 못함 |
| **문맥 무시** | "Log4j RCE"에서 CVE-2021-44228을 연결 못함 |
| **확장성 부재** | 새로운 유형마다 규칙 추가 필요 |
| **오류 빈발** | 오타, 비표준 표기 → 분류 실패 |

#### LLM 활용의 장점

| 장점 | 설명 |
|------|------|
| **추론 능력** | 문맥을 이해하여 유연한 분류 |
| **새 유형 대응** | 처음 보는 제품/취약점도 유사성 기반 판단 |
| **정규화 우수** | 다양한 표기를 통일된 이름으로 매핑 |

#### 자체 모델의 필요성

| 이유 | 설명 |
|------|------|
| **비용 절감** | 외부 API 비용 제거 (건당 과금 X) |
| **속도 향상** | 자체 호스팅으로 지연 시간 단축 |
| **일관성 보장** | 같은 입력 → 같은 출력 보장 |
| **독자적 자산** | 외부 의존 없는 핵심 역량 확보 |

### 3.3 무엇을 저장해야 하는가?

> **중요 구분: 본업(분류) vs 학습 데이터**
>
> - **본업 목적**: 취약점/제품을 분류하여 `vulnerabilities`, `products` 등 비즈니스 테이블에 적재
> - **학습 데이터 목적**: 분류 과정을 로깅하여 미래 Fine-tuning에 활용
>
> 두 목적은 병렬로 진행되며, 학습 데이터 수집이 본업을 방해하지 않아야 합니다.

Fine-tuned 모델 학습을 위해 **`[질문(Input)] → [정답(Output)]`** 쌍이 필요합니다.

**반드시 저장해야 할 3가지:**

| 데이터 | 설명 | 예시 |
|--------|------|------|
| **Raw Input** | 원본 텍스트 | 크롤링한 CVE 설명, 제품 문서 |
| **LLM Input** | 실제 프롬프트 | "이 취약점의 Layer/Zone/Tag는?" |
| **Final Verified Output** | **확정된 정답** | 사람이 검수했거나 자동 승인된 결과 |

> **핵심**: LLM이 뱉은 답변을 그대로 저장하는 게 아니라, **"이게 맞다"고 판명된 최종 결과**를 저장해야 합니다.

---

## 4. 핵심 아키텍처: 4계층 Intelligent Ingestion 파이프라인 (v1.3 신규)

### 4.1 전체 파이프라인 개요

```
┌─────────────────────────────────────────────────────────────────────────┐
│            4계층 Intelligent Ingestion 파이프라인 (v1.3)                  │
└─────────────────────────────────────────────────────────────────────────┘

[크롤러 / 외부 입력]
       │
       │  메타데이터 태깅 (AI 불필요):
       │  - source_type: "NVD_API", "EXPLOIT_DB", "SECURITY_BLOG"
       │  - format: "JSON", "HTML", "PDF"
       │  - url, size, timestamp
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Layer -1: Intake Router (규칙 기반)                                       │
│                                                                          │
│  "메타데이터를 보고 어떤 경로(Track)로 처리할지 결정"                        │
│  AI 필요: ❌                                                              │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        라우팅 규칙                               │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │ 정형 API 응답 (NVD JSON)     → Track A: L0 → L2 (L1 스킵)       │    │
│  │ 구조화된 CSV/Excel           → Track A: L0 → L2 (L1 스킵)       │    │
│  │ 비정형 문서 (HTML/PDF/MD)    → Track B: L0 → L1 → L2            │    │
│  │ 짧은 텍스트 (수동 입력)       → Track C: 바로 L2                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
   [Track A]         [Track B]         [Track C]
   정형 데이터        비정형 문서        짧은 텍스트
       │                 │                 │
       ▼                 ▼                 │
┌──────────────────────────────────────────┐│
│ Layer 0: Format Parser (도구/라이브러리)  ││
│                                          ││
│  "형식 깨지 않고 텍스트 추출"              ││
│  AI 필요: ❌ | 비용: $0                   ││
│                                          ││
│  JSON → json lib                         ││
│  HTML → BeautifulSoup                    ││
│  PDF  → pdfplumber                       ││
│  CSV  → pandas                           ││
└──────────────────────────────────────────┘│
       │                 │                 │
       │                 ▼                 │
       │  ┌────────────────────────────────┐│
       │  │ Layer 1: AI Structurer         ││
       │  │                                ││
       │  │ "의미 단위로 분할 + 노이즈 제거" ││
       │  │ AI 필요: ✅ (저비용 모델)       ││
       │  │ 모델: gpt-4o-mini, claude-haiku││
       │  │ 비용: ~$0.01/raw               ││
       │  │                                ││
       │  │ - 광고, 서론, 인삿말 제거       ││
       │  │ - 의미 단위로 분할              ││
       │  │ - unit_type 태깅               ││
       │  └────────────────────────────────┘│
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Layer 2: AI Classifier (고성능 모델)                                      │
│                                                                          │
│  "GR 3D 좌표 할당 (Layer × Zone × Tag)"                                   │
│  AI 필요: ✅ (고성능 모델)                                                │
│  모델: gpt-4o, claude-3.5-sonnet                                         │
│  비용: ~$0.03/unit                                                       │
│                                                                          │
│  - Dynamic Few-shot (Pinecone 연동)                                      │
│  - UNKNOWN 태그 허용 (Hallucination 방지)                                 │
│  - 자동 검증 + Human Review                                              │
└──────────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
                [GR Database Cluster]
                PostgreSQL + Neo4j + Pinecone
```

### 4.2 각 계층의 책임과 AI 필요 여부

| 계층 | 명칭 | 책임 | AI 필요 | 비용 |
|------|------|------|---------|------|
| **Layer -1** | Intake Router | 메타데이터 → Track 결정 | ❌ 규칙 기반 | $0 |
| **Layer 0** | Format Parser | 형식 → 텍스트 추출 | ❌ 라이브러리 | $0 |
| **Layer 1** | AI Structurer | 텍스트 → 의미 단위 분할 | ✅ 저비용 LLM | ~$0.01/raw |
| **Layer 2** | AI Classifier | 의미 단위 → GR 좌표 | ✅ 고성능 LLM | ~$0.03/unit |

### 4.3 왜 4계층인가? (설계 철학)

#### 책임 분리 원칙

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   크롤러     │     │   라우터     │     │  구조화기    │     │   분류기    │
│             │     │             │     │             │     │             │
│ "가져오기"   │ →  │ "경로 결정"  │ →  │ "쪼개기"    │ →  │ "좌표 할당" │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    수집 책임          라우팅 책임          분할 책임          분류 책임
```

#### AI 투입 지점 최적화

| 작업 | 규칙으로 가능? | AI 필요? | 결정 |
|------|--------------|---------|------|
| PDF → 텍스트 추출 | ✅ pdfplumber | ❌ | Layer 0 (도구) |
| JSON 파싱 | ✅ json lib | ❌ | Layer 0 (도구) |
| "어디까지가 한 취약점 설명인지" 판단 | ❌ 문맥 이해 필요 | ✅ | Layer 1 (AI) |
| GR 좌표 할당 | ❌ 도메인 지식 필요 | ✅ | Layer 2 (AI) |

#### 학습 데이터 분리

```
Layer 1 학습: "좋은 Chunking" 데이터셋 → Chunking 전용 모델
Layer 2 학습: "좋은 Classification" 데이터셋 → Classification 전용 모델
```

→ 나중에 각각 Fine-tuning 가능

---

## 5. Layer -1: Intake Router 상세 (v1.3 신규)

### 5.1 크롤러가 붙이는 메타데이터

크롤러는 AI 없이도 다음 메타데이터를 수집합니다:

| 메타데이터 | 예시 | 수집 방법 |
|-----------|------|----------|
| `source_type` | "NVD_API", "EXPLOIT_DB", "SECURITY_BLOG" | 크롤러 설정에서 지정 |
| `format` | "JSON", "HTML", "PDF" | Content-Type 헤더 또는 확장자 |
| `url` | "https://nvd.nist.gov/..." | 요청 URL |
| `page_size` | 15000 | 응답 크기 (bytes) |
| `has_structure` | true/false | JSON/XML 파싱 성공 여부 |
| `crawl_config` | "nvd_cve_feed" | 어떤 크롤링 작업인지 |

### 5.2 라우팅 규칙

```python
class IntakeRouter:
    def route(self, raw_input: RawInput) -> ProcessingTrack:
        # 1. 소스 유형 기반 판단
        if raw_input.source_type in ['NVD_API', 'CVE_JSON', 'CPE_DICT']:
            return Track.A  # 정형 → Layer 0 → Layer 2 (Layer 1 스킵)

        if raw_input.source_type == 'MANUAL_INPUT':
            if len(raw_input.text) < 500:  # 짧은 텍스트
                return Track.C  # 바로 Layer 2
            else:
                return Track.B  # 길면 Layer 1 필요

        # 2. 파일 형식 기반 판단
        if raw_input.format in ['JSON', 'YAML', 'CSV', 'XML']:
            if self._is_well_structured(raw_input):
                return Track.A
            else:
                return Track.B  # JSON이지만 비정형 텍스트 포함

        if raw_input.format in ['HTML', 'PDF', 'MARKDOWN', 'DOCX']:
            return Track.B  # 비정형 → Layer 0 + 1 + 2

        # 3. 기본값: 안전하게 전체 파이프라인
        return Track.B
```

### 5.3 라우팅 테이블

| 소스 유형 | 형식 | 트랙 | 경로 | 이유 |
|----------|------|------|------|------|
| NVD API | JSON | A | L0 → L2 | 이미 CVE 1건 = 1 레코드로 정형화됨 |
| CPE Dictionary | JSON | A | L0 → L2 | 제품 1건 = 1 레코드 |
| Exploit-DB | HTML | B | L0 → L1 → L2 | 페이지에 여러 정보 혼재 |
| 보안 블로그 | HTML | B | L0 → L1 → L2 | 광고, 서론 제거 필요 |
| PDF 보고서 | PDF | B | L0 → L1 → L2 | 다중 섹션, 의미 분할 필요 |
| 관리자 수동입력 (짧음) | Text | C | → L2 | 이미 단일 개념으로 입력됨 |
| 관리자 수동입력 (김) | Text | B | L1 → L2 | 의미 분할 필요할 수 있음 |
| 자산 대장 | Excel | A | L0 → L2 | 1행 = 1 제품으로 정형화됨 |

### 5.4 Track 정의

```yaml
Track A (정형 데이터):
  경로: Layer 0 → Layer 2
  특징: Layer 1 스킵 (이미 1 raw = 1 unit으로 정형화)
  예시: NVD JSON, CPE, 자산 대장
  비용: ~$0.03/raw

Track B (비정형 문서):
  경로: Layer 0 → Layer 1 → Layer 2
  특징: 전체 파이프라인 통과, 1 raw = N units
  예시: HTML, PDF, Markdown, 긴 텍스트
  비용: ~$0.01 + $0.03×N/raw

Track C (짧은 텍스트):
  경로: 바로 Layer 2
  특징: Layer 0, 1 모두 스킵
  예시: 수동 입력된 짧은 설명 (<500자)
  비용: ~$0.03/raw
```

---

# 동적 트랙 전환 섹션 (v1.3 기획서에 추가할 내용)

**위치**: 5.4 Track 정의 다음, 6. Layer 0 이전 (585번 줄 이후)

---

### 5.5 동적 트랙 전환 (Fallback Logic) - v1.3 추가

초기 Track 배정이 잘못된 경우, **Layer 0 결과를 기반으로 트랙을 재조정**합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                     동적 트랙 전환 흐름도                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Track A (정형) ──► Layer 0 ──► 파싱 결과 검증                  │
│         │                              │                        │
│         │                    ┌─────────┴─────────┐              │
│         │                    ▼                   ▼              │
│         │              [예상대로 정형]      [예상과 다름]         │
│         │                    │                   │              │
│         │                    ▼                   ▼              │
│         │               → Layer 2           Track B로 전환       │
│         │                                        │              │
│         │                                        ▼              │
│         │                                   → Layer 1 → L2      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.5.1 전환 트리거 조건

| 조건 | 초기 Track | 전환 후 | 이유 |
|------|-----------|--------|------|
| JSON/CSV인데 중첩 텍스트 필드 발견 | A | B | 의미 분할 필요 |
| 정형인데 예상 스키마와 불일치 | A | B | AI 구조화 필요 |
| 짧은 텍스트인데 실제 500자 초과 | C | B | 의미 분할 필요 |
| HTML인데 구조화된 테이블만 존재 | B | A | 이미 정형화됨 |
| 파싱 실패 (손상된 파일) | 모두 | ERROR | 수동 검토 필요 |

#### 5.5.2 Layer 0 검증 로직

```python
@dataclass
class Layer0Result:
    parsed: ParsedDocument
    quality_score: float          # 0.0 ~ 1.0
    structure_type: str           # "structured", "semi", "unstructured"
    needs_ai_structuring: bool    # True면 Track B로 전환

def evaluate_layer0_result(result: Layer0Result, initial_track: str) -> str:
    """Layer 0 결과를 평가하여 트랙 재결정"""

    # Track A → B 전환 조건
    if initial_track == 'A':
        if result.needs_ai_structuring:
            return 'B'  # Layer 1 필요
        if result.quality_score < 0.7:
            return 'B'  # 스키마 불일치

    # Track C → B 전환 조건
    if initial_track == 'C':
        if len(result.parsed.raw_text) > 500:
            return 'B'  # 길이 초과

    # Track B → A 전환 조건 (최적화)
    if initial_track == 'B':
        if result.structure_type == 'structured' and result.quality_score > 0.9:
            return 'A'  # 이미 정형화됨

    # 파싱 실패
    if result.quality_score < 0.3:
        return 'ERROR'

    return initial_track  # 유지
```

#### 5.5.3 needs_ai_structuring 판단 기준

```python
def check_needs_ai_structuring(parsed: ParsedDocument) -> bool:
    """정형 데이터지만 AI 구조화가 필요한지 판단"""

    # 1. 텍스트 필드에 긴 설명이 포함된 경우
    for field in parsed.text_fields:
        if len(field) > 200 and contains_multiple_concepts(field):
            return True

    # 2. description 필드가 복잡한 경우 (문장 5개 이상)
    if 'description' in parsed.metadata:
        if count_sentences(parsed.metadata['description']) > 5:
            return True

    # 3. 예상 스키마와 실제 구조 불일치
    if parsed.schema_match_score < 0.8:
        return True

    return False
```

#### 5.5.4 전환 로그 테이블 확장

```sql
-- intake_log에 트랙 전환 이력 추가
ALTER TABLE intake_log ADD COLUMN initial_track VARCHAR(10);
ALTER TABLE intake_log ADD COLUMN track_switched BOOLEAN DEFAULT FALSE;
ALTER TABLE intake_log ADD COLUMN switch_reason VARCHAR(200);
```

#### 5.5.5 비용 영향

| 시나리오 | 비용 변화 | 비고 |
|---------|----------|------|
| A → B 전환 | +$0.01/raw | Layer 1 추가 실행 |
| B → A 전환 | -$0.01/raw | Layer 1 스킵 |
| C → B 전환 | +$0.01/raw | Layer 1 추가 실행 |
| 전환율 5% 가정 | 전체 +2~3% | 정확도 향상으로 상쇄 |

**핵심 원칙**: 비용보다 **분류 정확도**가 중요. 잘못된 Track으로 처리하면 최종 분류 품질이 떨어짐.

---

**적용 방법**: 이 내용을 `Engine B_분류엔진_기획서_v1.3.md` 파일의 585번 줄 (Track C 정의 끝) 이후, "## 6. Layer 0: Format Parser 상세" 이전에 삽입하세요.


---

## 6. Layer 0: Format Parser 상세

### 6.1 역할

- **목적**: 다양한 파일 형식에서 텍스트 + 구조 정보 추출
- **AI 필요**: ❌ (도구/라이브러리 사용)
- **비용**: $0

### 6.2 형식별 파서

| 형식 | 라이브러리 | 추출 대상 |
|------|-----------|----------|
| JSON/YAML | `json`, `pyyaml` | 필드 값, 구조 |
| HTML | `BeautifulSoup` | `<main>` 텍스트, 메뉴/광고 제외 |
| PDF | `pdfplumber` | 페이지별 텍스트, 표 |
| CSV/Excel | `pandas` | 행/열 데이터 |
| Markdown | `markdown-it` | 섹션, 코드블럭 |
| DOCX | `python-docx` | 단락, 표 |

### 6.3 출력 형식

```python
@dataclass
class ParsedDocument:
    source_format: str              # "PDF", "HTML", "JSON"
    raw_text: str                   # 추출된 전체 텍스트
    sections: List[Section]         # 섹션/페이지 정보
    tables: List[Table]             # 표 데이터 (있는 경우)
    metadata: dict                  # 페이지 수, 인코딩 등
```

---

## 7. Layer 1: AI Structurer 상세 (v1.3 신규)

### 7.1 역할

- **목적**: 텍스트를 **의미 단위(Semantic Unit)**로 분할 + 노이즈 제거
- **AI 필요**: ✅ (저비용 모델)
- **모델**: `gpt-4o-mini`, `claude-3-haiku`
- **비용**: ~$0.01/raw

### 7.2 왜 AI가 필요한가?

```
규칙 기반 파서의 한계:
- 줄바꿈(`\n`)이나 헤더(`##`) 기준으로 자름
- "어디까지가 한 취약점 설명인지" 모름
- 문맥을 무시하고 물리적 구조만 봄

AI Structurer의 장점:
- "여기까지가 Redis 설명, 여기서부터는 Nginx 설명" 이해
- 광고, 서론, 인삿말을 문맥으로 판단하여 제거
- 의미 단위로 정확히 분할
```

### 7.3 프롬프트 설계

```
너는 보안 문서를 읽고 '분류 단위(classification_unit)'로 분할하는 전문가야.

## 분할 규칙
1. 각 단위는 하나의 개념만 포함해야 한다:
   - 하나의 취약점 설명
   - 하나의 제품/구성요소 설명
   - 하나의 공격 시나리오
2. 광고, 서론, 인삿말, 저작권 문구는 제거한다.
3. 요약하지 말고 원문을 그대로 **발췌(Extract)**한다.
4. 한 문단에 여러 개념이 섞여 있으면 분리한다.

## unit_type 선택지
- "VULNERABILITY": 취약점 설명
- "INFRA_COMPONENT": 인프라 구성요소 설명
- "SECURITY_CONTROL": 보안 통제 설명
- "ATTACK_SCENARIO": 공격 시나리오
- "PRODUCT": 제품/서비스 설명
- "MISC": 기타

## 출력 형식 (JSON)
{
  "units": [
    {
      "unit_type": "VULNERABILITY",
      "title": "Log4Shell Remote Code Execution",
      "raw_text": "Apache Log4j2 2.0-beta9 through 2.14.1...",
      "source_section": "3.1 Critical Vulnerabilities"
    },
    ...
  ],
  "removed_noise": ["광고 배너 텍스트", "뉴스레터 구독 안내"]
}
```

### 7.4 출력 예시

**입력 (HTML에서 추출된 텍스트):**
```
안녕하세요, 보안 뉴스입니다.
오늘 알아볼 건 두 가지 취약점입니다.

[광고] 최고의 보안 솔루션 SecurePro!

첫 번째는 Log4Shell입니다. Apache Log4j2 2.0-beta9 through 2.14.1 버전에서
발견된 원격 코드 실행 취약점으로...

두 번째는 Spring4Shell입니다. Spring Framework 5.3.0 ~ 5.3.17 버전에서...

뉴스레터 구독하기 | 연락처: security@news.com
```

**AI Structurer 출력:**
```json
{
  "units": [
    {
      "unit_type": "VULNERABILITY",
      "title": "Log4Shell",
      "raw_text": "Apache Log4j2 2.0-beta9 through 2.14.1 버전에서 발견된 원격 코드 실행 취약점으로...",
      "source_section": "본문 첫 번째 취약점"
    },
    {
      "unit_type": "VULNERABILITY",
      "title": "Spring4Shell",
      "raw_text": "Spring Framework 5.3.0 ~ 5.3.17 버전에서...",
      "source_section": "본문 두 번째 취약점"
    }
  ],
  "removed_noise": [
    "[광고] 최고의 보안 솔루션 SecurePro!",
    "뉴스레터 구독하기 | 연락처: security@news.com",
    "안녕하세요, 보안 뉴스입니다."
  ]
}
```

→ **1 raw data → 2 units 생성**

### 7.5 비용 최적화

| 항목 | 설정 |
|------|------|
| **모델** | `gpt-4o-mini` (가장 저렴) |
| **최대 토큰** | 입력 8K, 출력 2K |
| **예상 비용** | raw당 ~$0.01 |
| **Track A 스킵** | 정형 데이터는 Layer 1 생략 → 비용 절약 |

---

## 8. Layer 2: AI Classifier 상세

### 8.1 역할

- **목적**: 각 classification_unit에 GR 3D 좌표 할당
- **AI 필요**: ✅ (고성능 모델)
- **모델**: `gpt-4o`, `claude-3.5-sonnet`
- **비용**: ~$0.03/unit

### 8.2 Dynamic Few-shot 전략

> **핵심 아이디어**: 분류할 때마다 Pinecone에서 유사한 "Golden Sample"을 검색하여 프롬프트에 예시로 삽입

#### Golden Sample이란?

- **정의**: 사람이 검수하여 **정확하다고 확인된** 분류 결과
- **출처**: `human_annotation` 테이블에서 `is_verified = TRUE`인 샘플
- **저장**: Pinecone에 `input_text`를 임베딩하여 저장

#### Dynamic Few-shot 워크플로우

```
1. 새 입력 텍스트 수신
   → "Kubernetes pod의 RBAC 권한 설정 오류로 인한 권한 상승 취약점"

2. Pinecone에서 유사한 Golden Sample 검색 (Top 3)
   → 유사도 0.92: "EKS pod의 IAM role 권한 상승"
   → 유사도 0.87: "Docker container privilege escalation"
   → 유사도 0.84: "OpenShift RBAC misconfiguration"

3. 검색된 예시를 프롬프트에 삽입
   → few_shot_examples = [
       {"input": "EKS pod...", "output": {"layer": "L6", "zone": "Z2", ...}},
       {"input": "Docker container...", "output": {"layer": "L6", "zone": "Z2", ...}},
       ...
     ]

4. LLM이 예시를 참고하여 분류
   → 일관된 분류 기준 적용
```

### 8.3 UNKNOWN 태그 처리

> **문제**: LLM이 무조건 답을 만들려고 Hallucination 발생
> **해결**: "모르겠으면 UNKNOWN이라고 해도 된다"고 명시적으로 허용

#### UNKNOWN 사용 규칙

```yaml
UNKNOWN 허용 차원:
  - Layer: "UNKNOWN_LAYER"
  - Zone: "UNKNOWN_ZONE"
  - Primary Tag: "UNKNOWN_TAG"

UNKNOWN 발생 시 처리:
  - 자동 거부 → 리뷰 큐로 이동
  - 사람이 직접 분류 (최고 품질 학습 데이터)
  - 또는 정말 분류 불가능한 경우 폐기
```

#### UNKNOWN 비율 모니터링

| UNKNOWN 비율 | 상태 | 조치 |
|-------------|------|------|
| < 5% | **정상** | 유지 |
| 5% ~ 15% | **주의** | 프롬프트/예시 검토 |
| > 15% | **경고** | 근본 원인 분석 필요 (데이터 품질? 분류 체계?) |

### 8.4 분류 결과 검증

| Confidence Score | 규칙 검증 | UNKNOWN | 처리 방법 |
|------------------|----------|---------|----------|
| ≥ 90% | 통과 | 없음 | **자동 승인** → 바로 학습 데이터 |
| 70% ~ 89% | 통과 | 없음 | **리뷰 큐** → 사람 검수 대기 |
| < 70% | - | - | **거부** → 재분류 또는 폐기 |
| - | - | 있음 | **리뷰 큐** → 사람이 직접 분류 |
| - | 실패 | - | **리뷰 큐** → 사람 검수 필요 |

### 8.5 Human Review (사람 검수)

리뷰 큐에 있는 데이터를 전문가가 검토합니다.

**리뷰 UI 구성:**
```
┌─────────────────────────────────────────────────────────────┐
│                        리뷰 화면                             │
├────────────────────────────┬────────────────────────────────┤
│      [원본 텍스트]          │        [LLM 분류 결과]          │
│                            │                                │
│  "Apache Log4j2 2.0-beta9  │  Layer: [L7 ▼] [L6 ▼]         │
│   through 2.14.1 JNDI      │  Zone:  [Z2 ▼] [Z0-A ▼]       │
│   features used in         │  Primary Tag: [A1.5 ▼]        │
│   configuration, log       │  Secondary:   [T1.2] [S1.3]   │
│   messages..."             │                                │
│                            │  Confidence: 92%               │
├────────────────────────────┴────────────────────────────────┤
│  [코멘트]: LLM 분류 정확함, Layer 6도 추가 필요             │
├─────────────────────────────────────────────────────────────┤
│         [승인 (LLM 결과 OK)]    [수정 후 저장]              │
└─────────────────────────────────────────────────────────────┘
```

**검수 결과 처리:**
- **승인**: LLM 결과를 그대로 `human_annotation`에 저장 → **A급 학습 데이터**
- **수정**: 사람이 고친 결과를 저장 → **가장 귀한 '오답 노트' 데이터**

---

## 9. 데이터 스키마 (v1.3 개정)

### 9.1 스키마 설계 원칙

#### FK 타입 정합성
> GR_DB의 기존 테이블과 FK 연결 시 타입 일치 필요

- `layer_id`: 문자열 (예: "L7", "L6") - `layers.layer_id`와 동일 타입
- `zone_id`: 문자열 (예: "Z2", "Z0-A") - `security_zones.zone_id`와 동일 타입
- `tag_id`: 문자열 (예: "A1.5") - `function_tags.tag_id`와 동일 타입

#### JSONB vs 정규화 확장 옵션
> 초기에는 JSONB로 빠르게 구현, 필요 시 정규화

```yaml
현재 (JSONB):
  - layer_ids JSONB → ["L7", "L6"]
  - 장점: 스키마 변경 없이 유연한 확장
  - 단점: FK 제약 불가, 정합성은 애플리케이션에서 검증

미래 (정규화 옵션):
  - classification_unit_layers (unit_id, layer_id FK)
  - classification_unit_zones (unit_id, zone_id FK)
  - 장점: DB 레벨 정합성 보장
  - 전환 시점: 데이터 1만 건 이상, 정합성 이슈 발생 시
```

### 9.2 intake_log 테이블 (v1.3 신규)

```sql
-- Intake Router 로그
CREATE TABLE intake_log (
    intake_id SERIAL PRIMARY KEY,

    -- 입력 정보 (크롤러가 붙인 메타데이터)
    source_type VARCHAR(50) NOT NULL,       -- 'NVD_API', 'EXPLOIT_DB', 'SECURITY_BLOG'
    source_format VARCHAR(20),              -- 'JSON', 'HTML', 'PDF', 'TEXT'
    source_url VARCHAR(1000),
    raw_size_bytes INT,
    crawl_config VARCHAR(100),              -- 크롤러 설정 이름

    -- 라우팅 결과
    assigned_track VARCHAR(10) NOT NULL,    -- 'A', 'B', 'C'
    routing_reason VARCHAR(200),            -- "NVD JSON → 정형 데이터 → Track A"

    -- 처리 결과
    units_created INT DEFAULT 0,            -- 생성된 classification_unit 수
    processing_status VARCHAR(20),          -- 'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'
    error_message TEXT,

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

### 9.3 classification_unit 테이블 (v1.3 확장)

```sql
CREATE TABLE classification_unit (
    unit_id SERIAL PRIMARY KEY,

    -- Intake 참조 (v1.3 추가)
    intake_id INT REFERENCES intake_log(intake_id),

    -- 소스 정보
    source_type VARCHAR(50) NOT NULL,       -- 'CVE', 'PRODUCT', 'INFRA_COMPONENT'
    source_id VARCHAR(100),
    source_table VARCHAR(100),

    -- Layer 0 결과 (Format Parser)
    source_format VARCHAR(20),              -- 'PDF', 'HTML', 'JSON', 'MARKDOWN'
    format_parser_metadata JSONB,           -- 페이지 번호, 섹션 경로 등

    -- Layer 1 결과 (AI Structurer) - v1.3 신규
    unit_type VARCHAR(50),                  -- 'VULNERABILITY', 'INFRA_COMPONENT', 'SECURITY_CONTROL'
    extracted_title VARCHAR(500),           -- AI가 추출한 제목
    source_section VARCHAR(200),            -- 원본 문서 내 위치 힌트
    noise_removed JSONB,                    -- 제거된 노이즈 목록

    -- AI Structurer 메타데이터 (v1.3 신규)
    structurer_model VARCHAR(50),           -- 'gpt-4o-mini', 'claude-3-haiku'
    structurer_prompt_version VARCHAR(20),
    chunking_confidence DECIMAL(3,2),       -- 분할 신뢰도

    -- 원본 텍스트
    raw_text TEXT NOT NULL,

    -- 메타데이터
    metadata JSONB,

    -- 상태
    processing_status VARCHAR(20) DEFAULT 'PENDING',
    assigned_track VARCHAR(10),             -- 'A', 'B', 'C' (v1.3 추가)

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9.4 llm_classification_result 테이블

```sql
CREATE TABLE llm_classification_result (
    result_id SERIAL PRIMARY KEY,

    -- 분류 단위 참조
    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),

    -- LLM 정보
    model_name VARCHAR(50) NOT NULL,
    prompt_version VARCHAR(20),
    prompt_text TEXT,

    -- Few-shot 정보
    few_shot_sample_ids JSONB,
    few_shot_count INT DEFAULT 0,

    -- 분류 결과 (GR 좌표)
    layer_ids JSONB,
    zone_ids JSONB,
    primary_tag_id VARCHAR(20),
    secondary_tag_ids JSONB,

    -- 품질 지표
    confidence DECIMAL(3,2),
    has_unknown BOOLEAN DEFAULT FALSE,
    reasoning_summary TEXT,

    -- 원본 응답
    raw_response_json JSONB,

    -- 검증 결과
    validation_status VARCHAR(20),
    validation_errors JSONB,

    -- 비용 추적
    tokens_used INT,
    api_cost DECIMAL(10,4),

    -- 보존 정책
    is_archived BOOLEAN DEFAULT FALSE,
    archived_at TIMESTAMP,
    archive_location VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9.5 human_annotation 및 training_sample 테이블

```sql
-- 사람 검수 결과 테이블 (확정된 "정답")
CREATE TABLE human_annotation (
    annotation_id SERIAL PRIMARY KEY,

    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),
    source_result_id INT REFERENCES llm_classification_result(result_id),

    -- 검수자 정보
    annotator_id VARCHAR(100),
    annotator_role VARCHAR(50),

    -- 확정된 분류 결과 (정답)
    layer_ids JSONB NOT NULL,
    zone_ids JSONB NOT NULL,
    primary_tag_id VARCHAR(20) NOT NULL,
    secondary_tag_ids JSONB,

    -- 검수 메타데이터
    annotation_type VARCHAR(20),            -- 'APPROVED', 'MODIFIED'
    is_ambiguous BOOLEAN DEFAULT FALSE,
    modification_summary TEXT,
    comment TEXT,

    -- 학습 데이터 품질
    is_verified BOOLEAN DEFAULT FALSE,
    quality_score DECIMAL(3,2),

    -- Pinecone 연동
    pinecone_vector_id VARCHAR(100),
    is_golden_sample BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP
);

-- Fine-tuning용 학습 데이터셋
CREATE TABLE training_sample (
    sample_id SERIAL PRIMARY KEY,

    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),
    annotation_id INT REFERENCES human_annotation(annotation_id),

    -- 학습 데이터 (Input → Output 쌍)
    input_text TEXT NOT NULL,
    target_output JSONB NOT NULL,

    -- 분류
    sample_source VARCHAR(20),              -- 'AUTO_APPROVED', 'HUMAN_VERIFIED', 'HUMAN_MODIFIED'
    domain_type VARCHAR(50),

    -- 버전 관리
    dataset_version VARCHAR(20),

    -- 품질
    quality_tier VARCHAR(10),               -- 'A', 'B', 'C'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9.6 테이블 관계도

```
┌────────────────────┐
│    intake_log      │ ←── 크롤러 메타데이터 + 라우팅 결과 (v1.3)
│                    │
│ - source_type      │
│ - source_format    │
│ - assigned_track   │
│ - units_created    │
└─────────┬──────────┘
          │
          │ 1:N
          ▼
┌────────────────────────┐
│ classification_unit    │ ←── Layer 0 + Layer 1 결과
│                        │
│ - unit_type            │ (AI Structurer, v1.3)
│ - extracted_title      │
│ - raw_text             │
│ - assigned_track       │
└─────────┬──────────────┘
          │
          │ 1:N
          ▼
┌────────────────────────┐
│ llm_classification_    │ ←── Layer 2 결과
│ result                 │
│                        │
│ - layer_ids/zone_ids   │
│ - confidence           │
│ - has_unknown          │
│ - raw_response_json    │ → 90일 후 S3 아카이브
└─────────┬──────────────┘
          │
          │ 1:1 (또는 1:0)
          ▼
┌────────────────────────┐
│ human_annotation       │ ←── 사람 검수 결과 (정답) ★★★
│                        │
│ - is_golden_sample     │
│ - pinecone_vector_id   │
└─────────┬──────────────┘
          │
          │ 1:1
          ▼
┌────────────────────────┐
│ training_sample        │ ←── Fine-tuning용 데이터셋
│                        │
│ - input_text           │
│ - target_output        │
│ - quality_tier         │
└────────────────────────┘
```

### 9.7 데이터 보존 정책

> **문제**: `raw_response_json`, `prompt_text` 등 대용량 필드가 누적되면 DB 비대화
> **해결**: 일정 기간 후 S3로 아카이브

| 테이블 | 필드 | 보존 기간 | 아카이브 위치 |
|--------|------|----------|--------------|
| `llm_classification_result` | `raw_response_json` | 90일 | S3 Cold Storage |
| `llm_classification_result` | `prompt_text` | 90일 | S3 Cold Storage |
| `classification_unit` | `raw_text` | 무기한 | PostgreSQL (학습에 필수) |
| `human_annotation` | 전체 | 무기한 | PostgreSQL (정답 데이터) |
| `training_sample` | 전체 | 무기한 | PostgreSQL (Fine-tuning용) |

---

## 10. 수집 전략: 어떤 데이터를 우선 수집하는가?

### 10.1 기본 원칙

데이터는 무조건 많다고 좋은 게 아닙니다. **"어떤 샘플을 사람이 보느냐"가 효율을 좌우**합니다.

### 10.2 우선순위 전략

#### 전략 1: UNKNOWN 포함 결과 우선

```
UNKNOWN_LAYER 또는 UNKNOWN_TAG 포함 → 최우선 리뷰
→ LLM이 "모르겠다"고 한 것 = 가장 어려운 케이스 = 최고 가치 학습 데이터
```

#### 전략 2: Confidence 낮은 것부터 검수

```
LLM confidence < 0.7  →  사람이 가장 먼저 검수
LLM confidence 0.7~0.9 →  다음 우선순위
LLM confidence ≥ 0.9   →  자동 승인 (나중에 샘플링 검증)
```

**이유**: LLM이 자신 없어하는 것 = 모델이 가장 배워야 할 것

#### 전략 3: 도메인/태그 다양성 최대화

```
각 Domain(D/N/S/A/…) 별로 골고루 수집
→ 특정 Tag만 많은 데이터셋은 편향됨
```

**균형 목표:**
- Layer별 최소 100건씩
- Zone별 최소 50건씩
- Domain별 최소 200건씩

#### 전략 4: Edge Case 집중 수집

이미 존재하는 Edge Case 문서 활용:
- `3D_INFRASTRUCTURE_CLASSIFICATION_V2.2_EDGE_CASE`
- `IT_Infrastructure_Function_Tag_Classification_Guide`

**이 문서들의 예시를 전부 classification_unit으로 만들어서:**
1. LLM 분류 실행
2. 사람이 정답 확정
3. → **모델이 가장 헷갈리는 부분을 특정해서 가르치는 효과**

#### 전략 5: 자동 승인 vs 리뷰 분리

```yaml
자동 승인 조건 (사람 안 봐도 됨):
  - LLM confidence ≥ 0.9
  - 규칙 기반 검증 통과 (불가능 조합 없음)
  - UNKNOWN 없음
  - → 바로 training_sample에 'AUTO_APPROVED'로 저장

리뷰 필요 조건 (사람이 봐야 함):
  - confidence 낮음 (<0.9)
  - 규칙 위반 감지
  - UNKNOWN 포함
  - → 리뷰 큐에 추가
```

### 10.3 수집 우선순위 매트릭스

| 우선순위 | 데이터 유형 | 이유 |
|---------|------------|------|
| **1순위** | UNKNOWN 포함 결과 | LLM도 모르는 것 → 가장 귀한 학습 데이터 |
| **2순위** | Edge Case 문서 예시 | 가장 어려운 케이스 → 학습 효과 최대 |
| **3순위** | Confidence 낮은 결과 | 모델의 약점 보완 |
| **4순위** | 새로운 제품/취약점 | 최신 데이터 확보 |
| **5순위** | 도메인 균형 맞추기 | 편향 방지 |
| **6순위** | 자동 승인 샘플링 | 품질 검증 |

---

## 11. 보안, PII, 멀티테넌트 고려사항

### 11.1 보안 원칙

| 영역 | 정책 | 구현 방법 |
|------|------|----------|
| **PII 최소화** | 개인 식별 정보 수집 최소화 | `annotator_id`는 익명 ID 사용, 이메일 저장 금지 |
| **데이터 분리** | 학습 데이터에 민감 정보 포함 금지 | CVE 공개 정보만 사용, 내부 취약점 스캔 결과는 별도 관리 |
| **접근 제어** | 역할 기반 접근 제어 (RBAC) | 리뷰어 권한, 관리자 권한 분리 |
| **감사 로깅** | 모든 검수 활동 기록 | `human_annotation.annotator_id`, 타임스탬프 |

### 11.2 멀티테넌트 확장 고려

> 현재는 단일 테넌트로 시작하되, 향후 확장 가능한 구조 유지

```sql
-- 향후 멀티테넌트 확장 시 추가될 컬럼
-- ALTER TABLE classification_unit ADD COLUMN tenant_id VARCHAR(50);
-- ALTER TABLE llm_classification_result ADD COLUMN tenant_id VARCHAR(50);

-- Row-Level Security (RLS) 적용 예시
-- CREATE POLICY tenant_isolation ON classification_unit
--   USING (tenant_id = current_setting('app.current_tenant'));
```

### 11.3 LLM API 보안

| 항목 | 정책 |
|------|------|
| **API 키 관리** | 환경 변수 또는 Secrets Manager 사용, 코드에 하드코딩 금지 |
| **데이터 전송** | TLS 1.3 사용, 외부 LLM에 민감 정보 전송 금지 |
| **비용 제한** | 일일/월간 API 호출 한도 설정, 이상 사용 알림 |

---

## 12. 구현 전략: 어떻게 만드는가?

### 12.1 기술 스택

| 구성 요소 | 기술 | 이유 |
|----------|------|------|
| **언어** | Python 3.11+ | 데이터 처리, LLM API, DB 연동 생태계 최강 |
| **LLM API** | OpenAI, Anthropic | GPT-4, Claude 활용 |
| **임베딩** | OpenAI/Voyage | Pinecone 연동용 벡터 생성 |
| **DB 연동** | psycopg2, neo4j-driver, pinecone-client | 3개 DB 모두 지원 |
| **데이터 처리** | pandas, pydantic | 대량 데이터 + 스키마 검증 |
| **웹 프레임워크** | FastAPI | 리뷰 UI 백엔드, API 제공 |
| **스케줄링** | APScheduler, Celery | 배치 처리, 아카이브 |
| **환경** | Ubuntu 22.04 LTS | 안정성, Docker 호환 |

### 12.2 프로젝트 구조 (v1.3 개정)

```
classification_engine/
├── pyproject.toml
├── README.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                       # 핵심 모듈
│   │   ├── models.py               # Pydantic 데이터 모델
│   │   ├── config.py               # 설정 관리
│   │   ├── tracks.py               # Track A/B/C 정의 (v1.3)
│   │   └── exceptions.py
│   │
│   ├── router/                     # Layer -1: Intake Router (v1.3 신규)
│   │   ├── __init__.py
│   │   ├── intake_router.py        # 라우팅 메인 로직
│   │   ├── rules.py                # 라우팅 규칙 정의
│   │   └── metadata_extractor.py   # 크롤러 메타데이터 처리
│   │
│   ├── ingestors/                  # Layer 0: Format Parser
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── json_ingestor.py
│   │   ├── html_ingestor.py
│   │   ├── pdf_ingestor.py
│   │   ├── csv_ingestor.py
│   │   └── markdown_ingestor.py
│   │
│   ├── structurer/                 # Layer 1: AI Structurer (v1.3 신규)
│   │   ├── __init__.py
│   │   ├── semantic_chunker.py     # LLM 기반 의미 분할
│   │   ├── noise_filter.py         # 광고/서론/인삿말 제거
│   │   ├── unit_extractor.py       # classification_unit 생성
│   │   └── prompts/
│   │       ├── chunking_prompt.py
│   │       └── unit_types.py
│   │
│   ├── classifier/                 # Layer 2: AI Classifier
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── openai_classifier.py
│   │   ├── anthropic_classifier.py
│   │   ├── fewshot/
│   │   │   ├── embedder.py
│   │   │   ├── retriever.py
│   │   │   └── prompt_builder.py
│   │   └── prompts/
│   │       ├── classification_prompt.py
│   │       └── unknown_handler.py
│   │
│   ├── validators/                 # 검증
│   │   ├── rule_validator.py
│   │   ├── unknown_detector.py
│   │   ├── consistency_validator.py
│   │   └── confidence_scorer.py
│   │
│   ├── review/                     # Human Review
│   │   ├── __init__.py
│   │   ├── review_queue.py
│   │   └── annotation_service.py
│   │
│   ├── training/                   # 학습 데이터 관리
│   │   ├── __init__.py
│   │   ├── golden_sample_manager.py
│   │   ├── data_exporter.py
│   │   ├── dataset_manager.py
│   │   └── quality_scorer.py
│   │
│   ├── archive/                    # 보존 정책
│   │   ├── __init__.py
│   │   ├── s3_archiver.py
│   │   └── retention_policy.py
│   │
│   ├── db/                         # 데이터베이스 연동
│   │   ├── postgres.py
│   │   ├── neo4j.py
│   │   └── pinecone.py
│   │
│   ├── pipeline/                   # 파이프라인 오케스트레이션
│   │   ├── __init__.py
│   │   ├── orchestrator.py         # 전체 파이프라인 관리 (v1.3)
│   │   ├── track_executor.py       # Track별 실행 (v1.3)
│   │   └── batch_processor.py
│   │
│   └── api/                        # REST API
│       ├── routes.py
│       ├── intake_api.py           # Intake Router API (v1.3)
│       ├── review_api.py
│       └── metrics_api.py
│
├── data/
│   ├── prompts/
│   └── exports/
│
└── tests/
    ├── test_router/
    ├── test_ingestors/
    ├── test_structurer/
    └── test_classifier/
```

### 12.3 개발 단계 (Phase)

#### Phase 1: 기반 구축 + 4계층 파이프라인

**목표**: Intake Router + Format Parser + AI Classifier 기본 동작

- [ ] Intake Router 구현 (규칙 기반 라우팅)
- [ ] Format Parser 구현 (JSON, HTML, PDF)
- [ ] Track A 경로 완성 (정형 데이터)
- [ ] AI Classifier 기본 구현
- [ ] UNKNOWN 태그 처리 로직
- [ ] 학습 데이터 스키마 생성

**산출물**:
- Track A 경로로 NVD JSON 처리 가능
- 첫 100건 분류 결과 저장

#### Phase 2: AI Structurer + Track B 완성

**목표**: 비정형 문서 처리 파이프라인 완성

- [ ] AI Structurer 구현 (gpt-4o-mini)
- [ ] Semantic Chunking 프롬프트 최적화
- [ ] Track B 경로 완성
- [ ] Dynamic Few-shot 구현 (Pinecone 연동)
- [ ] 리뷰 큐 시스템 구현

**산출물**:
- HTML, PDF 문서에서 의미 단위 추출
- Layer 정확도 ≥95% 달성
- Golden Sample 100건 이상 축적

#### Phase 3: 품질 관리 + 운영 안정화

**목표**: Fine-tuning 준비 + 보존 정책

- [ ] training_sample 생성 파이프라인
- [ ] JSONL 내보내기 기능
- [ ] 데이터셋 버전 관리
- [ ] S3 아카이브 시스템 구현
- [ ] KPI 대시보드

**산출물**:
- Fine-tuning용 데이터셋 v1.0 (1,000건 이상)
- 90일 이상 오래된 데이터 자동 아카이브

#### Phase 4: 자체 모델 전환 (장기)

**목표**: 외부 LLM 의존도 감소

- [ ] Chunking 전용 Fine-tuned 모델 (Layer 1)
- [ ] Classification 전용 Fine-tuned 모델 (Layer 2)
- [ ] 하이브리드 라우팅

**산출물**:
- 비용 80% 절감
- 자체 모델 정확도 외부 LLM의 90% 이상

---

## 13. API 명세 (v1.3 개정)

### 13.1 Intake API (v1.3 신규)

**POST /engine-b/intake**

```json
// Request (크롤러가 호출)
{
  "source_type": "EXPLOIT_DB",
  "source_format": "HTML",
  "source_url": "https://exploit-db.com/exploits/12345",
  "raw_content": "<html>...</html>",
  "crawl_config": "exploit_db_daily",
  "metadata": {
    "crawled_at": "2025-12-01T10:00:00Z",
    "page_size": 15000
  }
}

// Response
{
  "intake_id": 12345,
  "assigned_track": "B",
  "routing_reason": "EXPLOIT_DB + HTML → 비정형 문서 → Track B",
  "processing_status": "QUEUED",
  "estimated_units": 3
}
```

### 13.2 분류 API

**POST /engine-b/classify**

```json
// Request
{
  "source_type": "CVE",
  "raw_text": "Apache Log4j2 2.0-beta9 through 2.14.1...",
  "metadata": {
    "source": "NVD",
    "cve_id": "CVE-2021-44228"
  },
  "options": {
    "use_few_shot": true,
    "few_shot_count": 3
  }
}

// Response
{
  "unit_id": 12345,
  "result_id": 67890,
  "classification": {
    "layer_ids": ["L7", "L6"],
    "zone_ids": ["Z2", "Z0-A"],
    "primary_tag": "A1.5",
    "secondary_tags": ["T1.2", "S1.3"]
  },
  "confidence": 0.92,
  "has_unknown": false,
  "few_shot_used": 3,
  "assigned_track": "A",
  "validation_status": "PASSED",
  "next_action": "AUTO_APPROVED"
}
```

### 13.3 파이프라인 상태 API (v1.3 신규)

**GET /engine-b/intake/{intake_id}/status**

```json
// Response
{
  "intake_id": 12345,
  "assigned_track": "B",
  "status": "COMPLETED",
  "layers_completed": ["L0", "L1", "L2"],
  "units_created": 3,
  "units_classified": 3,
  "units_auto_approved": 2,
  "units_in_review": 1,
  "processing_time_ms": 4500,
  "cost_usd": 0.10
}
```

### 13.4 리뷰 API

**GET /engine-b/review/queue**

```json
// Response
{
  "total_pending": 45,
  "unknown_count": 8,
  "items": [
    {
      "unit_id": 12346,
      "raw_text": "...",
      "llm_result": {...},
      "confidence": 0.75,
      "has_unknown": true,
      "priority": "HIGH"
    }
  ]
}
```

### 13.5 메트릭 API

**GET /engine-b/metrics**

```json
// Response
{
  "period": "2025-12",
  "accuracy": {
    "layer": 0.96,
    "zone": 0.93,
    "primary_tag": 0.91
  },
  "unknown_ratio": 0.08,
  "auto_approval_rate": 0.52,
  "cost": {
    "total_usd": 450.00,
    "per_raw": 0.045,
    "per_unit": 0.03
  },
  "volume": {
    "total_raw": 10000,
    "total_units": 15000,
    "training_samples": 850,
    "golden_samples": 120
  },
  "track_distribution": {
    "A": 4000,
    "B": 5500,
    "C": 500
  }
}
```

---

## 14. 학습 데이터 내보내기 포맷

### 14.1 Fine-tuning용 JSONL 포맷

```jsonl
{"messages": [
    {"role": "system", "content": "너는 GR Framework 분류 전문가야. 취약점/제품 설명을 읽고 Layer, Zone, Tag를 분류해줘. 확신이 없으면 UNKNOWN으로 표시해."},
    {"role": "user", "content": "다음 취약점을 분류해줘:\n\nApache Log4j2 2.0-beta9 through 2.14.1..."},
    {"role": "assistant", "content": "{\"layer_ids\": [\"L7\", \"L6\"], \"zone_ids\": [\"Z2\"], \"primary_tag\": \"A1.5\", \"secondary_tags\": [\"T1.2\", \"S1.3\"]}"}
]}
{"messages": [...]}
{"messages": [...]}
```

### 14.2 데이터셋 버전 관리

| 버전 | 날짜 | 샘플 수 | 설명 |
|------|------|---------|------|
| v1.0 | 2025-12 | 1,000 | 초기 수집 |
| v1.1 | 2026-01 | 2,500 | Edge Case 보강, UNKNOWN 처리 개선 |
| v2.0 | 2026-03 | 5,000 | Zone 규칙 변경 반영 |

---

## 15. 결론

### 15.1 v1.3의 핵심 변화

| 항목 | v1.0 | v1.1 | v1.2 | v1.3 |
|------|------|------|------|------|
| **파이프라인** | 규칙 기반 | 2단계 LLM | 2단계 LLM | **4계층 (Router→Parser→Structurer→Classifier)** |
| **라우팅** | - | - | - | **Intake Router (Track A/B/C)** |
| **파싱** | 규칙 기반 | 규칙 기반 | 규칙 기반 | **Layer 0 (도구) + Layer 1 (AI)** |
| **분류 방식** | 규칙 기반 | LLM | LLM + Few-shot | LLM + Few-shot + **AI Structurer** |
| **비용 최적화** | - | - | - | **Track A는 L1 스킵, 저비용 모델 분리** |
| **비용 단위** | - | - | - | **Raw vs Unit 구분 명확화** |

### 15.2 4계층 파이프라인 요약

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Layer -1    │     │ Layer 0     │     │ Layer 1     │     │ Layer 2     │
│ Router      │ →  │ Parser      │ →  │ Structurer  │ →  │ Classifier  │
│             │     │             │     │             │     │             │
│ 경로 결정    │     │ 텍스트 추출  │     │ 의미 분할    │     │ 좌표 할당   │
│ (규칙)      │     │ (도구)      │     │ (AI 저비용)  │     │ (AI 고성능) │
│ $0          │     │ $0          │     │ ~$0.01/raw  │     │ ~$0.03/unit │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 15.3 성공 기준

- [ ] **4계층 파이프라인 동작**: Track A/B/C 모두 정상 처리
- [ ] **정확도 KPI**: Layer ≥95%, Zone ≥92%, Tag ≥90%
- [ ] **UNKNOWN 비율**: < 15%
- [ ] **비용 효율**: Track A는 Layer 1 스킵으로 비용 절감
- [ ] **학습 데이터 축적**: 월 1,000건 이상
- [ ] **자체 모델**: 외부 LLM 정확도의 90% 이상

---

## 부록: 용어 정의

| 용어 | 정의 |
|------|------|
| **Raw Data** | 크롤러가 가져온 원본 1건 (HTML 1페이지, PDF 1파일, JSON 1응답) |
| **Unit** | AI Structurer가 분할한 의미 단위 1개 (`classification_unit` 테이블의 1행) |
| **Intake Router** | 데이터 메타데이터를 보고 처리 경로(Track)를 결정하는 라우터 (Layer -1) |
| **Format Parser** | PDF/HTML/JSON 등 형식에서 텍스트를 추출하는 도구 (Layer 0) |
| **AI Structurer** | 텍스트를 의미 단위로 분할하고 노이즈를 제거하는 AI (Layer 1) |
| **AI Classifier** | 각 단위에 GR 3D 좌표를 할당하는 AI (Layer 2) |
| **Track A** | 정형 데이터 경로: L0 → L2 (L1 스킵), 1 raw = 1 unit |
| **Track B** | 비정형 문서 경로: L0 → L1 → L2, 1 raw = N units |
| **Track C** | 짧은 텍스트 경로: 바로 L2 (L0, L1 스킵) |
| **Semantic Chunking** | 물리적 구조가 아닌 의미 단위로 텍스트를 분할하는 기법 |
| **Data Flywheel** | 데이터가 쌓일수록 AI가 좋아지고, AI가 좋아질수록 데이터가 더 잘 쌓이는 선순환 구조 |
| **Golden Sample** | 사람이 검증 완료하여 Few-shot 예시로 사용 가능한 고품질 샘플 |
| **Dynamic Few-shot** | 분류 시 Pinecone에서 유사한 Golden Sample을 검색하여 프롬프트에 예시로 주입하는 전략 |
| **UNKNOWN 태그** | LLM이 확신이 없을 때 Hallucination 대신 사용하는 태그 |

---

**[문서 끝]**
