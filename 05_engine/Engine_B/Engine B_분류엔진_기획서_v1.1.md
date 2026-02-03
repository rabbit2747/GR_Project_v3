# GR 분류 엔진 (Classification Engine) 기획서

> **"혼돈을 질서로, 원석을 보석으로, 그리고 경험을 자산으로"**
>
> 외부의 비정형 데이터를 GR Framework의 3D 좌표계로 정확히 배치하고,
> 그 과정에서 축적된 데이터로 자체 AI를 성장시키는 엔진

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 분류 엔진 (Classification Engine) 기획서 |
| **버전** | v1.1 |
| **작성일** | 2025-11-28 |
| **수정일** | 2025-12-01 |
| **목적** | 분류 엔진의 존재 이유, 분류 대상, 분류 방법론, **Data Flywheel 전략** 정립 |
| **대상 독자** | 기획자, 아키텍트, 개발팀 |
| **연관 문서** | Engine A 종합 계획서_v1.0.md, 00_분류체계_개요.md, 01_schema.sql |
| **구현 환경** | Ubuntu + Python |

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2025-11-28 | 최초 작성 (규칙 기반 분류 설계) |
| v1.1 | 2025-12-01 | **LLM 기반 분류 + Data Flywheel 전략 추가**, 학습 데이터 축적 스키마 설계 |

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

### 1.3 분류 엔진의 정의

**분류 엔진(Classification Engine)** 은 이러한 문제를 해결하기 위해:

1. **다양한 소스**의 비정형 데이터를 수신하고
2. **LLM의 추론 능력**으로 GR 표준 모델(Canonical Model)로 변환하며
3. **3D 좌표(Layer × Zone × Tag)** 를 할당하고
4. **중복/충돌을 처리**하여 DB에 적재하며
5. **(v1.1 신규) 이 과정을 학습 데이터로 축적**하여 자체 AI 성장의 기반을 마련합니다

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

## 3. 핵심 전략: Data Flywheel (v1.1 신규)

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

Fine-tuned 모델 학습을 위해 **`[질문(Input)] → [정답(Output)]`** 쌍이 필요합니다.

**반드시 저장해야 할 3가지:**

| 데이터 | 설명 | 예시 |
|--------|------|------|
| **Raw Input** | 원본 텍스트 | 크롤링한 CVE 설명, 제품 문서 |
| **LLM Input** | 실제 프롬프트 | "이 취약점의 Layer/Zone/Tag는?" |
| **Final Verified Output** | **확정된 정답** | 사람이 검수했거나 자동 승인된 결과 |

> **핵심**: LLM이 뱉은 답변을 그대로 저장하는 게 아니라, **"이게 맞다"고 판명된 최종 결과**를 저장해야 합니다.

---

## 4. 분류 방법론: 어떻게 분류하는가? (v1.1 개정)

### 4.1 분류 엔진 아키텍처 (LLM 기반)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   분류 엔진 (Classification Engine) v1.1                 │
│                        "LLM + Data Flywheel"                            │
└─────────────────────────────────────────────────────────────────────────┘

