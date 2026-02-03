# GR 생태계 마스터플랜 v2.2
# GR Ecosystem Masterplan v2.2

> **"Foundation, not Product - AI를 위한 보안 지능의 토대"**

---

## 📋 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 생태계 마스터플랜 v2.2 |
| **버전** | 2.2 (2025-01-20) |
| **목적** | GR 생태계의 비전, 전략, 아키텍처를 정의하는 최상위 문서 |
| **대상 독자** | 투자자, 파트너사, 신규 팀원, 기술 의사결정자 |
| **이전 버전** | v2.1 (GR_생태계_마스터플랜_v2.1.md) |
| **주요 변경** | 구체적 기간 표현을 추상적 단계 표현으로 변경 (초기/중기/확장 단계, 성장기/성숙기) |

---

## 🎯 1. 비전 & 철학 (Vision & Philosophy)

### "From Classification to Intelligence"

GR(Gotroot) 생태계는 전 세계의 모든 IT 인프라 제품과 기술을 **'보안 지능(Security Intelligence)'이 이해할 수 있는 언어**로 번역하고 구조화하는 토대입니다.

### 핵심 철학

**1. Foundation, not Product (토대, 제품이 아님)**
- 우리는 특정 보안 솔루션을 만들지 않습니다
- 모든 보안 제품이 공통으로 사용할 **'보안의 표준 언어와 좌표계'**를 만듭니다
- GR DB와 GR Framework는 상품이 아니라 **생태계의 기초 인프라**입니다

**2. Context-Aware Security (맥락 기반 보안)**
- 제품 자체가 아니라, 그 제품이 **'어디서(Zone/Layer) 무엇을(Tag) 하는가'**에 따라 보안 정책을 결정합니다
- 같은 Nginx라도 프록시로 쓰면 Layer 2, 웹서버로 쓰면 Layer 7의 보안 정책을 적용합니다

**3. AI-First Architecture (AI 우선 설계)**
- 사람이 읽기 위한 문서가 아니라, **AI가 학습하고 추론하기 위한 데이터셋**으로 설계합니다
- RAG(Retrieval-Augmented Generation)를 통해 할루시네이션 없는 정확한 보안 진단을 제공합니다

---

## 🏗️ 2. 핵심 개념: Foundation vs Product

GR 생태계는 **계층 구조**로 이루어져 있습니다. 각 계층의 역할을 명확히 구분하는 것이 중요합니다.

### 생태계 계층 구조

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
│  - 3차원 좌표계 (Layer × Zone × Tag)                        │
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

### 각 계층의 정의

| 계층 | 명칭 | 역할 | 비유 | 수익 모델 |
|------|------|------|------|----------|
| **Layer 1** | GR DB | 보안의 위키피디아, AI 학습 원천 데이터 | 도서관 | 무료 (투자 기반) |
| **Layer 2** | GR Framework | 데이터를 해석하는 규칙과 좌표계 | 문법책 | 무료 (오픈 스탠다드) |
| **Layer 3** | AI/RAG | GR DB를 참조하여 상황에 맞는 답을 추론 | 전문가 | API 사용료 |
| **Layer 4** | Products | 고객의 문제를 해결하는 구체적 서비스 | 의사/변호사 | SaaS 구독료 |

### 기능 (Feature) vs 제품 (Product)

**GR Atlas**는 제품이 아니라 **기능(Feature)**입니다.
- Atlas = 3D 시각화 뷰어
- 자동화 진단 솔루션, IaC, Edu에 **내장되는 공통 컴포넌트**

---

## 📐 3. 3차원 프레임워크 v2.0 (3D Framework)

AI가 인프라를 입체적으로 인식하기 위한 3축 좌표계입니다.

### 축 1: Deployment Layer (기술 스택의 수직적 깊이)

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
| **L7** | 애플리케이션 & AI | Application & AI Logic | 비즈니스 로직 및 AI 워크로드 | Very High | Web App, **LLM Model**, **Vector Search**, **RAG Pipeline** |
| **Cross** | 관리 & 보안 | Management & Security | 모든 계층 관통 | Medium | Monitoring, IAM, SIEM, Testing |

**v2.0 주요 변경**:
- ✅ **Layer 0 신설**: SaaS/API 서비스를 명시적으로 분리
- ✅ **Layer 7 확장**: AI 워크로드 (LLM, Embedding Model, Vector DB, Agentic Workflow) 포함

---

### 축 2: Security Zone (보안 신뢰의 수평적 경계)

**AI의 관점**: "이곳은 얼마나 위험한가? 누구와 대화할 수 있는가?"

