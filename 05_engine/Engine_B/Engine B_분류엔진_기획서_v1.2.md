# GR 분류 엔진 (Classification Engine) 기획서

> **"혼돈을 질서로, 원석을 보석으로, 그리고 경험을 자산으로"**
>
> 외부의 비정형 데이터를 GR Framework의 3D 좌표계로 정확히 배치하고,
> 그 과정에서 축적된 데이터로 자체 AI를 성장시키는 엔진

---

## Executive Summary (v1.2 추가)

### 핵심 목표
분류 엔진은 **외부 비정형 데이터 → GR 3D 좌표계 매핑**을 수행하는 핵심 엔진으로, **LLM 기반 추론 + Data Flywheel 전략**을 통해 장기적으로 자체 AI를 확보합니다.

### 주요 지표 (KPI)
| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| **Layer 정확도** | ≥ 95% | 사람 검수 결과 대비 |
| **Zone 정확도** | ≥ 92% | 사람 검수 결과 대비 |
| **Primary Tag 정확도** | ≥ 90% | 사람 검수 결과 대비 |
| **UNKNOWN 비율** | < 15% | 전체 분류 중 |
| **자동 승인률** | ≥ 50% | Confidence ≥90% |
| **학습 데이터 축적** | 1,000건/월 | training_sample 테이블 |

### 비용 로드맵
```
Phase 1 (0-6개월): LLM 100% → 월 $500-1,000
Phase 2 (6-12개월): 규칙 70% + LLM 30% → 월 $200-400
Phase 3 (12개월+): 자체 모델 90% + LLM 10% → 월 $50-100
```

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 분류 엔진 (Classification Engine) 기획서 |
| **버전** | v1.2 |
| **작성일** | 2025-11-28 |
| **수정일** | 2025-12-01 |
| **목적** | 분류 엔진의 존재 이유, 분류 대상, 분류 방법론, Data Flywheel 전략, **동적 Few-shot, UNKNOWN 처리, 보안/품질 기준** 정립 |
| **대상 독자** | 기획자, 아키텍트, 개발팀 |
| **연관 문서** | Engine A 종합 계획서_v1.0.md, 00_분류체계_개요.md, 01_schema.sql |
| **구현 환경** | Ubuntu + Python |

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2025-11-28 | 최초 작성 (규칙 기반 분류 설계) |
| v1.1 | 2025-12-01 | LLM 기반 분류 + Data Flywheel 전략 추가 |
| v1.2 | 2025-12-01 | **Dynamic Few-shot, UNKNOWN 태그, 보안/PII/멀티테넌트 고려, 정확도 KPI, 보존 정책 추가** |

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

> **중요 구분 (v1.2 추가): 본업(분류) vs 학습 데이터**
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

## 4. 분류 방법론: 어떻게 분류하는가? (v1.2 개정)

### 4.1 분류 엔진 아키텍처 (LLM + Dynamic Few-shot)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   분류 엔진 (Classification Engine) v1.2                 │
│                  "LLM + Dynamic Few-shot + UNKNOWN 처리"                 │
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
│  ┌────────────────┐  ┌─────────────────────────────────────┐           │
│  │ 2. Dynamic     │  │ Pinecone에서 유사한 Golden Sample   │           │
│  │ Few-shot       │→│ 검색하여 프롬프트에 예시로 삽입     │ (v1.2)    │
│  │ (예시 주입)    │  └─────────────────────────────────────┘           │
│  └───────┬────────┘                                                     │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────┐                                                     │
│  │ 3. LLM         │  GPT-4, Claude 등에 분류 요청                       │
│  │ Classifier     │  → llm_classification_result 테이블에 저장          │
│  │ (추론 분류)    │  ※ UNKNOWN 태그 허용으로 Hallucination 방지         │
│  └───────┬────────┘                                                     │
│          │                                                              │
│          ▼                                                              │
│  ┌────────────────┐                                                     │
│  │ 4. Auto        │  규칙 기반 검증 + Confidence Score                  │
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
│      │     │ 5. Human     │    │                                        │
│      │     │ Review       │    │                                        │
│      │     │ (사람 검수)   │    │                                        │
│      │     └──────┬───────┘    │                                        │
│      │            │            │                                        │
│      └────────────┴────────────┘                                        │
│                   │                                                     │
│                   ▼                                                     │
│         ┌─────────────────┐                                             │
│         │ 6. Final Output │  human_annotation 테이블에 저장             │
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