[Input Layer]
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ LLM 지식    │ │ NVD API     │ │ 수동 입력   │ │ 웹 크롤링   │
│ (Claude)    │ │ (CVE Feed)  │ │ (Manual)    │ │ (Scraper)   │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       └───────────────┴───────────────┴───────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       [Processing Layer]                                 │
│                                                                         │
│  ┌────────────────┐                                                     │
│  │ 1. Parser      │  입력 데이터를 분류 단위(Unit)로 분할               │
│  │ (단위 분할)    │  → classification_unit 테이블에 저장                │
│  └───────┬────────┘                                                     │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────┐                                                     │
│  │ 2. LLM         │  GPT-4, Claude 등에 분류 요청                       │
│  │ Classifier     │  → llm_classification_result 테이블에 저장          │
│  │ (추론 분류)    │  ※ 프롬프트 + 결과 전체 로깅                        │
│  └───────┬────────┘                                                     │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────┐                                                     │
│  │ 3. Auto        │  규칙 기반 검증 + Confidence Score                  │
│  │ Validator      │  → 자동 승인 / 리뷰 큐 / 거부 분기                  │
│  │ (자동 검증)    │                                                     │
│  └───────┬────────┘                                                     │
│          │                                                              │
│   ┌──────┴──────┬───────────────┐                                       │
│   ▼             ▼               ▼                                       │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                                 │
│ │ 자동승인  │ │ 리뷰 큐   │ │ 거부     │                                 │
│ │ (≥90%)   │ │ (70-89%) │ │ (<70%)   │                                 │
│ └────┬─────┘ └────┬─────┘ └────┬─────┘                                 │
│      │            │            │                                        │
│      │            ▼            │                                        │
│      │     ┌──────────────┐    │                                        │
│      │     │ 4. Human     │    │                                        │
│      │     │ Review       │    │                                        │
│      │     │ (사람 검수)   │    │                                        │
│      │     └──────┬───────┘    │                                        │
│      │            │            │                                        │
│      └────────────┴────────────┘                                        │
│                   │                                                     │
│                   ▼                                                     │
│         ┌─────────────────┐                                             │
│         │ 5. Final Output │  human_annotation 테이블에 저장             │
│         │ (정답 확정)     │  ← 이것이 학습 데이터가 됨                   │
│         └────────┬────────┘                                             │
│                  │                                                      │
└──────────────────┼──────────────────────────────────────────────────────┘
                   │
                   ▼
[Output Layer]
┌─────────────────────────────────────────────────────────────────────────┐
│                         GR Database Cluster                              │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │
│  │ PostgreSQL  │  │   Neo4j     │  │  Pinecone   │  │ Training Data │  │
│  │ (Master)    │  │  (Graph)    │  │  (Vector)   │  │ (학습 데이터)  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 분류 프로세스 상세

#### Stage 1: Parser (단위 분할)

입력 데이터를 **LLM이 한 번에 판단하기 좋은 단위(Unit)** 로 분할합니다.

| 입력 소스 | 분할 단위 | 예시 |
|----------|----------|------|
| CVE JSON | 개별 CVE 1건 | CVE-2021-44228 |
| 제품 문서 | 섹션/단락 단위 | "PostgreSQL 개요" 섹션 |
| 인프라 설명 | 구성요소 1개 | "Nginx Reverse Proxy 설정" |
| 웹 크롤링 | 페이지/블록 단위 | Exploit-DB 취약점 1건 |

#### Stage 2: LLM Classifier (추론 분류)

LLM에게 GR Framework 좌표 분류를 요청합니다.

**프롬프트 예시:**
```
당신은 GR Framework 분류 전문가입니다.

다음 취약점 설명을 읽고 GR 3D 좌표를 분류해주세요:
- Layer: L0~L7, Cross-Layer 중 선택
- Zone: Zone 0-A, 0-B, 1~5 중 선택
- Primary Tag: 주요 기능 태그 1개
- Secondary Tags: 보조 태그들

[취약점 설명]
{raw_text}

JSON 형식으로 응답해주세요.
```

**LLM 응답 예시:**
```json
{
  "layer_ids": ["L7", "L6"],
  "zone_ids": ["Z2", "Z0-A"],
  "primary_tag": "A1.5",
  "secondary_tags": ["T1.2", "S1.3"],
  "confidence": 0.92,
  "reasoning": "Log4j는 Java 애플리케이션 라이브러리로 Layer 7에 위치하며..."
}
```

#### Stage 3: Auto Validator (자동 검증)

LLM 결과를 규칙 기반으로 검증합니다.

**검증 항목:**
1. **Layer-Zone 조합 유효성**: 불가능한 조합이 아닌가?
2. **Tag 존재 여부**: DB에 있는 Tag인가?
3. **Confidence 점수**: LLM이 자신 있는가?
4. **규칙 위반 여부**: GR Framework 규칙 준수 여부

**분기 처리:**

| Confidence Score | 규칙 검증 | 처리 방법 |
|------------------|----------|----------|
| ≥ 90% | 통과 | **자동 승인** → 바로 학습 데이터 |
| 70% ~ 89% | 통과 | **리뷰 큐** → 사람 검수 대기 |
| < 70% | - | **거부** → 재분류 또는 폐기 |
| - | 실패 | **리뷰 큐** → 사람 검수 필요 |

#### Stage 4: Human Review (사람 검수)

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