| Zone | 명칭 | 신뢰도 | 설명 | 보안 원칙 | 예시 구성요소 |
|------|------|--------|------|----------|--------------|
| **Zone 0-A** | 비신뢰 외부 | 0% | 일반 인터넷, 해커, 익명 사용자 | Default Deny | - |
| **Zone 0-B** | 신뢰 파트너 | 10% | API Key로 인증된 외부 SaaS/Partner | Allow with Auth | OpenAI API, GitHub, Slack |
| **Zone 1** | 경계 영역 (Perimeter) | 0-20% | 외부 위협 차단 최전선 (DMZ) | 최대 강도 필터링 | Firewall, WAF, DDoS 방어 |
| **Zone 2** | 애플리케이션 영역 | 30% | 비즈니스 로직 실행 영역 | 인증/인가 필수 | Web Server, API Server |
| **Zone 3** | 데이터 영역 | 60% | 가장 민감한 자산 보관 | 격리 + 암호화 | Database, 파일 스토리지 |
| **Zone 4** | 관리 영역 (Management) | 80% | 시스템 전체 통제 관제탑 | 최고 수준 접근 제어 | 모니터링, 로깅, CI/CD |
| **Zone 5** | 엔드포인트 영역 | 50% | 제로 트러스트 기반 사용자 단말 | 지속적 검증 | 사용자 PC, 모바일, VPN Client |

**v2.0 주요 변경**:
- ✅ **Zone 0 세분화**: 0-A (Untrusted) vs 0-B (Trusted Partner) 분리
- ✅ **신뢰도 수치화**: AI가 리스크를 계산할 수 있도록 신뢰 수준 명시

---

### 축 3: Function Tag & Attributes (기능과 속성)

**AI의 관점**: "이 녀석의 정체는 무엇이고, 어떤 DNA를 가졌는가?"

#### 기존 기능 도메인 (8개)

| 코드 | 도메인명 (한글) | 도메인명 (영문) | 태그 개수 | 설명 |
|------|----------------|----------------|----------|------|
| **M** | 관리 기능 | Management | 20개 | 모니터링, 로깅, 백업 |
| **N** | 네트워크 기능 | Network | 35개 | 라우팅, 로드밸런싱, 프록시 |
| **S** | 보안 기능 | Security | 40개 | 인증, 암호화, 위협 탐지 |
| **A** | 애플리케이션 기능 | Application | 30개 | 웹서버, API, UI/UX |
| **D** | 데이터 기능 | Data | 35개 | 저장, 처리, 분석 |
| **R** | 런타임 기능 | Runtime | 25개 | 컨테이너, 메시징, 캐시 |
| **C** | 컴퓨팅 기능 | Computing | 20개 | 가상화, 오케스트레이션 |
| **P** | 플랫폼 기능 | Platform | 20개 | CI/CD, IaC, 버전 관리 |

#### 신규 속성 도메인 (2개) - v2.0

| 코드 | 도메인명 (한글) | 도메인명 (영문) | 태그 개수 | 설명 | 목적 |
|------|----------------|----------------|----------|------|------|
| **T** | 기술 스택 | Tech Stack | 30개 | 언어, 런타임, OS | **CVE 영향도 분석** |
| **I** | 인터페이스 | Interface | 25개 | 프로토콜, 데이터 포맷 | **통신 흐름 분석** |

**Domain T (Tech Stack) 예시**:
- `T1.1` Java
- `T1.2` Python
- `T1.3` Go
- `T1.4` Node.js
- `T2.1` JVM
- `T2.2` .NET CLR
- `T3.1` Linux
- `T3.2` Windows

**Domain I (Interface) 예시**:
- `I1.1` HTTP/1.1
- `I1.2` HTTP/2
- `I1.3` gRPC
- `I1.4` WebSocket
- `I2.1` JSON
- `I2.2` XML
- `I2.3` Protobuf

**v2.0 주요 변경**:
- ✅ **Domain T 신설**: 취약점(CVE) 매핑을 위한 기술 스택 속성
- ✅ **Domain I 신설**: 네트워크 정책 자동화를 위한 인터페이스 속성
- ✅ **총 10개 도메인**, 약 **280개 태그**로 확장

---

## 🗄️ 4. 데이터 아키텍처 (Data Architecture)

### 하이브리드 데이터베이스 전략

GR DB는 **단일 DB가 아닌 3개 DB의 조합**입니다. 각 DB는 특화된 역할을 수행합니다.

```
┌─────────────────────────────────────────────────────────┐
│               API Gateway (FastAPI)                     │
│          단일 진입점, 쿼리 라우팅 및 조합                 │
└────────────┬───────────────┬────────────────┬───────────┘
             │               │                │
             ▼               ▼                ▼
    ┌─────────────┐  ┌──────────────┐  ┌─────────────┐
    │ PostgreSQL  │  │   Neo4j      │  │  Pinecone   │
    │  (Master)   │  │ (Graph DB)   │  │ (Vector DB) │
    └─────────────┘  └──────────────┘  └─────────────┘
         │                  │                  │
         │                  │                  │
    [Product Info]    [Relationships]    [Embeddings]
    - Name            - Zone → Layer    - 설명 벡터
    - Vendor          - Tag → Product   - 스펙 벡터
    - CPE             - Attack Path     - 유사도 검색
    - Version         - Dependency
    - License         - CVE Impact
```