### 4.2 Dynamic Few-shot 전략 (v1.2 신규)

> **핵심 아이디어**: 분류할 때마다 Pinecone에서 유사한 "Golden Sample"을 검색하여 프롬프트에 예시로 삽입

#### 4.2.1 Golden Sample이란?

- **정의**: 사람이 검수하여 **정확하다고 확인된** 분류 결과
- **출처**: `human_annotation` 테이블에서 `is_verified = TRUE`인 샘플
- **저장**: Pinecone에 `input_text`를 임베딩하여 저장

#### 4.2.2 Dynamic Few-shot 워크플로우

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

#### 4.2.3 Few-shot 프롬프트 템플릿

```
당신은 GR Framework 분류 전문가입니다.

## 분류 기준
- Layer: L0~L7, Cross-Layer 중 선택
- Zone: Zone 0-A, 0-B, 1~5 중 선택
- Primary Tag: 주요 기능 태그 1개
- Secondary Tags: 보조 태그들

## 참고 예시 (유사한 과거 분류)
{few_shot_examples}

## 분류할 텍스트
{raw_text}

## 중요 지침
- 확신이 없는 차원은 "UNKNOWN"으로 표시하세요
- 추측하지 말고, 근거가 있는 분류만 하세요

JSON 형식으로 응답해주세요.
```

### 4.3 UNKNOWN 태그 처리 (v1.2 신규)

> **문제**: LLM이 무조건 답을 만들려고 Hallucination 발생
> **해결**: "모르겠으면 UNKNOWN이라고 해도 된다"고 명시적으로 허용

#### 4.3.1 UNKNOWN 사용 규칙

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

#### 4.3.2 UNKNOWN 비율 모니터링

| UNKNOWN 비율 | 상태 | 조치 |
|-------------|------|------|
| < 5% | **정상** | 유지 |
| 5% ~ 15% | **주의** | 프롬프트/예시 검토 |
| > 15% | **경고** | 근본 원인 분석 필요 (데이터 품질? 분류 체계?) |

---

### 4.4 분류 프로세스 상세

#### Stage 1: Parser (단위 분할)

입력 데이터를 **LLM이 한 번에 판단하기 좋은 단위(Unit)** 로 분할합니다.

| 입력 소스 | 분할 단위 | 예시 |
|----------|----------|------|
| CVE JSON | 개별 CVE 1건 | CVE-2021-44228 |
| 제품 문서 | 섹션/단락 단위 | "PostgreSQL 개요" 섹션 |
| 인프라 설명 | 구성요소 1개 | "Nginx Reverse Proxy 설정" |
| 웹 크롤링 | 페이지/블록 단위 | Exploit-DB 취약점 1건 |

#### Stage 2: Dynamic Few-shot (예시 주입) - v1.2

1. **임베딩 생성**: 입력 텍스트를 OpenAI/Voyage 임베딩으로 변환
2. **유사도 검색**: Pinecone에서 Top 3~5 유사 샘플 검색
3. **예시 삽입**: 검색된 Golden Sample을 프롬프트에 삽입
4. **프롬프트 구성**: 시스템 프롬프트 + 예시 + 입력 + UNKNOWN 허용 지침

#### Stage 3: LLM Classifier (추론 분류)

LLM에게 GR Framework 좌표 분류를 요청합니다.

**LLM 응답 예시 (UNKNOWN 포함):**
```json
{
  "layer_ids": ["L7", "UNKNOWN_LAYER"],
  "zone_ids": ["Z2"],
  "primary_tag": "A1.5",
  "secondary_tags": ["T1.2"],
  "confidence": 0.75,
  "reasoning": "애플리케이션 계층임은 확실하나, Runtime 영향 여부는 추가 정보 필요"
}
```

#### Stage 4: Auto Validator (자동 검증)

LLM 결과를 규칙 기반으로 검증합니다.