#### Stage 5: Final Output (정답 확정)

최종 확정된 결과가 `human_annotation` 테이블에 저장되며, 이것이 나중에 Fine-tuning 학습 데이터가 됩니다.

---

## 5. 데이터 스키마: 무엇을 저장하는가? (v1.1 개정)

### 5.1 학습 데이터 축적 스키마 (신규)

기존 비즈니스 로직과 별개로, **"미래의 AI 학습"** 을 위한 3개의 핵심 테이블을 추가합니다.

```sql
-- ============================================
-- 학습 데이터 축적 스키마 (Training Data Schema)
-- ============================================

-- 1. 분류 단위 테이블 (LLM에 던질 "문제")
CREATE TABLE classification_unit (
    unit_id SERIAL PRIMARY KEY,

    -- 소스 정보
    source_type VARCHAR(50) NOT NULL,       -- 'CVE', 'PRODUCT', 'INFRA_COMPONENT', 'TECH_STACK'
    source_id VARCHAR(100),                 -- 원본 시스템의 ID (cve_id, product_id 등)
    source_table VARCHAR(100),              -- 원본 테이블명

    -- 원본 텍스트 (LLM에 실제로 넣는 "문제 본문")
    raw_text TEXT NOT NULL,

    -- 메타데이터
    metadata JSONB,                         -- 파일 경로, 문서 제목, 섹션 이름 등

    -- 상태 관리
    processing_status VARCHAR(20) DEFAULT 'PENDING',  -- PENDING, PROCESSING, COMPLETED, FAILED

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. LLM 분류 결과 테이블 (LLM의 "답안")
CREATE TABLE llm_classification_result (
    result_id SERIAL PRIMARY KEY,

    -- 분류 단위 참조
    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),

    -- LLM 정보
    model_name VARCHAR(50) NOT NULL,        -- 'gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini'
    prompt_version VARCHAR(20),             -- 프롬프트 버전 관리 (예: 'v1.0', 'v1.1')
    prompt_text TEXT,                       -- 실제 사용한 프롬프트 전체

    -- 분류 결과 (GR 좌표)
    layer_ids JSONB,                        -- ["L7", "L6"]
    zone_ids JSONB,                         -- ["Z2", "Z0-A"]
    primary_tag_id VARCHAR(20),             -- 'A1.5'
    secondary_tag_ids JSONB,                -- ["T1.2", "S1.3"]

    -- 품질 지표
    confidence DECIMAL(3,2),                -- 0.00 ~ 1.00 (LLM이 출력한 신뢰도)
    reasoning_summary TEXT,                 -- LLM이 짧게 쓴 분류 이유

    -- 원본 응답
    raw_response_json JSONB,                -- LLM이 실제로 반환한 전체 JSON

    -- 검증 결과
    validation_status VARCHAR(20),          -- PASSED, FAILED, NEEDS_REVIEW
    validation_errors JSONB,                -- 검증 실패 시 오류 목록

    -- 비용 추적
    tokens_used INT,                        -- 토큰 사용량 (비용 계산용)
    api_cost DECIMAL(10,4),                 -- API 호출 비용 (USD)

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 사람 검수 결과 테이블 (확정된 "정답" - 가장 중요!)
CREATE TABLE human_annotation (
    annotation_id SERIAL PRIMARY KEY,

    -- 분류 단위 참조
    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),

    -- 기반이 된 LLM 결과 (어떤 LLM 결과를 검토했는지)
    source_result_id INT REFERENCES llm_classification_result(result_id),

    -- 검수자 정보
    annotator_id VARCHAR(100),              -- 검수자 ID/이름
    annotator_role VARCHAR(50),             -- 'SECURITY_EXPERT', 'INFRA_ENGINEER' 등

    -- 확정된 분류 결과 (정답)
    layer_ids JSONB NOT NULL,               -- ["L7", "L6"]
    zone_ids JSONB NOT NULL,                -- ["Z2", "Z0-A"]
    primary_tag_id VARCHAR(20) NOT NULL,    -- 'A1.5'
    secondary_tag_ids JSONB,                -- ["T1.2", "S1.3"]

    -- 검수 메타데이터
    annotation_type VARCHAR(20),            -- 'APPROVED' (LLM 그대로), 'MODIFIED' (수정함)
    is_ambiguous BOOLEAN DEFAULT FALSE,     -- 애매해서 "정답 없음/여러 후보" 케이스
    modification_summary TEXT,              -- 수정한 경우: 무엇을 왜 바꿨는지
    comment TEXT,                           -- 추가 코멘트, 엣지 케이스 설명

    -- 학습 데이터 품질
    is_verified BOOLEAN DEFAULT FALSE,      -- 최종 검증 완료 여부
    quality_score DECIMAL(3,2),             -- 학습 데이터로서의 품질 점수

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP
);

-- 4. 학습 데이터셋 테이블 (Fine-tuning용 최종 가공 데이터)
CREATE TABLE training_sample (
    sample_id SERIAL PRIMARY KEY,

    -- 참조
    unit_id INT NOT NULL REFERENCES classification_unit(unit_id),
    annotation_id INT REFERENCES human_annotation(annotation_id),

    -- 학습 데이터 (Input → Output 쌍)
    input_text TEXT NOT NULL,               -- classification_unit.raw_text
    target_output JSONB NOT NULL,           -- 정답 레이블 JSON

    -- 분류
    sample_source VARCHAR(20),              -- 'AUTO_APPROVED', 'HUMAN_VERIFIED', 'HUMAN_MODIFIED'
    domain_type VARCHAR(50),                -- 'VULNERABILITY', 'PRODUCT', 'INFRA'

    -- 버전 관리
    dataset_version VARCHAR(20),            -- 'v1.0', 'v1.1' (데이터셋 버전)

    -- 품질
    quality_tier VARCHAR(10),               -- 'A', 'B', 'C' (학습 데이터 등급)

    -- 타임스탬프
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 인덱스
-- ============================================
CREATE INDEX idx_unit_source_type ON classification_unit(source_type);
CREATE INDEX idx_unit_status ON classification_unit(processing_status);
CREATE INDEX idx_llm_result_unit ON llm_classification_result(unit_id);
CREATE INDEX idx_llm_result_model ON llm_classification_result(model_name);
CREATE INDEX idx_llm_result_validation ON llm_classification_result(validation_status);
CREATE INDEX idx_annotation_unit ON human_annotation(unit_id);
CREATE INDEX idx_annotation_type ON human_annotation(annotation_type);
CREATE INDEX idx_training_version ON training_sample(dataset_version);
CREATE INDEX idx_training_quality ON training_sample(quality_tier);
```

