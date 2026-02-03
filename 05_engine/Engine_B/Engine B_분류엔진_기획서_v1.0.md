# GR 분류 엔진 (Classification Engine) 기획서

> **"혼돈을 질서로, 원석을 보석으로"**
>
> 외부의 비정형 데이터를 GR Framework의 3D 좌표계로 정확히 배치하는 엔진

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 분류 엔진 (Classification Engine) 기획서 |
| **버전** | v1.0 |
| **작성일** | 2025-11-28 |
| **목적** | 분류 엔진의 존재 이유, 분류 대상, 분류 방법론 정립 |
| **대상 독자** | 기획자, 아키텍트, 개발팀 |
| **연관 문서** | Engine A 종합 계획서_v1.0.md, 00_분류체계_개요.md, 01_schema.sql |
| **구현 환경** | Ubuntu + Python |

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

### 1.3 분류 엔진의 정의

**분류 엔진(Classification Engine)** 은 이러한 문제를 해결하기 위해:

1. **다양한 소스**의 비정형 데이터를 수신하고
2. **GR 표준 모델(Canonical Model)** 로 변환하며
3. **3D 좌표(Layer × Zone × Tag)** 를 할당하고
4. **중복/충돌을 처리**하여 DB에 적재합니다

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

분류 엔진은 **제품 별칭(Alias)** 테이블을 활용하여 모든 표기를 **정규 이름(Canonical Name)** 으로 통일합니다.

---

## 3. 분류 방법론: 어떻게 분류하는가?

### 3.1 분류 엔진 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                        분류 엔진 (Classification Engine)             │
└─────────────────────────────────────────────────────────────────────┘

[Input Layer]
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ LLM 지식    │ │ NVD API     │ │ 수동 입력   │ │ 웹 크롤링   │
│ (Claude)    │ │ (CVE Feed)  │ │ (Manual)    │ │ (Scraper)   │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       └───────────────┴───────────────┴───────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    [Processing Layer]                                │
│                                                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │ 1. Parser      │→│ 2. Normalizer  │→│ 3. Classifier  │        │
│  │ (포맷 파싱)    │  │ (정규화)       │  │ (좌표 할당)    │        │
│  └────────────────┘  └────────────────┘  └────────────────┘        │
│          │                   │                   │                  │
│          ▼                   ▼                   ▼                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │ Raw Data       │  │ Canonical      │  │ Classified     │        │
│  │ (원본 데이터)   │  │ Model          │  │ Data           │        │
│  │                │  │ (표준 모델)     │  │ (분류된 데이터) │        │
│  └────────────────┘  └────────────────┘  └────────────────┘        │
│                                                  │                  │
│                              ┌───────────────────┘                  │
│                              ▼                                      │
│                    ┌────────────────┐                               │
│                    │ 4. Validator   │                               │
│                    │ (검증)         │                               │
│                    └────────────────┘                               │
│                              │                                      │
│              ┌───────────────┼───────────────┐                      │
│              ▼               ▼               ▼                      │
│       ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│       │ 자동승인  │    │ 리뷰 큐   │    │ 거부     │                 │
│       │ (≥85%)   │    │ (70-85%) │    │ (<70%)   │                 │
│       └──────────┘    └──────────┘    └──────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
[Output Layer]
┌─────────────────────────────────────────────────────────────────────┐
│                         GR Database Cluster                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │ PostgreSQL  │  │   Neo4j     │  │  Pinecone   │                 │
│  │ (Master)    │  │  (Graph)    │  │  (Vector)   │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 분류 프로세스 상세

#### Stage 1: Parser (포맷 파싱)

다양한 입력 소스의 데이터를 읽어 내부 처리 가능한 형태로 변환합니다.

| 입력 소스 | 입력 형식 | 파서 |
|----------|----------|------|
| LLM 지식 | 마크다운, 텍스트 | MarkdownParser |
| NVD API | JSON (CVE JSON 4.0/5.0) | NVDParser |
| 수동 입력 | CSV, Excel | CSVParser |
| 웹 크롤링 | HTML | HTMLParser |

#### Stage 2: Normalizer (정규화)

파싱된 데이터를 GR Canonical Model로 변환합니다.