**검증 항목:**
1. **Layer-Zone 조합 유효성**: 불가능한 조합이 아닌가?
2. **Tag 존재 여부**: DB에 있는 Tag인가?
3. **Confidence 점수**: LLM이 자신 있는가?
4. **규칙 위반 여부**: GR Framework 규칙 준수 여부
5. **(v1.2) UNKNOWN 포함 여부**: UNKNOWN이 있으면 무조건 리뷰 큐

**분기 처리:**

| Confidence Score | 규칙 검증 | UNKNOWN | 처리 방법 |
|------------------|----------|---------|----------|
| ≥ 90% | 통과 | 없음 | **자동 승인** → 바로 학습 데이터 |
| 70% ~ 89% | 통과 | 없음 | **리뷰 큐** → 사람 검수 대기 |
| < 70% | - | - | **거부** → 재분류 또는 폐기 |
| - | - | 있음 | **리뷰 큐** → 사람이 직접 분류 |
| - | 실패 | - | **리뷰 큐** → 사람 검수 필요 |

#### Stage 5: Human Review (사람 검수)

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

#### Stage 6: Final Output (정답 확정)

최종 확정된 결과가 `human_annotation` 테이블에 저장되며, 이것이 나중에 Fine-tuning 학습 데이터가 됩니다.

---

## 5. 데이터 스키마: 무엇을 저장하는가? (v1.2 개정)

### 5.1 스키마 설계 원칙 (v1.2 추가)

#### FK 타입 정합성
> GR_DB의 기존 테이블과 FK 연결 시 타입 일치 필요

- `layer_id`: 문자열 (예: "L7", "L6") - `layers.layer_id`와 동일 타입
- `zone_id`: 문자열 (예: "Z2", "Z0-A") - `security_zones.zone_id`와 동일 타입
- `tag_id`: 문자열 (예: "A1.5") - `atom_tags.tag_id`와 동일 타입

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

### 5.2 학습 데이터 축적 스키마

```sql
-- ============================================
-- 학습 데이터 축적 스키마 (Training Data Schema)
-- v1.2: FK 타입 맞춤, 보존 정책 컬럼 추가
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

    -- Few-shot 정보 (v1.2 추가)
    few_shot_sample_ids JSONB,              -- 사용된 Golden Sample IDs
    few_shot_count INT DEFAULT 0,           -- 사용된 예시 개수

    -- 분류 결과 (GR 좌표) - 문자열 타입으로 GR_DB FK와 정합
    layer_ids JSONB,                        -- ["L7", "L6"] 또는 ["UNKNOWN_LAYER"]
    zone_ids JSONB,                         -- ["Z2", "Z0-A"]
    primary_tag_id VARCHAR(20),             -- 'A1.5' 또는 'UNKNOWN_TAG'
    secondary_tag_ids JSONB,                -- ["T1.2", "S1.3"]

    -- 품질 지표
    confidence DECIMAL(3,2),                -- 0.00 ~ 1.00 (LLM이 출력한 신뢰도)
    has_unknown BOOLEAN DEFAULT FALSE,      -- UNKNOWN 태그 포함 여부 (v1.2)
    reasoning_summary TEXT,                 -- LLM이 짧게 쓴 분류 이유

    -- 원본 응답 (대용량 필드)
    raw_response_json JSONB,                -- LLM이 실제로 반환한 전체 JSON

    -- 검증 결과
    validation_status VARCHAR(20),          -- PASSED, FAILED, NEEDS_REVIEW
    validation_errors JSONB,                -- 검증 실패 시 오류 목록

    -- 비용 추적
    tokens_used INT,                        -- 토큰 사용량 (비용 계산용)
    api_cost DECIMAL(10,4),                 -- API 호출 비용 (USD)

    -- 보존 정책 (v1.2 추가)
    is_archived BOOLEAN DEFAULT FALSE,      -- S3로 아카이브 여부
    archived_at TIMESTAMP,                  -- 아카이브 시점
    archive_location VARCHAR(500),          -- S3 경로 (예: s3://gr-archive/llm-results/2025/01/)

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
    annotator_id VARCHAR(100),              -- 검수자 ID/이름 (PII 최소화: 이메일 대신 ID 사용)
    annotator_role VARCHAR(50),             -- 'SECURITY_EXPERT', 'INFRA_ENGINEER' 등

    -- 확정된 분류 결과 (정답) - 문자열 타입으로 GR_DB FK와 정합
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
    is_verified BOOLEAN DEFAULT FALSE,      -- 최종 검증 완료 여부 (Golden Sample 후보)
    quality_score DECIMAL(3,2),             -- 학습 데이터로서의 품질 점수

    -- Pinecone 연동 (v1.2 추가)
    pinecone_vector_id VARCHAR(100),        -- Pinecone에 저장된 벡터 ID
    is_golden_sample BOOLEAN DEFAULT FALSE, -- Golden Sample로 선정 여부

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
CREATE INDEX idx_llm_result_has_unknown ON llm_classification_result(has_unknown);
CREATE INDEX idx_llm_result_archived ON llm_classification_result(is_archived);
CREATE INDEX idx_annotation_unit ON human_annotation(unit_id);
CREATE INDEX idx_annotation_type ON human_annotation(annotation_type);
CREATE INDEX idx_annotation_golden ON human_annotation(is_golden_sample);
CREATE INDEX idx_training_version ON training_sample(dataset_version);
CREATE INDEX idx_training_quality ON training_sample(quality_tier);
```