### 5.2 테이블 관계도 (학습 데이터 흐름)

```
┌────────────────────┐
│ classification_unit│ ←── 입력 데이터 (문제)
│                    │
│ - raw_text         │
│ - source_type      │
│ - metadata         │
└─────────┬──────────┘
          │
          │ 1:N
          ▼
┌────────────────────────┐
│ llm_classification_    │ ←── LLM 분류 결과 (답안)
│ result                 │
│                        │
│ - model_name           │
│ - prompt_text          │
│ - layer_ids/zone_ids   │
│ - confidence           │
│ - raw_response_json    │
└─────────┬──────────────┘
          │
          │ 1:1 (또는 1:0)
          ▼
┌────────────────────────┐
│ human_annotation       │ ←── 사람 검수 결과 (정답) ★★★
│                        │
│ - annotator_id         │
│ - annotation_type      │
│ - layer_ids/zone_ids   │
│ - modification_summary │
└─────────┬──────────────┘
          │
          │ 1:1
          ▼
┌────────────────────────┐
│ training_sample        │ ←── Fine-tuning용 데이터셋
│                        │
│ - input_text           │
│ - target_output        │
│ - dataset_version      │
│ - quality_tier         │
└────────────────────────┘
```

### 5.3 기존 취약점 스키마 (v1.0에서 유지)

기존 `vulnerabilities`, `vulnerability_layers`, `vulnerability_zones` 등의 테이블은 v1.0과 동일하게 유지됩니다.

학습 데이터 테이블과 비즈니스 테이블의 관계:

```
┌───────────────────────────────────────────────────────────────────────┐
│                         데이터 흐름                                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [학습 데이터 영역]              [비즈니스 데이터 영역]                 │
│                                                                       │
│  classification_unit ─────────→ vulnerabilities                       │
│         │                              │                              │
│         ▼                              ▼                              │
│  llm_classification_result      vulnerability_layers                  │
│         │                       vulnerability_zones                   │
│         ▼                       vulnerability_tags                    │
│  human_annotation                      │                              │
│         │                              │                              │
│         ▼                              ▼                              │
│  training_sample               Production DB                          │
│         │                       (서비스에 활용)                        │
│         ▼                                                             │
│  Fine-tuned Model                                                     │
│  (자체 AI)                                                            │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 6. 수집 전략: 어떤 데이터를 우선 수집하는가? (v1.1 신규)

### 6.1 기본 원칙

데이터는 무조건 많다고 좋은 게 아닙니다. **"어떤 샘플을 사람이 보느냐"가 효율을 좌우**합니다.

### 6.2 우선순위 전략

#### 전략 1: Confidence 낮은 것부터 검수

```
LLM confidence < 0.7  →  사람이 가장 먼저 검수
LLM confidence 0.7~0.9 →  다음 우선순위
LLM confidence ≥ 0.9   →  자동 승인 (나중에 샘플링 검증)
```

**이유**: LLM이 자신 없어하는 것 = 모델이 가장 배워야 할 것

#### 전략 2: 도메인/태그 다양성 최대화

```
각 Domain(D/N/S/A/…) 별로 골고루 수집
→ 특정 Tag만 많은 데이터셋은 편향됨
```

**균형 목표:**
- Layer별 최소 100건씩
- Zone별 최소 50건씩
- Domain별 최소 200건씩

#### 전략 3: Edge Case 집중 수집

이미 존재하는 Edge Case 문서 활용:
- `3D_INFRASTRUCTURE_CLASSIFICATION_V2.2_EDGE_CASE`
- `IT_Infrastructure_Function_Tag_Classification_Guide`

**이 문서들의 예시를 전부 classification_unit으로 만들어서:**
1. LLM 분류 실행
2. 사람이 정답 확정
3. → **모델이 가장 헷갈리는 부분을 특정해서 가르치는 효과**

#### 전략 4: 자동 승인 vs 리뷰 분리

```yaml
자동 승인 조건 (사람 안 봐도 됨):
  - LLM confidence ≥ 0.9
  - 규칙 기반 검증 통과 (불가능 조합 없음)
  - → 바로 training_sample에 'AUTO_APPROVED'로 저장

리뷰 필요 조건 (사람이 봐야 함):
  - confidence 낮음 (<0.9)
  - 규칙 위반 감지
  - → 리뷰 큐에 추가