**취약점 정규화 예시:**
```python
# 입력 (NVD JSON)
{
  "cve": {
    "id": "CVE-2021-44228",
    "descriptions": [{"lang": "en", "value": "Apache Log4j2..."}]
  },
  "configurations": {...},
  "metrics": {"cvssMetricV31": [{"cvssData": {"baseScore": 10.0}}]}
}

# 출력 (GR Canonical Model)
{
  "vulnerability_id": "CVE-2021-44228",
  "name": "Log4Shell",
  "type": "CVE",
  "severity": "CRITICAL",
  "cvss_score": 10.0,
  "description": "Apache Log4j2...",
  "affected_products": ["log4j-core"],
  "cwe_ids": ["CWE-917", "CWE-502"],
  "references": [...],
  "published_date": "2021-12-10",
  "last_modified": "2024-01-15"
}
```

**제품 정규화 예시:**
```python
# 입력
{"name": "redis-server", "version": "7.0.5"}

# 정규화 과정
# 1. Alias 테이블 조회 → "redis-server" → "Redis"
# 2. 벤더 추론 → "Redis Ltd."
# 3. CPE 생성 → "cpe:2.3:a:redis:redis:7.0.5:*:*:*:*:*:*:*"

# 출력 (GR Canonical Model)
{
  "product_id": "redis",
  "canonical_name": "Redis",
  "vendor": "Redis Ltd.",
  "version": "7.0.5",
  "cpe": "cpe:2.3:a:redis:redis:7.0.5:*:*:*:*:*:*:*",
  "category": "Database",
  "license": "BSD-3-Clause"
}
```

#### Stage 3: Classifier (좌표 할당)

정규화된 데이터에 3D 좌표(Layer × Zone × Tag)를 할당합니다.

**분류 로직:**

```python
# 취약점 분류 로직 (의사 코드)
def classify_vulnerability(vuln):
    # 1. 영향받는 제품에서 Layer 추론
    layers = infer_layers_from_products(vuln.affected_products)

    # 2. 공격 벡터에서 Zone 추론
    zones = infer_zones_from_attack_vector(vuln.attack_vector)

    # 3. 취약점 유형에서 Tag 추론
    tags = infer_tags_from_cwe(vuln.cwe_ids)

    # 4. MITRE ATT&CK 매핑
    mitre = map_to_mitre_techniques(vuln)

    return ClassifiedVulnerability(
        layers=layers,
        zones=zones,
        tags=tags,
        mitre_techniques=mitre
    )
```

**분류 규칙 예시:**

| 조건 | Layer | Zone | Tag |
|------|-------|------|-----|
| CWE-79 (XSS) | Layer 7 | Zone 2 | S1.4 (XSS Protection) |
| CWE-89 (SQL Injection) | Layer 5 | Zone 3 | S1.5 (SQL Injection) |
| CWE-502 (Deserialization) | Layer 7 | Zone 2 | S1.6 (Deserialization) |
| Attack Vector: NETWORK | - | Zone 0-A, Zone 1 | - |
| Attack Vector: LOCAL | - | Zone 5 | - |

#### Stage 4: Validator (검증)

분류된 데이터의 품질을 검증하고 신뢰도 점수를 산출합니다.

**Agreement Score 계산:**
```
Agreement Score = (내부 일관성 × 0.4) + (외부 검증 × 0.4) + (규칙 준수 × 0.2)

- 내부 일관성: Layer/Zone/Tag 조합이 논리적인가?
- 외부 검증: NVD, MITRE 등 외부 소스와 일치하는가?
- 규칙 준수: GR Framework 분류 규칙을 준수하는가?
```

**검증 결과에 따른 처리:**

| Agreement Score | 처리 방법 |
|-----------------|----------|
| ≥ 85% | 자동 승인 → Production DB 적재 |
| 70% ~ 84% | 리뷰 큐 → 전문가 검토 후 승인 |
| < 70% | 거부 → 재분류 또는 수동 처리 |

---

## 4. 데이터 스키마: 무엇을 저장하는가?

### 4.1 기존 스키마 현황

현재 `01_schema.sql`에 정의된 테이블 중 분류 엔진 관련:

```sql
-- 기존 테이블 (요약)
- cve: CVE 기본 정보
- cve_tech_stack_mapping: CVE-제품 매핑
- cve_component_mapping: CVE-컴포넌트 매핑
- mitre_techniques: MITRE ATT&CK 기법
- mitre_cve_mapping: MITRE-CVE 매핑
- staging_cve: 스테이징 영역
```

### 4.2 취약점 스키마 확장 제안

현재 CVE 중심의 스키마를 **통합 취약점 스키마**로 확장합니다:

```sql
-- ============================================
-- 통합 취약점 스키마 (Unified Vulnerability Schema)
-- ============================================

-- 1. 취약점 유형 테이블 (CVE, CWE, OWASP, Named 등)
CREATE TABLE vulnerability_types (
    type_id SERIAL PRIMARY KEY,
    type_code VARCHAR(20) NOT NULL UNIQUE,  -- 'CVE', 'CWE', 'OWASP', 'NAMED', 'MITRE'
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    source_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 통합 취약점 마스터 테이블
CREATE TABLE vulnerabilities (
    vulnerability_id SERIAL PRIMARY KEY,

    -- 식별 정보
    external_id VARCHAR(50) NOT NULL,       -- CVE-2021-44228, CWE-79 등
    type_id INT REFERENCES vulnerability_types(type_id),
    canonical_name VARCHAR(200),            -- Log4Shell, Heartbleed 등 (별칭)

    -- 기본 정보
    title VARCHAR(500),
    description TEXT,
    severity VARCHAR(20),                   -- CRITICAL, HIGH, MEDIUM, LOW, INFO

    -- CVSS 점수
    cvss_v2_score DECIMAL(3,1),
    cvss_v3_score DECIMAL(3,1),
    cvss_v4_score DECIMAL(3,1),
    cvss_vector VARCHAR(200),

    -- 영향 범위
    attack_vector VARCHAR(20),              -- NETWORK, ADJACENT, LOCAL, PHYSICAL
    attack_complexity VARCHAR(20),          -- LOW, HIGH
    privileges_required VARCHAR(20),        -- NONE, LOW, HIGH
    user_interaction VARCHAR(20),           -- NONE, REQUIRED
    scope VARCHAR(20),                      -- UNCHANGED, CHANGED

    -- CIA 영향
    confidentiality_impact VARCHAR(20),     -- NONE, LOW, HIGH
    integrity_impact VARCHAR(20),           -- NONE, LOW, HIGH
    availability_impact VARCHAR(20),        -- NONE, LOW, HIGH

    -- 메타데이터
    published_date DATE,
    last_modified_date DATE,
    source VARCHAR(100),                    -- NVD, MITRE, LLM, MANUAL
    source_url VARCHAR(500),

    -- GR Framework 좌표 (분류 결과)
    primary_layer_id INT REFERENCES layers(layer_id),
    primary_zone_id INT REFERENCES zones(zone_id),

    -- 품질 관리
    agreement_score DECIMAL(5,2),           -- 0.00 ~ 100.00
    classification_status VARCHAR(20),      -- PENDING, AUTO_APPROVED, REVIEWED, REJECTED
    reviewed_by VARCHAR(100),
    reviewed_at TIMESTAMP,

    -- 감사
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(external_id, type_id)
);

-- 3. 취약점-Layer 매핑 (N:M)
CREATE TABLE vulnerability_layers (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    layer_id INT REFERENCES layers(layer_id),
    is_primary BOOLEAN DEFAULT FALSE,
    confidence DECIMAL(3,2),               -- 0.00 ~ 1.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, layer_id)
);

-- 4. 취약점-Zone 매핑 (N:M)
CREATE TABLE vulnerability_zones (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    zone_id INT REFERENCES zones(zone_id),
    is_primary BOOLEAN DEFAULT FALSE,
    attack_direction VARCHAR(20),          -- INBOUND, OUTBOUND, LATERAL
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, zone_id)
);

-- 5. 취약점-Tag 매핑 (N:M)
CREATE TABLE vulnerability_tags (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    tag_id INT REFERENCES tags(tag_id),
    tag_role VARCHAR(20),                  -- PRIMARY, SECONDARY, RELATED
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, tag_id)
);

-- 6. 취약점-제품 매핑 (N:M) - 기존 테이블 확장
CREATE TABLE vulnerability_products (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    product_id INT REFERENCES products(product_id),
    affected_versions VARCHAR(500),        -- 영향받는 버전 범위
    fixed_version VARCHAR(100),            -- 패치된 버전
    cpe_match VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, product_id)
);

-- 7. 취약점-CWE 매핑 (N:M)
CREATE TABLE vulnerability_cwes (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    cwe_id VARCHAR(20),                    -- CWE-79, CWE-89 등
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, cwe_id)
);

-- 8. 취약점-MITRE ATT&CK 매핑 (N:M)
CREATE TABLE vulnerability_mitre (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    technique_id INT REFERENCES mitre_techniques(technique_id),
    mapping_confidence VARCHAR(20),        -- HIGH, MEDIUM, LOW
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, technique_id)
);

-- 9. 취약점 별칭 테이블
CREATE TABLE vulnerability_aliases (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    alias_name VARCHAR(200) NOT NULL,      -- Log4Shell, Heartbleed 등
    alias_type VARCHAR(50),                -- COMMON_NAME, VENDOR_NAME, MEDIA_NAME
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(vulnerability_id, alias_name)
);

-- 10. 취약점 참조 링크 테이블
CREATE TABLE vulnerability_references (
    id SERIAL PRIMARY KEY,
    vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id),
    ref_type VARCHAR(50),                  -- ADVISORY, PATCH, EXPLOIT, ARTICLE
    ref_source VARCHAR(100),               -- NVD, VENDOR, GITHUB, EXPLOIT-DB
    ref_url VARCHAR(1000),
    ref_name VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. 취약점 스테이징 테이블 (배치 처리용)
CREATE TABLE staging_vulnerabilities (
    staging_id SERIAL PRIMARY KEY,

    -- 원본 데이터
    raw_data JSONB,
    source VARCHAR(100),

    -- 파싱/정규화 결과
    parsed_data JSONB,
    canonical_data JSONB,

    -- 분류 결과
    classified_data JSONB,

    -- 처리 상태
    processing_status VARCHAR(20),          -- RECEIVED, PARSING, NORMALIZING, CLASSIFYING, VALIDATING, COMPLETED, FAILED
    error_message TEXT,

    -- 품질 점수
    agreement_score DECIMAL(5,2),

    -- 배치 정보
    batch_id VARCHAR(100),

    -- 타임스탬프
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,

    -- 최종 적재된 vulnerability_id (있으면)
    final_vulnerability_id INT REFERENCES vulnerabilities(vulnerability_id)
);

-- ============================================
-- 인덱스
-- ============================================
CREATE INDEX idx_vuln_external_id ON vulnerabilities(external_id);
CREATE INDEX idx_vuln_type ON vulnerabilities(type_id);
CREATE INDEX idx_vuln_severity ON vulnerabilities(severity);
CREATE INDEX idx_vuln_cvss_v3 ON vulnerabilities(cvss_v3_score);
CREATE INDEX idx_vuln_status ON vulnerabilities(classification_status);
CREATE INDEX idx_vuln_layer ON vulnerability_layers(layer_id);
CREATE INDEX idx_vuln_zone ON vulnerability_zones(zone_id);
CREATE INDEX idx_vuln_tag ON vulnerability_tags(tag_id);
CREATE INDEX idx_vuln_product ON vulnerability_products(product_id);
CREATE INDEX idx_staging_status ON staging_vulnerabilities(processing_status);
CREATE INDEX idx_staging_batch ON staging_vulnerabilities(batch_id);
```