### 5.3 데이터 보존 정책 (v1.2 추가)

> **문제**: `raw_response_json`, `prompt_text` 등 대용량 필드가 누적되면 DB 비대화
> **해결**: 일정 기간 후 S3로 아카이브

#### 5.3.1 보존 정책 매트릭스

| 테이블 | 필드 | 보존 기간 | 아카이브 위치 |
|--------|------|----------|--------------|
| `llm_classification_result` | `raw_response_json` | 90일 | S3 Cold Storage |
| `llm_classification_result` | `prompt_text` | 90일 | S3 Cold Storage |
| `classification_unit` | `raw_text` | 무기한 | PostgreSQL (학습에 필수) |
| `human_annotation` | 전체 | 무기한 | PostgreSQL (정답 데이터) |
| `training_sample` | 전체 | 무기한 | PostgreSQL (Fine-tuning용) |

#### 5.3.2 아카이브 프로세스

```python
# 예시: 90일 지난 raw_response_json 아카이브
def archive_old_responses():
    cutoff_date = datetime.now() - timedelta(days=90)

    # 1. S3에 백업
    old_results = db.query("""
        SELECT result_id, raw_response_json, prompt_text
        FROM llm_classification_result
        WHERE created_at < %s AND is_archived = FALSE
    """, [cutoff_date])

    for result in old_results:
        s3_path = f"s3://gr-archive/llm-results/{result.created_at.year}/{result.created_at.month}/"
        s3.upload(result.to_json(), s3_path + f"{result.result_id}.json")

    # 2. DB에서 대용량 필드 제거
    db.execute("""
        UPDATE llm_classification_result
        SET raw_response_json = NULL,
            prompt_text = NULL,
            is_archived = TRUE,
            archived_at = NOW(),
            archive_location = %s
        WHERE created_at < %s AND is_archived = FALSE
    """, [s3_path, cutoff_date])
```