### DB별 역할 분담

| Database | 역할 | 저장 데이터 | 핵심 쿼리 | 선택 이유 |
|----------|------|------------|----------|----------|
| **PostgreSQL** | Master (불변 팩트) | Product 정보, Vendor, CPE, License, Version | `SELECT * WHERE vendor='Apache'` | ACID 보장, 트랜잭션 지원 |
| **Neo4j** | Relationships (관계) | Zone↔Layer 연결, Tag 조합, 공격 경로, 의존성 | `MATCH (a)-[*]->(b) RETURN path` | 관계 탐색 최적화, 그래프 쿼리 |
| **Pinecone** | Semantics (의미) | 제품 설명 임베딩, 스펙 벡터 | `similarity_search(vector, k=10)` | 고속 벡터 검색, RAG 최적화 |

### 데이터 흐름 예시

**사용자 질문**: "Nginx와 비슷한 역할을 하는 제품을 찾아줘"

```
1. API Gateway가 질문을 받음
2. Vector DB (Pinecone)에서 "Nginx 설명 벡터"와 유사한 제품 10개 검색
   → 결과: [Apache, HAProxy, Traefik, Envoy, ...]
3. Graph DB (Neo4j)에서 각 제품의 Archetype(역할) 조회
   → "Apache는 Reverse Proxy + Web Server 역할 가능"
4. PostgreSQL에서 각 제품의 상세 정보 조회
   → Vendor, Version, License, EOL 등
5. API Gateway가 결과를 통합하여 반환
```

### 인프라 비용 (초기)

| 항목 | 서비스 | 규모 | 월 비용 | 연 비용 |
|------|--------|------|---------|---------|
| PostgreSQL | AWS RDS | db.t3.medium | $50 | $600 |
| Neo4j | AuraDB Professional | 1 instance | $200 | $2,400 |
| Pinecone | Serverless (100k vectors) | 1 pod | $70 | $840 |
| OpenAI API | Embedding (ada-002) | 100개 제품 | $100 | $1,200 |
| **합계** | - | - | **$420** | **$5,040** |

---

## 🤖 5. LLM 전략 (LLM Strategy)

### LLM 사용 전략: Phase별 구분

GR 생태계는 **데이터 구축 단계**와 **고객 배포 단계**에서 LLM 사용 전략이 명확히 다릅니다.

#### Phase 0-2: GR DB 구축 단계

**목표**: 10,000개 제품 × 평균 3개 Archetype = 30,000개 지식 노드 구축

**LLM 사용**:
- ✅ **외부 LLM API 자유 사용**
  - GPT-4 (추론), Claude (분석), Gemini (검증)
  - 제품 설명 → Archetype 추론
  - 공식 문서 → Function Tag 추출
  - CVE 설명 → MITRE Technique 매핑

**비용 구조** (연간):
```yaml
OpenAI API:
  - Embedding (ada-002): $500/년 (10,000개 제품)
  - GPT-4 (추론): $300/년 (월 100개 제품 처리)

Anthropic Claude API:
  - Claude 3.5 Sonnet (분석): $200/년

합계: ~$1,000/년
```

**데이터 안전성**:
- ✅ 모두 공개 데이터 (제품 정보, CVE, 공식 문서)
- ✅ 기밀 정보 없음 → 외부 API 사용 안전

---

#### Phase 2+: 고객 배포 단계

**목표**: 고객사 인프라 분석 및 보안 진단

**80/20 원칙**: Direct Query 80% + AI-Assisted 20%

**80% Direct Query (AI 불필요)**:
```python
# Case 1: 제품 태그 조회 (단순 DB 쿼리)
def get_product_tags(product_name: str):
    """
    PostgreSQL + Neo4j 직접 쿼리
    - 응답 시간: 50ms
    - 정확도: 100%
    - 비용: $0
    - 기밀 안전: ✅
    """
    return db.execute("""
        SELECT p.name, a.role, a.layer, a.zone, array_agg(t.tag_code)
        FROM products p
        JOIN archetypes a ON p.id = a.product_id
        WHERE p.name = %s
    """, [product_name])

# Case 2: Zone 간 통신 경로 검증
def check_communication_allowed(
    source_zone: str,
    target_zone: str
):
    """
    Neo4j 그래프 쿼리
    - 응답 시간: 100ms
    - 정확도: 100%
    - 비용: $0
    """
    return neo4j.execute("""
        MATCH path = (z1:Zone {code: $source})
                    -[:ALLOWS_COMMUNICATION*1..3]->
                     (z2:Zone {code: $target})
        RETURN EXISTS(path)
    """, {"source": source_zone, "target": target_zone})
```