### 4.3 스키마 관계도

```
┌─────────────────────┐
│ vulnerability_types │
└──────────┬──────────┘
           │ 1:N
           ▼
┌─────────────────────┐       ┌─────────────────┐
│   vulnerabilities   │──────▶│ vulnerability_  │
│                     │ 1:N   │ aliases         │
│  - external_id      │       └─────────────────┘
│  - type_id          │
│  - canonical_name   │       ┌─────────────────┐
│  - severity         │──────▶│ vulnerability_  │
│  - cvss_score       │ 1:N   │ references      │
│  - agreement_score  │       └─────────────────┘
└─────────┬───────────┘
          │
    ┌─────┼─────┬─────────┬─────────┬─────────┐
    │     │     │         │         │         │
    ▼     ▼     ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌─────────┐ ┌───────┐ ┌───────┐
│layers │ │zones  │ │  tags   │ │products│ │ mitre │
│(N:M)  │ │(N:M)  │ │ (N:M)   │ │(N:M)   │ │(N:M)  │
└───────┘ └───────┘ └─────────┘ └────────┘ └───────┘
```

---

## 5. 구현 전략: 어떻게 만드는가?

### 5.1 기술 스택

| 구성 요소 | 기술 | 이유 |
|----------|------|------|
| **언어** | Python 3.11+ | 데이터 처리, NLP, DB 연동 생태계 최강 |
| **DB 연동** | psycopg2, neo4j-driver, pinecone-client | 3개 DB 모두 지원 |
| **데이터 처리** | pandas, pydantic | 대량 데이터 + 스키마 검증 |
| **NLP/분류** | spaCy, scikit-learn | 텍스트 분류 |
| **HTTP 클라이언트** | httpx, aiohttp | NVD API 등 외부 연동 |
| **스케줄링** | APScheduler, Celery | 배치 처리 |
| **환경** | Ubuntu 22.04 LTS | 안정성, Docker 호환 |