### 5.4 테이블 관계도 (학습 데이터 흐름)

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
│ - few_shot_sample_ids  │ (v1.2: Dynamic Few-shot 정보)
│ - layer_ids/zone_ids   │
│ - has_unknown          │ (v1.2: UNKNOWN 여부)
│ - confidence           │
│ - raw_response_json    │ → 90일 후 S3 아카이브
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
│ - is_golden_sample     │ (v1.2: Pinecone 연동)
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
│ - dataset_version      │
│ - quality_tier         │
└────────────────────────┘
```

---

## 6. 수집 전략: 어떤 데이터를 우선 수집하는가? (v1.1 신규)

### 6.1 기본 원칙

데이터는 무조건 많다고 좋은 게 아닙니다. **"어떤 샘플을 사람이 보느냐"가 효율을 좌우**합니다.

### 6.2 우선순위 전략

#### 전략 1: UNKNOWN 포함 결과 우선 (v1.2 추가)

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
- `IT_Infrastructure_Function_Classification_Guide`

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

### 6.3 수집 우선순위 매트릭스

| 우선순위 | 데이터 유형 | 이유 |
|---------|------------|------|
| **1순위** | UNKNOWN 포함 결과 | LLM도 모르는 것 → 가장 귀한 학습 데이터 (v1.2) |
| **2순위** | Edge Case 문서 예시 | 가장 어려운 케이스 → 학습 효과 최대 |
| **3순위** | Confidence 낮은 결과 | 모델의 약점 보완 |
| **4순위** | 새로운 제품/취약점 | 최신 데이터 확보 |
| **5순위** | 도메인 균형 맞추기 | 편향 방지 |
| **6순위** | 자동 승인 샘플링 | 품질 검증 |

---

## 7. 보안, PII, 멀티테넌트 고려사항 (v1.2 신규)

### 7.1 보안 원칙

| 영역 | 정책 | 구현 방법 |
|------|------|----------|
| **PII 최소화** | 개인 식별 정보 수집 최소화 | `annotator_id`는 익명 ID 사용, 이메일 저장 금지 |
| **데이터 분리** | 학습 데이터에 민감 정보 포함 금지 | CVE 공개 정보만 사용, 내부 취약점 스캔 결과는 별도 관리 |
| **접근 제어** | 역할 기반 접근 제어 (RBAC) | 리뷰어 권한, 관리자 권한 분리 |
| **감사 로깅** | 모든 검수 활동 기록 | `human_annotation.annotator_id`, 타임스탬프 |

### 7.2 멀티테넌트 확장 고려

> 현재는 단일 테넌트로 시작하되, 향후 확장 가능한 구조 유지

```sql
-- 향후 멀티테넌트 확장 시 추가될 컬럼
-- ALTER TABLE classification_unit ADD COLUMN tenant_id VARCHAR(50);
-- ALTER TABLE llm_classification_result ADD COLUMN tenant_id VARCHAR(50);

-- Row-Level Security (RLS) 적용 예시
-- CREATE POLICY tenant_isolation ON classification_unit
--   USING (tenant_id = current_setting('app.current_tenant'));
```

### 7.3 LLM API 보안

| 항목 | 정책 |
|------|------|
| **API 키 관리** | 환경 변수 또는 Secrets Manager 사용, 코드에 하드코딩 금지 |
| **데이터 전송** | TLS 1.3 사용, 외부 LLM에 민감 정보 전송 금지 |
| **비용 제한** | 일일/월간 API 호출 한도 설정, 이상 사용 알림 |

---

## 8. 구현 전략: 어떻게 만드는가?

### 8.1 기술 스택

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

### 8.2 프로젝트 구조 (v1.2 업데이트)

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
│   ├── fewshot/                # Stage 2: Dynamic Few-shot (v1.2 신규)
│   │   ├── __init__.py
│   │   ├── embedder.py         # 임베딩 생성
│   │   ├── retriever.py        # Pinecone 검색
│   │   └── prompt_builder.py   # 프롬프트 구성
│   │
│   ├── llm/                    # Stage 3: LLM 분류
│   │   ├── __init__.py
│   │   ├── base.py             # LLM 인터페이스
│   │   ├── openai_classifier.py
│   │   ├── anthropic_classifier.py
│   │   ├── prompts/            # 프롬프트 템플릿
│   │   │   ├── vulnerability_prompt.py
│   │   │   ├── product_prompt.py
│   │   │   └── unknown_handler.py   # UNKNOWN 처리 (v1.2)
│   │   └── response_parser.py  # LLM 응답 파싱
│   │
│   ├── validators/             # Stage 4: 자동 검증
│   │   ├── rule_validator.py   # 규칙 기반 검증
│   │   ├── unknown_detector.py # UNKNOWN 감지 (v1.2)
│   │   ├── consistency_validator.py
│   │   └── confidence_scorer.py
│   │
│   ├── review/                 # Stage 5: 사람 검수
│   │   ├── __init__.py
│   │   ├── review_queue.py     # 리뷰 큐 관리
│   │   └── annotation_service.py
│   │
│   ├── training/               # 학습 데이터 관리
│   │   ├── __init__.py
│   │   ├── golden_sample_manager.py  # Golden Sample 관리 (v1.2)
│   │   ├── data_exporter.py    # JSONL 내보내기
│   │   ├── dataset_manager.py  # 버전 관리
│   │   └── quality_scorer.py   # 품질 평가
│   │
│   ├── archive/                # 보존 정책 (v1.2 신규)
│   │   ├── __init__.py
│   │   ├── s3_archiver.py      # S3 아카이브
│   │   └── retention_policy.py # 보존 정책 관리
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
│       ├── review_api.py       # 리뷰 UI API
│       └── metrics_api.py      # KPI 모니터링 API (v1.2)
│
├── data/
│   ├── prompts/                # 프롬프트 버전 관리
│   └── exports/                # 학습 데이터 내보내기
│
└── tests/
```