**20% AI-Assisted (복잡한 추론 필요)**:
```python
# Case 3: 공격 경로 시뮬레이션 (AI 필요)
def analyze_attack_path(infrastructure_data: dict):
    """
    옵션 1: On-premise LLM (기밀 유지)
    - 고객사 내부 서버에 설치
    - Llama 3.1 (8B), Mistral (7B) 등
    - 초기 비용: $10K~$50K (GPU 서버)
    - 기밀 완벽 보장

    옵션 2: 익명화 후 외부 LLM
    - 민감 정보 마스킹 (IP, 도메인, 계정명)
    - 구조만 외부 LLM에 전송
    - GPT-4, Claude API 사용
    - 비용: 월 $100~$500
    """
    # Neo4j에서 공격 경로 그래프 추출
    attack_paths = neo4j.execute(...)

    # LLM으로 위험도 분석 및 대응 방안 생성
    analysis = llm.generate(
        prompt=f"Analyze attack paths: {attack_paths}",
        model="llama-3.1-8b-instruct"  # On-premise
    )

    return analysis
```

**비용 비교**:
| 방식 | 응답 속도 | 정확도 | 월 비용 | 기밀 안전성 |
|------|----------|--------|---------|------------|
| Direct Query (80%) | 50-100ms | 100% | $0 | ✅ 완벽 |
| On-premise LLM (20%) | 500ms-2s | 95% | $0 (운영비만) | ✅ 완벽 |
| External LLM (20%) | 1-3s | 98% | $100-$500 | ⚠️ 익명화 필요 |

### 자체 AI 모델 개발 계획 (Phase 3: 성숙기)

**Phase 3 (성숙기)**:
- GR DB 기반 Fine-tuned LLM 개발
- 30,000+ Archetype 데이터로 학습
- 보안 도메인 특화 모델

**비용 분석**:
```yaml
Self-Hosted LLM:
  initial_cost: $50,000 (GPU 서버 + 개발)
  annual_operating: $10,000 (전기, 유지보수)
  breakeven: 장기적으로 외부 API 대비 비용 효율적

External API (계속 사용):
  annual_cost: $1,000 (초기 단계)
  long_term_total: 누적 비용 증가

결론: Phase 0-2는 외부 API가 효율적, Phase 3부터 자체 모델 고려
```

---

## 🧬 6. 데이터 모델: 원자화 전략 (Data Model)

### 2-Tier 구조

GR DB는 제품을 **2단계로 분해**하여 저장합니다.

#### Tier 1: Product Master (불변의 팩트)

**저장 위치**: PostgreSQL
**성격**: 변하지 않는 제품의 객관적 정보

**스키마 예시**:
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,              -- 제품명
    vendor VARCHAR(200),                     -- 개발사/재단
    cpe VARCHAR(500),                        -- CVE 매칭용 식별자
    license VARCHAR(100),                    -- 라이선스 타입
    primary_language VARCHAR(50),            -- 주 개발 언어
    release_date DATE,                       -- 출시일
    eol_date DATE,                           -- 기술지원 종료일
    source_url TEXT,                         -- GitHub 등 소스 주소
    description TEXT,                        -- 제품 설명
    created_at TIMESTAMP DEFAULT NOW()
);
```

**예시 데이터 (Redis)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Redis",
  "vendor": "Redis Ltd.",
  "cpe": "cpe:2.3:a:redis:redis:*:*:*:*:*:*:*:*",
  "license": "RSALv2 / SSPL",
  "primary_language": "C",
  "release_date": "2009-05-10",
  "eol_date": null,
  "source_url": "https://github.com/redis/redis",
  "description": "In-memory data structure store, used as database, cache, and message broker"
}
```

---

#### Tier 2: Component Archetypes (가능한 역할들)

**저장 위치**: Neo4j (Graph) + Pinecone (Vector)
**성격**: 하나의 제품이 가질 수 있는 **모든 변신 형태**

**핵심 개념**:
- 하나의 제품(Product)은 여러 개의 Archetype(원형)을 가질 수 있습니다
- Archetype = "이 제품을 이렇게 쓰면, 이런 좌표에 배치되고, 이런 보안 정책이 적용된다"

**Neo4j 그래프 모델**:
```
(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:Cache)
                                     ├─ layer: "L5"
                                     ├─ zone: "Zone2"
                                     ├─ primary_tag: "D3.1"
                                     └─ use_case: "Application cache"

(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:SessionStore)
                                     ├─ layer: "L5"
                                     ├─ zone: "Zone3"
                                     ├─ primary_tag: "D3.3"
                                     └─ use_case: "Session management"

(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:MessageBroker)
                                     ├─ layer: "L6"
                                     ├─ zone: "Zone2"
                                     ├─ primary_tag: "R3.2"
                                     └─ use_case: "Pub/Sub messaging"
```

**예시 데이터 구조**:

| Archetype ID | Product | 역할 (Role) | Layer | Zone | Primary Tag | Secondary Tags | 설명 |
|--------------|---------|------------|-------|------|-------------|----------------|------|
| arch-001 | Redis | Cache | L5 | Zone 2 | D3.1 | P2.1, M1.3 | 애플리케이션 전용 캐시 |
| arch-002 | Redis | Session Store | L5 | Zone 3 | D3.3 | S2.2 | 중요 세션 저장소 |
| arch-003 | Redis | Message Broker | L6 | Zone 2 | R3.2 | I1.4 | Pub/Sub 메시징 큐 |

### 원자화 프로세스

**Step 1**: AI가 제품 문서 분석
```python
# LLM에게 질문
prompt = f"""
Redis의 공식 문서를 분석하여, GR Framework의 Function Tag 목록 중
매칭되는 기능을 모두 찾아내고, 각 기능별로 적합한 Layer와 Zone을 추천해줘.

Function Tag 목록: [D3.1 (Cache), D3.3 (Session Store), R3.2 (Message Queue), ...]
"""
```

**Step 2**: AI가 제안한 Archetype 후보
```
후보 1: Cache (D3.1 / L5 / Zone 2) - 신뢰도 95%
후보 2: Message Broker (R3.2 / L6 / Zone 2) - 신뢰도 90%
후보 3: Session Store (D3.3 / L5 / Zone 3) - 신뢰도 85%
후보 4: Database (D2.2 / L5 / Zone 3) - 신뢰도 60% (AI 오판 가능)
```

**Step 3**: 보안 전문가가 검증 및 승인
```
✅ 후보 1, 2, 3 승인 → GR DB에 적재
❌ 후보 4 기각 → Redis를 DB로 쓰는 건 안티패턴
```

---

## 📅 7. 제품 로드맵 (Product Roadmap)

### Phase 0: MVP & PoC (초기 단계)

**목표**: 100개 핵심 제품으로 전체 시스템 검증 및 첫 고객 확보

**주요 작업**:
```yaml
초기 작업: 인프라 구축
  - PostgreSQL, Neo4j, Pinecone 설정
  - FastAPI 기본 엔드포인트 개발

핵심 데이터 구축: 데이터 입력 (100개 제품)
  대상: Apache, Nginx, MySQL, PostgreSQL, Redis, MongoDB,
        Kafka, RabbitMQ, Kubernetes, Docker, Terraform,
        AWS 주요 서비스 (EC2, RDS, S3, Lambda 등), ...
  방법: 수작업 입력 (보안 전문가 직접 검수)

AI 파이프라인 개발: AI 파이프라인 v0.1
  - LLM 기반 Archetype 제안 엔진
  - 간단한 Atlas 3D 시각화

검증 및 고객 확보: PoC 고객 확보
  - 1~2개 Early Adopter 계약
  - 피드백 수집
```

**산출물**:
- GR DB v0.1 (100개 제품, 300개 Archetype)
- 자동화 진단 솔루션 MVP
- 투자 유치 자료 (실제 데이터 기반)

**예상 비용**: $15,000 (인프라 $5K + 인건비 $10K)

---

### Phase 1: AI 자동화 & 확장 (중기 단계)

**목표**: 1,000개 제품 확장 및 AI 파이프라인 완성

**주요 작업**:
```yaml
전반부: AI 자동화 엔진
  - 크롤러: 제품 문서 자동 수집
  - LLM Agent: Archetype 자동 추론
  - 전문가 검증 UI: 승인/기각 대시보드

중반부: 데이터 확장
  - 1,000개 주요 오픈소스/상용 제품 매핑
  - CVE 데이터베이스 연동 (NVD, MITRE)

후반부: 첫 번째 제품 출시
  - 자동화 진단 솔루션 정식 버전
  - 초기 유료 고객 확보
```

**산출물**:
- GR DB v1.0 (1,000개 제품, 3,000개 Archetype)
- 자동화 진단 솔루션 (유료 SaaS)
- 5~10개 유료 고객

**예상 비용**: $100,000 (인프라 $20K + 인건비 $80K)

---

### Phase 2: 생태계 완성 (확장 단계)

**목표**: 10,000개 제품 완성 및 파생 제품 출시

**주요 작업**:
```yaml
전반부: 데이터 대량 확장
  - 10,000개 제품 (롱테일 제품 포함)
  - Graph 깊이 확장 (공격 경로, 의존성 체인)

중반부: GR IaC 출시
  - "쇼핑몰 인프라 만들어줘" → Terraform 코드 자동 생성
  - 보안 정책이 내장된 IaC

후반부: GR Edu 출시
  - 실전 시뮬레이션 환경
  - CVE 실습 플랫폼
```

**산출물**:
- GR DB v2.0 (10,000개 제품)
- 3개 제품 포트폴리오 (진단, IaC, Edu)
- 시장 확대 및 고객 다각화