### 5.2 프로젝트 구조

```
classification_engine/
├── pyproject.toml              # 의존성 관리
├── README.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                   # 핵심 모듈
│   │   ├── __init__.py
│   │   ├── models.py           # Pydantic 데이터 모델
│   │   ├── config.py           # 설정 관리
│   │   └── exceptions.py       # 커스텀 예외
│   │
│   ├── parsers/                # Stage 1: 파서
│   │   ├── __init__.py
│   │   ├── base.py             # 파서 인터페이스
│   │   ├── markdown_parser.py  # LLM 지식 파싱
│   │   ├── nvd_parser.py       # NVD JSON 파싱
│   │   ├── csv_parser.py       # CSV/Excel 파싱
│   │   └── html_parser.py      # 웹 크롤링 파싱
│   │
│   ├── normalizers/            # Stage 2: 정규화
│   │   ├── __init__.py
│   │   ├── base.py             # 정규화 인터페이스
│   │   ├── vulnerability_normalizer.py
│   │   └── product_normalizer.py
│   │
│   ├── classifiers/            # Stage 3: 분류기
│   │   ├── __init__.py
│   │   ├── base.py             # 분류기 인터페이스
│   │   ├── layer_classifier.py
│   │   ├── zone_classifier.py
│   │   ├── tag_classifier.py
│   │   └── mitre_mapper.py
│   │
│   ├── validators/             # Stage 4: 검증기
│   │   ├── __init__.py
│   │   ├── base.py             # 검증기 인터페이스
│   │   ├── schema_validator.py
│   │   ├── consistency_validator.py
│   │   └── agreement_scorer.py
│   │
│   ├── db/                     # 데이터베이스 연동
│   │   ├── __init__.py
│   │   ├── postgres.py
│   │   ├── neo4j.py
│   │   └── pinecone.py
│   │
│   ├── pipeline/               # 파이프라인 오케스트레이션
│   │   ├── __init__.py
│   │   ├── classification_pipeline.py
│   │   └── batch_processor.py
│   │
│   └── api/                    # REST API (선택적)
│       ├── __init__.py
│       └── routes.py
│
├── data/                       # 데이터 파일
│   ├── input/                  # 입력 데이터
│   │   ├── vulnerabilities/    # 취약점 리스트
│   │   └── products/           # 제품 리스트
│   ├── mappings/               # 매핑 규칙
│   │   ├── layer_rules.yaml
│   │   ├── zone_rules.yaml
│   │   └── tag_rules.yaml
│   └── output/                 # 출력 데이터
│
├── tests/                      # 테스트
│   ├── __init__.py
│   ├── test_parsers.py
│   ├── test_normalizers.py
│   ├── test_classifiers.py
│   └── test_validators.py
│
└── scripts/                    # 유틸리티 스크립트
    ├── init_db.py              # DB 초기화
    ├── load_vulnerabilities.py # 취약점 일괄 로드
    └── export_report.py        # 리포트 생성
```

### 5.3 개발 단계 (Phase)

#### Phase 1: 기반 구축 (Foundation)

**목표**: 기본 파이프라인 동작

- [ ] 프로젝트 구조 생성
- [ ] 데이터 모델 정의 (Pydantic)
- [ ] PostgreSQL 연결 및 스키마 생성
- [ ] 마크다운 파서 구현 (LLM 지식 입력용)
- [ ] 기본 정규화/분류 로직

**산출물**:
- 취약점 리스트 문서화 (LLM 지식 기반)
- 기본 분류 결과 DB 적재

#### Phase 2: 분류 고도화 (Enhancement)

**목표**: 정확한 3D 좌표 할당

- [ ] Layer 분류기 구현 (규칙 기반)
- [ ] Zone 분류기 구현 (공격 벡터 기반)
- [ ] Tag 분류기 구현 (CWE 매핑)
- [ ] MITRE ATT&CK 매핑
- [ ] Agreement Score 계산