### 8.3 개발 단계 (Phase) - v1.2 업데이트

#### Phase 1: 기반 구축 + 학습 데이터 인프라

**목표**: LLM 분류 + 결과 로깅 파이프라인 + UNKNOWN 처리

- [ ] 학습 데이터 스키마 생성 (v1.2 컬럼 포함)
- [ ] LLM Classifier 구현 (OpenAI/Anthropic)
- [ ] UNKNOWN 태그 처리 로직 구현
- [ ] 프롬프트 템플릿 작성 (UNKNOWN 허용 지침 포함)
- [ ] 결과 전체 로깅 구현

**산출물**:
- LLM 분류 실행 시 자동으로 학습 데이터 축적
- UNKNOWN 비율 < 15% 달성
- 첫 100건 분류 결과 저장

#### Phase 2: Dynamic Few-shot + 리뷰 시스템

**목표**: Human-in-the-loop + Golden Sample 기반 Few-shot

- [ ] Pinecone 연동 (임베딩 저장/검색)
- [ ] Golden Sample 관리 시스템
- [ ] Dynamic Few-shot 프롬프트 구성
- [ ] 리뷰 큐 시스템 구현
- [ ] 간단한 리뷰 UI (또는 스프레드시트 연동)
- [ ] human_annotation 저장 파이프라인

**산출물**:
- Golden Sample 100건 이상 축적
- Few-shot 적용으로 정확도 5%+ 향상
- 사람이 검수한 정답 데이터 500건 이상

#### Phase 3: 품질 관리 + 보존 정책

**목표**: Fine-tuning 준비 + 운영 안정화

- [ ] training_sample 생성 파이프라인
- [ ] JSONL 내보내기 기능
- [ ] 데이터셋 버전 관리
- [ ] S3 아카이브 시스템 구현
- [ ] KPI 대시보드 (정확도, UNKNOWN 비율, 비용)

**산출물**:
- Fine-tuning용 데이터셋 v1.0 (1,000건 이상)
- Layer 정확도 ≥95%, Zone 정확도 ≥92%, Tag 정확도 ≥90%
- 90일 이상 오래된 데이터 자동 아카이브

#### Phase 4: 자체 모델 전환 (장기)

**목표**: 외부 LLM 의존도 감소

- [ ] Fine-tuned 모델 학습 (Llama, Mistral 등)
- [ ] 자체 모델 vs 외부 LLM 정확도 비교
- [ ] 하이브리드 라우팅 (자체 모델 + 외부 LLM)

**산출물**:
- GR 전용 분류 모델
- 비용 80% 절감

---

## 9. API 명세 (v1.2 업데이트)

