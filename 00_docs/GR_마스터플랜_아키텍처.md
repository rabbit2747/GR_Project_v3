# GR 생태계 마스터플랜: 아키텍처 & 기술

> **기술 상세 문서 - 3D 프레임워크, 데이터 아키텍처, LLM 전략**
> **최종 수정**: 2025-01-29

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | GR 생태계 마스터플랜: 아키텍처 & 기술 |
| **목적** | GR 생태계의 기술 아키텍처, 3D 프레임워크, 데이터 모델 정의 |
| **대상 독자** | 기술 의사결정자, 개발자, 시스템 아키텍트 |
| **관련 문서** | `GR_마스터플랜_비전.md` (비전 & 전략) |

---

## 1. 지식 구조 개요

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
│   모든 요소는 GR 좌표 (Layer/Zone/Tags)를 가짐             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 3차원 프레임워크 (3D Framework)

AI가 인프라를 입체적으로 인식하기 위한 3축 좌표계입니다.

### 2.1 축 1: Deployment Layer (기술 스택의 수직적 깊이)

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

### 2.2 축 2: Security Zone (보안 신뢰의 수평적 경계)

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

### 2.3 축 3: Function & Attributes (기능과 속성)

**AI의 관점**: "이 녀석의 정체는 무엇이고, 어떤 DNA를 가졌는가?"

#### 기능 도메인 (8개)

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

#### 속성 도메인 (2개)

| 코드 | 도메인명 (한글) | 도메인명 (영문) | 태그 개수 | 설명 | 목적 |
|------|----------------|----------------|----------|------|------|
| **T** | 기술 스택 | Tech Stack | 30개 | 언어, 런타임, OS | **CVE 영향도 분석** |
| **I** | 인터페이스 | Interface | 25개 | 프로토콜, 데이터 포맷 | **통신 흐름 분석** |

**Domain T (Tech Stack) 예시**:
- `T1.1` Java, `T1.2` Python, `T1.3` Go, `T1.4` Node.js
- `T2.1` JVM, `T2.2` .NET CLR
- `T3.1` Linux, `T3.2` Windows

**Domain I (Interface) 예시**:
- `I1.1` HTTP/1.1, `I1.2` HTTP/2, `I1.3` gRPC, `I1.4` WebSocket
- `I2.1` JSON, `I2.2` XML, `I2.3` Protobuf

**총 10개 도메인, 약 280개 태그**

---

## 3. 원자(Atom) 구조

### 3.1 표준 구조

```yaml
Atom:
  # ─── 정체성 ───
  id: "DOMAIN-TYPE-NAME-###"
  name: "정식 명칭"
  aliases: ["별칭들"]

  # ─── GR 분류 ───
  classification:
    domain: infrastructure | security | attack | defense | tool | concept
    type: component | technique | vulnerability | control | protocol
    abstraction_level: 1-4  # 인스턴스~원칙
    gr_coordinates:
      layer: "L0-L7 | Cross"
      zone: "Z0A-Z5"
      tags: ["M", "N", "S", ...]

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
      has_children: []   # 하위 유형
      related_to: []     # 관련 개념
    causal:
      requires: []       # 필요 조건
      enables: []        # 가능하게 하는 것
      prevents: []       # 방지하는 것
    security:
      targets: []        # 공격 대상 (공격 기법인 경우)
      mitigates: []      # 완화 대상 (방어 기법인 경우)
      vulnerable_to: []  # 취약한 공격/취약점

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
      revision: 1
```

### 3.2 원자 분량 가이드라인

| 섹션 | 목적 | 권장 분량 |
|------|------|-----------|
| definition | LLM 기본 이해 | 500-800자 |
| core_concepts | 심화 지식 | 개념당 100-200자 |
| relations | 온톨로지 추론 | 5-15개 관계 |
| security | 보안 실무 | 500-1000자 |
| products | 실제 적용 | 200-400자 |

**총 원자 분량**: A4 2-4페이지 (YAML 포함)

### 3.3 추상화 레벨 체계

| Level | 이름 | 설명 | 예시 |
|-------|------|------|------|
| **4** | Principle (원칙) | 보편적 진리, 설계 원칙 | 최소 권한, 심층 방어, Zero Trust |
| **3** | Concept (개념) | 추상적 분류, 카테고리 | Injection, 미들웨어, 인증 우회 |
| **2** | Technique (기법) | 구체적 방법, 유형 | UNION-based SQLi, WAS, RDBMS |
| **1** | Instance (인스턴스) | 특정 제품, 사례 | Apache Tomcat 9.0, CVE-2021-44228 |

---

## 4. 원자 유형별 ID 체계

### 4.1 ID 프리픽스

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