**산출물**:
- 완전한 3D 좌표가 부여된 취약점 DB
- 분류 정확도 리포트

#### Phase 3: 외부 연동 (Integration)

**목표**: 외부 데이터 소스 연동

- [ ] NVD API 연동 (CVE Feed)
- [ ] 웹 크롤러 구현 (Exploit-DB 등)
- [ ] 배치 처리 스케줄러
- [ ] Neo4j/Pinecone 동기화

**산출물**:
- 자동화된 취약점 업데이트 파이프라인
- 그래프/벡터 DB 동기화

#### Phase 4: 품질 관리 (Quality)

**목표**: 데이터 품질 보증

- [ ] 스테이징-프로덕션 워크플로우
- [ ] 리뷰 큐 대시보드
- [ ] 품질 감사 리포트
- [ ] 충돌 병합 로직

**산출물**:
- 품질 관리 대시보드
- 데이터 거버넌스 프로세스

---

## 6. 1차 목표: LLM 지식 기반 취약점 리스트업

### 6.1 즉시 실행 계획

분류 엔진 개발의 첫 단계로, **Claude의 지식을 활용한 취약점 리스트업**을 수행합니다.

```
목표: Claude가 알고 있는 주요 취약점들을 체계적으로 문서화

출력 위치: 프로젝트2_GR FrameWork/GR_DB/취약점_리스트/

파일 구조:
├── 00_취약점_분류_기준.md      # 분류 기준 설명
├── 01_CVE_주요취약점.md        # CVE 기반 주요 취약점
├── 02_CWE_취약점유형.md        # CWE 취약점 유형 분류
├── 03_OWASP_Top10.md           # OWASP Top 10
├── 04_Named_취약점.md          # 명명된 유명 취약점
└── 05_MITRE_ATT&CK_기법.md     # MITRE ATT&CK 공격 기법
```

### 6.2 각 문서의 포맷

**예시: Named 취약점**

```markdown
# Named Vulnerabilities (명명된 취약점)

## Heartbleed
- **CVE**: CVE-2014-0160
- **영향 제품**: OpenSSL 1.0.1 ~ 1.0.1f
- **심각도**: HIGH (CVSS 7.5)
- **CWE**: CWE-126 (Buffer Over-read)
- **요약**: TLS heartbeat 확장의 버퍼 오버리드 취약점
- **GR 좌표 (예상)**:
  - Layer: Layer 2 (Network), Layer 7 (Application)
  - Zone: Zone 1 (Perimeter)
  - Tag: S5.1 (TLS/SSL), N2.1 (Reverse Proxy)

## Log4Shell
- **CVE**: CVE-2021-44228
- ...
```

### 6.3 다음 단계

1. **취약점 리스트 문서화** ← 현재 단계
2. **취약점 스키마 SQL 생성**
3. **분류 엔진 기본 구조 구현**
4. **문서 → DB 적재 파이프라인**

---

## 7. 결론

### 7.1 분류 엔진의 본질

> **"분류 엔진은 GR 생태계의 '입구'이며, 외부 세계의 혼돈을 내부의 질서로 변환하는 관문입니다."**

### 7.2 핵심 가치

| 가치 | 설명 |
|------|------|
| **표준화** | 다양한 소스 → 단일 Canonical Model |
| **좌표화** | 모든 데이터에 3D 좌표 (Layer × Zone × Tag) |
| **품질 보증** | Agreement Score 기반 자동/수동 검증 |
| **확장성** | 새로운 소스 추가 용이한 파서 아키텍처 |

### 7.3 성공 기준

- [ ] 1,000+ 취약점이 3D 좌표와 함께 DB에 적재
- [ ] Agreement Score ≥ 85% 자동 승인율 70% 이상
- [ ] NVD 신규 CVE 24시간 내 자동 분류
- [ ] 제품-취약점 매핑 정확도 95% 이상

---

## 부록: 용어 정의

| 용어 | 정의 |
|------|------|
| **Canonical Model** | 다양한 소스의 데이터를 통일된 형식으로 변환한 표준 모델 |
| **Agreement Score** | 분류 결과의 신뢰도 점수 (0-100%) |
| **3D 좌표** | Layer × Zone × Tag로 구성된 GR Framework 분류 체계 |
| **Named Vulnerability** | Heartbleed, Log4Shell 등 별칭이 붙은 유명 취약점 |
| **CPE** | Common Platform Enumeration, 제품 식별 표준 |

---

**[문서 끝]**