### 9.1 분류 API

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
    "use_few_shot": true,      // v1.2: Few-shot 사용 여부
    "few_shot_count": 3        // v1.2: 사용할 예시 개수
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
  "has_unknown": false,          // v1.2: UNKNOWN 포함 여부
  "few_shot_used": 3,            // v1.2: 사용된 예시 개수
  "validation_status": "PASSED",
  "next_action": "AUTO_APPROVED"
}
```

### 9.2 리뷰 API

**GET /engine-b/review/queue**

```json
// Response
{
  "total_pending": 45,
  "unknown_count": 8,           // v1.2: UNKNOWN 포함 건수
  "items": [
    {
      "unit_id": 12346,
      "raw_text": "...",
      "llm_result": {...},
      "confidence": 0.75,
      "has_unknown": true,      // v1.2
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
  "comment": "Zone 0-A는 제외, 내부 시스템에서만 사용",
  "mark_as_golden": true        // v1.2: Golden Sample로 등록
}

// Response
{
  "annotation_id": 11111,
  "status": "SAVED",
  "training_sample_created": true,
  "golden_sample_registered": true,  // v1.2
  "pinecone_vector_id": "gs-11111"   // v1.2
}
```

### 9.3 메트릭 API (v1.2 신규)

**GET /engine-b/metrics**

```json
// Response
{
  "period": "2025-12",
  "accuracy": {
    "layer": 0.96,              // Layer 정확도: 96%
    "zone": 0.93,               // Zone 정확도: 93%
    "primary_tag": 0.91         // Primary Tag 정확도: 91%
  },
  "unknown_ratio": 0.08,        // UNKNOWN 비율: 8%
  "auto_approval_rate": 0.52,   // 자동 승인률: 52%
  "cost": {
    "total_usd": 450.00,
    "per_classification": 0.045
  },
  "volume": {
    "total_classified": 10000,
    "training_samples": 850,
    "golden_samples": 120
  }
}
```

---

## 10. 학습 데이터 내보내기 포맷

### 10.1 Fine-tuning용 JSONL 포맷

```jsonl
{"messages": [
    {"role": "system", "content": "너는 GR Framework 분류 전문가야. 취약점/제품 설명을 읽고 Layer, Zone, Tag를 분류해줘. 확신이 없으면 UNKNOWN으로 표시해."},
    {"role": "user", "content": "다음 취약점을 분류해줘:\n\nApache Log4j2 2.0-beta9 through 2.14.1..."},
    {"role": "assistant", "content": "{\"layer_ids\": [\"L7\", \"L6\"], \"zone_ids\": [\"Z2\"], \"primary_tag\": \"A1.5\", \"secondary_tags\": [\"T1.2\", \"S1.3\"]}"}
]}
{"messages": [...]}
{"messages": [...]}
```

### 10.2 데이터셋 버전 관리

| 버전 | 날짜 | 샘플 수 | 설명 |
|------|------|---------|------|
| v1.0 | 2025-12 | 1,000 | 초기 수집 |
| v1.1 | 2026-01 | 2,500 | Edge Case 보강, UNKNOWN 처리 개선 |
| v2.0 | 2026-03 | 5,000 | Zone 규칙 변경 반영 |

---

## 11. 결론

### 11.1 v1.2의 핵심 변화

| 항목 | v1.0 | v1.1 | v1.2 |
|------|------|------|------|
| **분류 방식** | 규칙 기반 | LLM 기반 | LLM + **Dynamic Few-shot** |
| **Hallucination 방지** | - | - | **UNKNOWN 태그 허용** |
| **학습 데이터** | 없음 | 전체 과정 로깅 | 로깅 + **Golden Sample 관리** |
| **보존 정책** | - | - | **S3 아카이브** |
| **보안 고려** | - | - | **PII 최소화, 테넌트 준비** |
| **정확도 KPI** | - | - | **Layer ≥95%, Zone ≥92%, Tag ≥90%** |

### 11.2 Data Flywheel 실현 로드맵

```
[현재]                    [중기]                    [장기]
LLM 100%                  규칙 70% + LLM 30%        자체 모델 90% + LLM 10%
고비용                    비용 절감                  비용 최소화
외부 의존                  하이브리드                 독자적 역량

     ──────────────────────────────────────────────────────→
                    학습 데이터 축적 (1K → 5K → 10K+)
                    Golden Sample 축적 (100 → 500 → 1K+)
```

### 11.3 성공 기준

- [ ] **정확도 KPI 달성**: Layer ≥95%, Zone ≥92%, Primary Tag ≥90%
- [ ] **UNKNOWN 비율**: < 15%
- [ ] **학습 데이터 축적**: 1,000+ 분류 결과
- [ ] **Golden Sample**: 100+ 검증된 예시
- [ ] **Human Review 처리율**: 80% 이상
- [ ] **Fine-tuning 데이터셋**: v1.0 생성
- [ ] **자체 모델 정확도**: 외부 LLM의 90% 이상 달성

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
| **Golden Sample** | 사람이 검증 완료하여 Few-shot 예시로 사용 가능한 고품질 샘플 (v1.2) |
| **Dynamic Few-shot** | 분류 시 Pinecone에서 유사한 Golden Sample을 검색하여 프롬프트에 예시로 주입하는 전략 (v1.2) |
| **UNKNOWN 태그** | LLM이 확신이 없을 때 Hallucination 대신 사용하는 태그 (v1.2) |

---

**[문서 끝]**