**예상 비용**: $500,000 (인프라 $50K + 인건비 $450K)

---

## 💰 8. 비즈니스 모델 (Business Model)

### 수익 구조

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

### 타겟 고객

| 고객 유형 | 니즈 | 제품 | ARR 예상 |
|----------|------|------|----------|
| **중견기업** | 인프라 현황 파악 | 자동화 진단 | $10K~$30K |
| **대기업** | 멀티클라우드 통합 관리 | 진단 + IaC | $50K~$200K |
| **보안 컨설팅사** | GR DB API 사용 | API 라이선스 | $6K~$20K |
| **교육기관** | 보안 실습 환경 | GR Edu | $2K~$10K |

### 단계별 ARR 목표

| 단계 | Phase | 고객 수 | 평균 단가 | ARR 목표 | 누적 투자 |
|------|-------|---------|----------|---------|----------|
| 초기 단계 | Phase 0-1 | 10 | $10K | $100K | $115K |
| 중기 단계 | Phase 1-2 | 50 | $20K | $1M | $600K |
| 확장 단계 | Phase 2 | 200 | $25K | $5M | $1.6M |
| 성장기 | 생태계 확대 | 500 | $30K | $15M | $3M |
| 성숙기 | 글로벌 진출 | 1,000+ | $50K | $50M+ | $5M |

---

## 🔒 9. 취약점 관리 & MITRE ATT&CK 통합

### GR Framework의 차별화: "WHERE" + "HOW"

기존 보안 프레임워크는 **"어떻게(HOW) 공격하는가"**에 집중합니다.
GR Framework는 **"어디에서(WHERE) 공격이 발생하는가"**를 제공하여, 실행 가능한 보안 전략을 만듭니다.

```
┌─────────────────────────────────────────────────────────────┐
│  MITRE ATT&CK (HOW - 공격 기법)                             │
│  - T1190: Exploit Public-Facing Application                │
│  - T1059: Command and Scripting Interpreter                │
│  - T1003: OS Credential Dumping                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ (매핑)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  GR Framework (WHERE - 인프라 위치)                         │
│  - Layer 2, Zone 1: 웹 서버 (T1190 적용)                   │
│  - Layer 7, Zone 2: 애플리케이션 (T1059 적용)               │
│  - Layer 5, Zone 3: 데이터베이스 (T1003 적용)               │
└──────────────────────┬──────────────────────────────────────┘
                       │ (실행 가능한 대응)
                       ▼
          ┌────────────────────────────────┐
          │  구체적 보안 조치                │
          │  - Layer 2: WAF 설치 (S3.4)    │
          │  - Layer 7: 입력 검증 (S1.6)   │
          │  - Layer 5: 암호화 (S2.2)      │
          └────────────────────────────────┘
```

### CVE 데이터베이스 통합

**목표**: 100,000+ CVE 레코드 수집 및 GR Framework 매핑

**PostgreSQL 스키마 확장**:
```sql
-- MITRE ATT&CK Technique 테이블
CREATE TABLE mitre_techniques (
    id UUID PRIMARY KEY,
    technique_id VARCHAR(20) UNIQUE,  -- T1190, T1059 등
    name VARCHAR(200),
    tactic VARCHAR(50),               -- Initial Access, Execution 등

    -- GR Framework 매핑
    common_layers JSONB,              -- ["L2", "L7"]
    common_zones JSONB,               -- ["Zone1", "Zone2"]
    affected_tags JSONB,              -- ["N2.1", "S3.4", "A1.5"]

    description TEXT,
    mitigation TEXT,
    detection TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

-- CVE-MITRE 매핑 테이블
CREATE TABLE cve_mitre_mapping (
    id UUID PRIMARY KEY,
    cve_id UUID REFERENCES cves(id),
    technique_id UUID REFERENCES mitre_techniques(id),

    -- 매핑 컨텍스트
    confidence DECIMAL(3,2),          -- 0.00 ~ 1.00
    exploit_chain_order INT,          -- 공격 체인 순서 (1, 2, 3...)

    created_at TIMESTAMP DEFAULT NOW()
);

-- CVE 테이블 GR 컨텍스트 추가
ALTER TABLE cves ADD COLUMN vulnerable_layers JSONB;
ALTER TABLE cves ADD COLUMN vulnerable_zones JSONB;
ALTER TABLE cves ADD COLUMN vulnerable_tags JSONB;
```