TECH-*      기술
  TECH-PROTOCOL-* 프로토콜
  TECH-CRYPTO-*   암호화
  TECH-LANG-*     프로그래밍 언어

COMP-*      컴플라이언스
  COMP-FRAMEWORK-* 프레임워크 (ISO, NIST)
  COMP-GOVERNANCE-* 거버넌스
  COMP-AUDIT-*    감사
```

---

## 5. 데이터 아키텍처

### 5.1 하이브리드 데이터베이스 전략

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
    - Vendor          - Tag → Product   - 스펙 벡터
    - CPE             - Attack Path     - 유사도 검색
    - Version         - Dependency
    - License         - CVE Impact
```

### 5.2 DB별 역할 분담

| Database | 역할 | 저장 데이터 | 핵심 쿼리 | 선택 이유 |
|----------|------|------------|----------|----------|
| **PostgreSQL** | Master (불변 팩트) | Product 정보, Vendor, CPE, License, Version | `SELECT * WHERE vendor='Apache'` | ACID 보장, 트랜잭션 지원 |
| **Neo4j** | Relationships (관계) | Zone↔Layer 연결, Tag 조합, 공격 경로, 의존성 | `MATCH (a)-[*]->(b) RETURN path` | 관계 탐색 최적화, 그래프 쿼리 |
| **Pinecone** | Semantics (의미) | 제품 설명 임베딩, 스펙 벡터 | `similarity_search(vector, k=10)` | 고속 벡터 검색, RAG 최적화 |

### 5.3 데이터 흐름 예시

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

---

## 6. 데이터 모델: 2-Tier 원자화 전략

### 6.1 Tier 1: Product Master (불변의 팩트)

**저장 위치**: PostgreSQL
**성격**: 변하지 않는 제품의 객관적 정보

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

### 6.2 Tier 2: Component Archetypes (가능한 역할들)

**저장 위치**: Neo4j (Graph) + Pinecone (Vector)
**성격**: 하나의 제품이 가질 수 있는 **모든 변신 형태**

**핵심 개념**:
- 하나의 제품(Product)은 여러 개의 Archetype(원형)을 가질 수 있습니다
- Archetype = "이 제품을 이렇게 쓰면, 이런 좌표에 배치되고, 이런 보안 정책이 적용된다"

**Neo4j 그래프 모델**:
```
(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:Cache)
                                     ├─ layer: "L5"
                                     ├─ zone: "Z2"
                                     ├─ primary_tag: "D3.1"
                                     └─ use_case: "Application cache"

(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:SessionStore)
                                     ├─ layer: "L5"
                                     ├─ zone: "Z3"
                                     ├─ primary_tag: "D3.3"
                                     └─ use_case: "Session management"

(Product:Redis) -[:HAS_ARCHETYPE]-> (Archetype:MessageBroker)
                                     ├─ layer: "L6"
                                     ├─ zone: "Z2"
                                     ├─ primary_tag: "R3.2"
                                     └─ use_case: "Pub/Sub messaging"
```

---

## 7. 기존 표준 연동

### 7.1 MITRE ATT&CK 매핑

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

### 7.2 CVE/CWE 연동

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
      entry: "Zone0-A"
      target: "Z3"