```

### 6.3 수집 우선순위 매트릭스

| 우선순위 | 데이터 유형 | 이유 |
|---------|------------|------|
| **1순위** | Edge Case 문서 예시 | 가장 어려운 케이스 → 학습 효과 최대 |
| **2순위** | Confidence 낮은 결과 | 모델의 약점 보완 |
| **3순위** | 새로운 제품/취약점 | 최신 데이터 확보 |
| **4순위** | 도메인 균형 맞추기 | 편향 방지 |
| **5순위** | 자동 승인 샘플링 | 품질 검증 |

---

## 7. 구현 전략: 어떻게 만드는가?

### 7.1 기술 스택

| 구성 요소 | 기술 | 이유 |
|----------|------|------|
| **언어** | Python 3.11+ | 데이터 처리, LLM API, DB 연동 생태계 최강 |
| **LLM API** | OpenAI, Anthropic | GPT-4, Claude 활용 |
| **DB 연동** | psycopg2, neo4j-driver, pinecone-client | 3개 DB 모두 지원 |
| **데이터 처리** | pandas, pydantic | 대량 데이터 + 스키마 검증 |
| **웹 프레임워크** | FastAPI | 리뷰 UI 백엔드, API 제공 |
| **스케줄링** | APScheduler, Celery | 배치 처리 |
| **환경** | Ubuntu 22.04 LTS | 안정성, Docker 호환 |

### 7.2 프로젝트 구조 (v1.1 업데이트)

```
classification_engine/
├── pyproject.toml
├── README.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                   # 핵심 모듈
│   │   ├── models.py           # Pydantic 데이터 모델
│   │   ├── config.py           # 설정 관리
│   │   └── exceptions.py
│   │
│   ├── parsers/                # Stage 1: 단위 분할
│   │   ├── base.py
│   │   ├── cve_parser.py
│   │   ├── product_parser.py
│   │   └── document_parser.py
│   │
│   ├── llm/                    # Stage 2: LLM 분류 (v1.1 신규)
│   │   ├── __init__.py
│   │   ├── base.py             # LLM 인터페이스
│   │   ├── openai_classifier.py
│   │   ├── anthropic_classifier.py
│   │   ├── prompts/            # 프롬프트 템플릿
│   │   │   ├── vulnerability_prompt.py
│   │   │   └── product_prompt.py
│   │   └── response_parser.py  # LLM 응답 파싱
│   │
│   ├── validators/             # Stage 3: 자동 검증
│   │   ├── rule_validator.py   # 규칙 기반 검증
│   │   ├── consistency_validator.py
│   │   └── confidence_scorer.py
│   │
│   ├── review/                 # Stage 4: 사람 검수 (v1.1 신규)
│   │   ├── __init__.py
│   │   ├── review_queue.py     # 리뷰 큐 관리
│   │   └── annotation_service.py
│   │
│   ├── training/               # 학습 데이터 관리 (v1.1 신규)
│   │   ├── __init__.py
│   │   ├── data_exporter.py    # JSONL 내보내기
│   │   ├── dataset_manager.py  # 버전 관리
│   │   └── quality_scorer.py   # 품질 평가
│   │
│   ├── db/                     # 데이터베이스 연동
│   │   ├── postgres.py
│   │   ├── neo4j.py
│   │   └── pinecone.py
│   │
│   ├── pipeline/               # 파이프라인
│   │   ├── classification_pipeline.py
│   │   └── batch_processor.py
│   │
│   └── api/                    # REST API
│       ├── routes.py
│       └── review_api.py       # 리뷰 UI API (v1.1 신규)
│
├── data/
│   ├── prompts/                # 프롬프트 버전 관리
│   └── exports/                # 학습 데이터 내보내기
│
└── tests/
```

### 7.3 개발 단계 (Phase) - v1.1 업데이트

#### Phase 1: 기반 구축 + 학습 데이터 인프라

**목표**: LLM 분류 + 결과 로깅 파이프라인

- [ ] 학습 데이터 스키마 생성 (classification_unit, llm_classification_result, human_annotation)
- [ ] LLM Classifier 구현 (OpenAI/Anthropic)
- [ ] 프롬프트 템플릿 작성
- [ ] 결과 전체 로깅 구현

**산출물**:
- LLM 분류 실행 시 자동으로 학습 데이터 축적
- 첫 100건 분류 결과 저장

#### Phase 2: 리뷰 시스템 + 정답 수집

**목표**: Human-in-the-loop 완성

- [ ] 리뷰 큐 시스템 구현
- [ ] 간단한 리뷰 UI (또는 스프레드시트 연동)
- [ ] 자동 승인 로직 구현
- [ ] human_annotation 저장 파이프라인

**산출물**:
- 사람이 검수한 정답 데이터 500건 이상
- 자동/수동 분류 비율 측정

#### Phase 3: 학습 데이터 가공 + 품질 관리

**목표**: Fine-tuning 준비

- [ ] training_sample 생성 파이프라인
- [ ] JSONL 내보내기 기능
- [ ] 데이터셋 버전 관리
- [ ] 품질 점수 산정

**산출물**:
- Fine-tuning용 데이터셋 v1.0 (1,000건 이상)
- 품질 리포트

#### Phase 4: 자체 모델 전환 (장기)

**목표**: 외부 LLM 의존도 감소

- [ ] Fine-tuned 모델 학습 (Llama, Mistral 등)
- [ ] 자체 모델 vs 외부 LLM 정확도 비교
- [ ] 하이브리드 라우팅 (자체 모델 + 외부 LLM)

**산출물**:
- GR 전용 분류 모델
- 비용 80% 절감

---

## 8. API 명세 (v1.1 신규)

### 8.1 분류 API

**POST /engine-b/classify**

```json
// Request
{
  "source_type": "CVE",
  "raw_text": "Apache Log4j2 2.0-beta9 through 2.14.1...",
  "metadata": {
    "source": "NVD",
    "cve_id": "CVE-2021-44228"
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
  "validation_status": "PASSED",
  "next_action": "AUTO_APPROVED"
}
```

### 8.2 리뷰 API

**GET /engine-b/review/queue**

```json
// Response
{
  "total_pending": 45,
  "items": [
    {
      "unit_id": 12346,
      "raw_text": "...",
      "llm_result": {...},
      "confidence": 0.75,
      "priority": "HIGH"
    }
  ]
}
```

**POST /engine-b/review/submit**

```json
// Request
{
  "unit_id": 12346,
  "result_id": 67891,
  "annotation_type": "MODIFIED",
  "layer_ids": ["L7"],
  "zone_ids": ["Z2"],
  "primary_tag": "A1.5",
  "secondary_tags": ["T1.2"],
  "comment": "Zone 0-A는 제외, 내부 시스템에서만 사용"
}

// Response
{
  "annotation_id": 11111,
  "status": "SAVED",
  "training_sample_created": true
}
```

---

## 9. 학습 데이터 내보내기 포맷 (v1.1 신규)

### 9.1 Fine-tuning용 JSONL 포맷

```jsonl
{"messages": [
    {"role": "system", "content": "너는 GR Framework 분류 전문가야. 취약점/제품 설명을 읽고 Layer, Zone, Tag를 분류해줘."},
    {"role": "user", "content": "다음 취약점을 분류해줘:\n\nApache Log4j2 2.0-beta9 through 2.14.1..."},
    {"role": "assistant", "content": "{\"layer_ids\": [\"L7\", \"L6\"], \"zone_ids\": [\"Z2\"], \"primary_tag\": \"A1.5\", \"secondary_tags\": [\"T1.2\", \"S1.3\"]}"}
]}
{"messages": [...]}
{"messages": [...]}
```

### 9.2 데이터셋 버전 관리

| 버전 | 날짜 | 샘플 수 | 설명 |
|------|------|---------|------|
| v1.0 | 2025-12 | 1,000 | 초기 수집 |
| v1.1 | 2026-01 | 2,500 | Edge Case 보강 |
| v2.0 | 2026-03 | 5,000 | Zone 규칙 변경 반영 |

---

## 10. 결론

### 10.1 v1.1의 핵심 변화

| 항목 | v1.0 | v1.1 |
|------|------|------|
| **분류 방식** | 규칙 기반 | LLM 기반 |
| **학습 데이터** | 없음 | 전체 과정 로깅 |
| **장기 목표** | 정확한 분류 | 정확한 분류 + **자체 AI 확보** |
| **테이블 추가** | - | classification_unit, llm_classification_result, human_annotation, training_sample |

### 10.2 Data Flywheel 실현 로드맵

```
[현재]                    [중기]                    [장기]
LLM 100%                  규칙 70% + LLM 30%        자체 모델 90% + LLM 10%
고비용                    비용 절감                  비용 최소화
외부 의존                  하이브리드                 독자적 역량

     ──────────────────────────────────────────────────────→
                    학습 데이터 축적 (1K → 5K → 10K+)
```

### 10.3 성공 기준

- [ ] 1,000+ 분류 결과가 학습 데이터로 축적
- [ ] Human Review 처리율 80% 이상
- [ ] Fine-tuning 데이터셋 v1.0 생성
- [ ] 자체 모델 정확도 외부 LLM의 90% 이상 달성

---

## 부록: 용어 정의

| 용어 | 정의 |
|------|------|
| **Data Flywheel** | 데이터가 쌓일수록 AI가 좋아지고, AI가 좋아질수록 데이터가 더 잘 쌓이는 선순환 구조 |
| **classification_unit** | LLM에 던질 분류 문제 하나의 단위 |
| **human_annotation** | 사람이 검수/확정한 정답 레이블 |
| **training_sample** | Fine-tuning에 사용할 최종 가공된 학습 데이터 |
| **Confidence Score** | LLM이 자신의 분류 결과에 대해 출력한 신뢰도 (0~1) |
| **Auto-Approved** | Confidence가 높고 규칙 검증을 통과하여 자동 승인된 데이터 |

---

**[문서 끝]**