**예시 데이터**:
```sql
-- Log4Shell 취약점 예시
INSERT INTO cves (cve_id, description, severity, cvss_score,
                  vulnerable_layers, vulnerable_zones, vulnerable_tags)
VALUES (
    'CVE-2021-44228',
    'Apache Log4j2 Remote Code Execution',
    'Critical',
    10.0,
    '["L7", "L6"]'::jsonb,            -- Application & Runtime
    '["Zone2", "Zone3"]'::jsonb,      -- Application & Data
    '["T1.1", "T2.1", "A1.5"]'::jsonb -- Java, JVM, Backend API
);

-- MITRE 매핑
INSERT INTO cve_mitre_mapping (cve_id, technique_id, confidence, exploit_chain_order)
VALUES (
    (SELECT id FROM cves WHERE cve_id = 'CVE-2021-44228'),
    (SELECT id FROM mitre_techniques WHERE technique_id = 'T1190'),
    0.95,
    1  -- 첫 번째 공격 단계
),
(
    (SELECT id FROM cves WHERE cve_id = 'CVE-2021-44228'),
    (SELECT id FROM mitre_techniques WHERE technique_id = 'T1059.007'),
    0.90,
    2  -- 두 번째 공격 단계 (코드 실행)
);
```

### Attack Path 시뮬레이션 (Neo4j)

**Neo4j 그래프 모델**:
```cypher
// Zone 간 공격 경로 노드 생성
CREATE (ap:AttackPath {
  id: 'path-log4shell-001',
  name: 'Log4Shell Exploitation Chain',
  severity: 'Critical',

  // 공격 흐름
  start_zone: 'Zone1',
  end_zone: 'Zone3',

  // 사용된 CVE & MITRE 기법
  cves: ['CVE-2021-44228'],
  mitre_techniques: ['T1190', 'T1059.007', 'T1003'],

  // GR Framework 컨텍스트
  affected_layers: ['L2', 'L7', 'L5'],
  affected_products: ['Apache Log4j', 'Tomcat', 'PostgreSQL']
})

// Zone-to-Zone 공격 관계
MATCH (z1:Zone {code: 'Zone1'}), (z2:Zone {code: 'Zone2'})
CREATE (z1)-[:ATTACK_PATH {
  technique: 'T1190',
  cve: 'CVE-2021-44228',
  difficulty: 'Low',
  time_to_exploit: '5 minutes',
  detection_difficulty: 'Medium'
}]->(z2)

MATCH (z2:Zone {code: 'Zone2'}), (z3:Zone {code: 'Zone3'})
CREATE (z2)-[:ATTACK_PATH {
  technique: 'T1003',
  cve: null,
  difficulty: 'Medium',
  time_to_exploit: '30 minutes',
  detection_difficulty: 'High'
}]->(z3)
```

**공격 경로 쿼리**:
```cypher
// Zone 1에서 Zone 3까지의 모든 공격 경로 찾기
MATCH path = (z1:Zone {code: 'Zone1'})
             -[:ATTACK_PATH*1..5]->
             (z3:Zone {code: 'Zone3'})
WHERE ALL(r IN relationships(path) WHERE r.difficulty IN ['Low', 'Medium'])
RETURN path,
       [r IN relationships(path) | r.technique] AS techniques,
       [r IN relationships(path) | r.cve] AS cves,
       LENGTH(path) AS hop_count
ORDER BY hop_count
LIMIT 10
```

### AI 기반 CVE → MITRE 자동 매핑

**문제**: NVD에는 매일 수십 개의 CVE가 추가되지만, MITRE 매핑은 수작업

**해결**: LLM을 사용한 자동 매핑

```python
async def auto_map_cve_to_mitre(cve_id: str):
    """
    CVE 설명 → MITRE ATT&CK Technique 자동 매핑
    """
    # 1. NVD에서 CVE 설명 가져오기
    cve_data = await fetch_cve_from_nvd(cve_id)

    # 2. LLM으로 MITRE 기법 추론
    prompt = f"""
    CVE 설명을 분석하여 적용 가능한 MITRE ATT&CK 기법을 찾아주세요.

    CVE ID: {cve_data['cve_id']}
    설명: {cve_data['description']}
    영향받는 제품: {cve_data['affected_products']}

    MITRE ATT&CK 기법 ID와 신뢰도를 반환하세요.
    """

    llm_response = await llm.generate(prompt)
    # 출력 예시: [{"technique": "T1190", "confidence": 0.95}, ...]

    # 3. GR Framework 컨텍스트 추론
    gr_context = await infer_gr_context(cve_data)
    # {
    #   "layers": ["L2", "L7"],
    #   "zones": ["Zone1", "Zone2"],
    #   "tags": ["N2.1", "A1.5"]
    # }

    # 4. DB에 저장
    await save_cve_mitre_mapping(
        cve_id=cve_id,
        mitre_techniques=llm_response,
        gr_context=gr_context
    )

    return {
        "cve_id": cve_id,
        "mitre_techniques": llm_response,
        "gr_context": gr_context
    }
```

### 실전 활용: Attack Surface 분석

**사용자 질문**: "우리 인프라에서 Zone 1에서 Zone 3까지 도달 가능한 공격 경로는?"