```

### 7.3 MITRE D3FEND 연동

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

## 8. CVE-MITRE 통합 스키마

### 8.1 PostgreSQL 스키마 확장

```sql
-- MITRE ATT&CK Technique 테이블
CREATE TABLE mitre_techniques (
    id UUID PRIMARY KEY,
    technique_id VARCHAR(20) UNIQUE,  -- T1190, T1059 등
    name VARCHAR(200),
    tactic VARCHAR(50),               -- Initial Access, Execution 등

    -- GR Framework 매핑
    common_layers JSONB,              -- ["L2", "L7"]
    common_zones JSONB,               -- ["Z1", "Z2"]
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

### 8.2 Attack Path 시뮬레이션 (Neo4j)

```cypher
// Zone 간 공격 경로 쿼리
MATCH path = (z1:Zone {code: 'Z1'})
             -[:ATTACK_PATH*1..5]->
             (z3:Zone {code: 'Z3'})
WHERE ALL(r IN relationships(path) WHERE r.difficulty IN ['Low', 'Medium'])
RETURN path,
       [r IN relationships(path) | r.technique] AS techniques,
       [r IN relationships(path) | r.cve] AS cves,
       LENGTH(path) AS hop_count
ORDER BY hop_count
LIMIT 10
```

---

## 9. LLM 전략

### 9.1 Phase별 LLM 사용 구분

#### 구축 단계 (Phase 0-2)

**목표**: 10,000개 제품 × 평균 3개 Archetype = 30,000개 지식 노드 구축

**LLM 사용**:
- 외부 LLM API 자유 사용 (GPT-4, Claude, Gemini)
- 제품 설명 → Archetype 추론
- 공식 문서 → Function 추출
- CVE 설명 → MITRE Technique 매핑

**데이터 안전성**:
- 모두 공개 데이터 (제품 정보, CVE, 공식 문서)
- 기밀 정보 없음 → 외부 API 사용 안전

#### 고객 배포 단계 (Phase 2+)

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
```

**20% AI-Assisted (복잡한 추론 필요)**:
```python
# Case 2: 공격 경로 시뮬레이션 (AI 필요)
def analyze_attack_path(infrastructure_data: dict):
    """
    옵션 1: On-premise LLM (기밀 유지)
    - 고객사 내부 서버에 설치
    - Llama 3.1 (8B), Mistral (7B) 등

    옵션 2: 익명화 후 외부 LLM
    - 민감 정보 마스킹 (IP, 도메인, 계정명)
    - 구조만 외부 LLM에 전송
    """
```

### 9.2 비용 비교

| 방식 | 응답 속도 | 정확도 | 월 비용 | 기밀 안전성 |
|------|----------|--------|---------|------------|
| Direct Query (80%) | 50-100ms | 100% | $0 | 완벽 |
| On-premise LLM (20%) | 500ms-2s | 95% | $0 (운영비만) | 완벽 |
| External LLM (20%) | 1-3s | 98% | $100-$500 | 익명화 필요 |

### 9.3 자체 AI 모델 개발 계획 (Phase 3)

- GR DB 기반 Fine-tuned LLM 개발
- 30,000+ Archetype 데이터로 학습
- 보안 도메인 특화 모델

---

## 10. 원자 생성 파이프라인

### 10.1 생성 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│                  Atom Generation Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 주제 선정                                               │
│      └── 우선순위 목록에서 선택                              │
│                                                             │
│   2. 자료 수집                                               │
│      ├── 공식 문서                                          │
│      ├── MITRE/CWE/CVE                                      │
│      ├── OWASP                                              │
│      └── 실무 경험                                          │
│                                                             │
│   3. 초안 생성 (Claude/GPT 활용)                            │
│      ├── 표준 템플릿 적용                                    │
│      ├── 정의/개념/관계 생성                                 │
│      └── 보안 프로파일 작성                                  │
│                                                             │
│   4. 검증 및 보완                                            │
│      ├── 기술적 정확성 검토                                  │
│      ├── 관계 일관성 확인                                    │
│      └── 누락 정보 보완                                      │
│                                                             │
│   5. 등록 및 연결                                            │
│      ├── DB 저장                                            │
│      ├── 기존 원자와 관계 연결                              │
│      └── 인덱스 업데이트                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 품질 기준

| 항목 | 기준 | 검증 방법 |
|------|------|-----------|
| 정의 완성도 | what/why 모두 작성 | 체크리스트 |
| 관계 밀도 | 최소 5개 관계 | 자동 검증 |
| GR 좌표 | Layer/Zone/Tags 모두 지정 | 자동 검증 |
| 출처 명시 | 최소 2개 출처 | 메타데이터 확인 |

---

## 11. 기술 스택

### 11.1 저장소

```yaml
Phase 1 (현재):
  Primary: PostgreSQL 15+
    - 원자 저장
    - 관계 저장
    - 전문 검색 (pg_trgm)

  Secondary: YAML 파일
    - 버전 관리
    - 리뷰 프로세스

Phase 2 (확장):
  Graph DB: Neo4j
    - 복잡한 관계 쿼리
    - 경로 탐색
    - 시각화

  Vector DB: Pinecone / pgvector
    - 임베딩 저장
    - 유사도 검색
    - RAG 지원
```

### 11.2 AI/LLM

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

### 11.3 개발 환경

```yaml
Language: Python 3.11+
Framework: FastAPI (API), Pydantic (Schema)
Database: PostgreSQL, Neo4j (Phase 2)
Container: Docker, Kubernetes
CI/CD: GitHub Actions
Documentation: MkDocs
```

---

## 12. 인프라 비용 (초기)

| 항목 | 서비스 | 규모 | 월 비용 | 연 비용 |
|------|--------|------|---------|---------|
| PostgreSQL | AWS RDS | db.t3.medium | $50 | $600 |
| Neo4j | AuraDB Professional | 1 instance | $200 | $2,400 |
| Pinecone | Serverless (100k vectors) | 1 pod | $70 | $840 |
| OpenAI API | Embedding (ada-002) | 100개 제품 | $100 | $1,200 |
| **합계** | - | - | **$420** | **$5,040** |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-01-29 | 3개 마스터플랜 문서 통합 (아키텍처 파트) |

---

**문서 끝**