**GR 시스템 응답**:
```yaml
Attack_Paths_Found: 3

Path_1:
  severity: Critical
  cves:
    - CVE-2021-44228 (Log4j RCE)
    - CVE-2023-12345 (SQL Injection)
  mitre_techniques:
    - T1190 (Exploit Public-Facing Application)
    - T1059.007 (Command Injection)
    - T1003 (Credential Dumping)

  attack_flow:
    step1:
      layer: L2
      zone: Zone1
      component: "Nginx (웹 서버)"
      vulnerability: "CVE-2021-44228"
      action: "Log4j exploit → RCE"

    step2:
      layer: L7
      zone: Zone2
      component: "Spring Boot API"
      vulnerability: null
      action: "내부 네트워크 스캔, DB 접근 시도"

    step3:
      layer: L5
      zone: Zone3
      component: "PostgreSQL"
      vulnerability: "CVE-2023-12345"
      action: "SQL Injection → 데이터 유출"

  mitigation:
    immediate:
      - Layer 2: "Nginx 업데이트 to 1.24+ (S5.1 Patch Management)"
      - Layer 7: "WAF 설정 강화 (S3.4)"
      - Layer 5: "DB 암호화 활성화 (S2.2)"

    long_term:
      - "Zone 1 → Zone 2: 네트워크 격리 강화"
      - "Zone 2 → Zone 3: DB 접근 제어 (Least Privilege)"
      - "모든 Layer: SIEM 모니터링 (M2.2)"

Estimated_Risk_Score: 9.2/10
Time_To_Exploit: 1-2 hours
Detection_Difficulty: Medium
```

---

## 🛡️ 10. 경쟁 우위 (Competitive Moat)

### 대체 불가능한 해자 (Moat)

**1. Pre-mapped 지식 베이스**
- 경쟁사는 "고객 데이터"를 분석하지만, 우리는 **"세상의 모든 제품"**을 미리 정의해뒀습니다
- 10,000개 제품 × 평균 3개 Archetype = 30,000개 지식 노드
- 이를 따라잡으려면 최소 2년 + 수백만 달러 필요

**2. 3D 좌표계 특허**
- Layer × Zone × Tag 조합은 GR만의 독창적 방법론
- 특허 출원 가능 (Method for Classifying IT Infrastructure Components Using 3D Coordinate System)

**3. AI의 Ground Truth**
- 2025년 AI 시대, 모든 보안 솔루션이 AI를 사용하지만 **"정확한 학습 데이터"**가 없습니다
- GR DB는 AI의 할루시네이션을 잡는 유일한 검증된 데이터셋이 될 것입니다

**4. Network Effect (네트워크 효과)**
- 더 많은 제품이 매핑될수록 → AI가 더 똑똑해짐
- 더 많은 고객이 사용할수록 → 피드백으로 데이터 품질 향상
- 선순환 구조

**5. API Economy**
- GR DB를 다른 보안 솔루션 업체에게 API로 판매 가능
- "Powered by GR Data" 라벨링으로 B2B2B 시장 진출

---

## ⚠️ 11. 리스크 및 대응 전략

### 주요 리스크

| 리스크 | 확률 | 영향도 | 대응 전략 |
|--------|------|--------|----------|
| **데이터 구축 지연** | 높음 | 치명적 | AI 파이프라인 조기 투자, 외주 활용 |
| **초기 자본 부족** | 중간 | 높음 | Phase 0로 PoC 먼저 → 투자 유치 |
| **AI 할루시네이션** | 중간 | 중간 | 전문가 검증 필수화, 신뢰도 점수 표시 |
| **경쟁사 모방** | 낮음 | 중간 | 특허 출원, First-Mover Advantage 극대화 |
| **데이터 최신성 유지 실패** | 중간 | 높음 | 자동 크롤링 + 커뮤니티 기여 모델 |

### 대응 전략

**Plan A (기본 계획)**:
- Phase 0 → PoC → 투자 유치 → Phase 1/2 진행

**Plan B (자본 부족 시)**:
- Phase 0만 완료 → 컨설팅 서비스로 먼저 수익 창출 → 데이터 구축 병행

**Plan C (시장 반응 부진 시)**:
- GR DB를 오픈소스화 → 커뮤니티 기여로 데이터 확충 → API 유료화로 수익

---

## 🎯 최종 결론

GR 생태계는 **"보안의 Google Maps"**를 만드는 프로젝트입니다.

- **지도 데이터 (GR DB)**: 전 세계 IT 제품의 좌표
- **내비게이션 엔진 (AI)**: 최적 경로와 위험 요소 계산
- **운전 대행 서비스 (제품들)**: 고객 문제 해결

2025년 11월, AI가 모든 산업을 재편하는 지금이야말로 **"AI가 공부할 교과서"**를 만드는 최적의 타이밍입니다.

우리는 제품을 만들지 않습니다.
**우리는 모든 보안 제품이 서 있을 토대를 만듭니다.**

---

**문서 끝**
