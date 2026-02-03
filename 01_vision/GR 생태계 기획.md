GR 생태계란 GR DB, GR Framework 을 기반으로 GR Edu, GR Consulting, GR solution, GR IaC 등 파생 아이템을 만들고 아이템을 통해 얻은 데이터와 노하우를 이용하여 다시 GR DB, GR Framework 또는 다른 아이템들을 업그레이드하는 선순환 생태계를 말한다.


1. GR DB 
 - GOTROOT의 지식의 보고로 보안 및 IT의 알렉산드리아 도서관을 목표로 한다.
 - 제일 핵심 기능은 GR Framework의 IT 인프라 분류 기준에 따른 IT 인프라 정보 저장과 각종 취약점들에 대한 정보 분류 및 저장이다.
 
 - 취약점 및 IT 인프라에 대한 지식 데이터베이스 
 - 취약점 및 IT 인프라에 대한 다양한 정보, 논문, 책, 뉴스 등 다양한 정보를 크롤링 한다. 
 - 수집한 정보를 머신러닝을 기반으로 하는 룰셋으로 원자화시킨다.
 - 원자화 된 정보는 머신러닝을 기반으로 하는 분류장치를 통해 분류되어 저장된다. 
 - 이때의 룰셋 및 분류 기준은 GR Framwork의 기준을 따른다. 
 
 - 단순 저장공간일 뿐 아니라 AI를 이용하여 보안관련 정보 검색 시 연관 된 정보들을 이용하여 기존 LLM의 정확도 보다 높은 정확도를 갖는 것을 목표로 한다. (이는 장기 프로젝트이며 GR DB의 부가적인 기능이자 목표. 본 기능은 GR Framework 에서 사용 될 정보들을 분류 저장하는 것)

 - 통합 보안 지식 데이터베이스를 구축하는 일은 대규모 작업이지만, 전례가 없는 것은 아니다. 
 - 본질적으로 GR DB는 인프라 컴포넌트, 소프트웨어, 취약점, 공격 기법, 방어 조치 등을 구조적으로 연결하는 **사이버 보안 지식 그래프(knowledge graph)**가 될 것이다. 
 - 이 데이터 상당수가 이미 공개되어 있거나 체계적으로 수집할 수 있다는 것이다. 
 예를 들어 아래와 같은 공개 저장소들이 있다. 
 ㄱ) 취약점: NVD의 CVE
 ㄴ) 약점 유형: CWE 
 ㄷ) 공격 패턴: MITRE, CAPEC
 ㄹ) 제품 식별자: CPE

 **데이터베이스 전략 (Multi-Database Architecture)**:

 **최종 목표: 3-Tier Database Design**
 - **관계형 DB** (PostgreSQL 15+): 원자화된 데이터, 트랜잭션, 데이터 무결성
 - **그래프 DB** (Neo4j): 복잡한 관계 탐색, CVE-MITRE 연결, 공격 경로 분석
 - **벡터 DB** (Pinecone/Weaviate/Milvus): 임베딩 저장, 유사도 검색, AI/ML 통합

 **Phase 1 (현재 구현)**:
 - **PostgreSQL 15+**: 관계형 데이터베이스 (34 tables, 완전히 원자화된 구조)
 - **pgvector extension**: PostgreSQL 내 벡터 검색 기능 (임시 솔루션)
 - **STIX 2.1 전략**: STIX 네이티브 저장 대신, 온디맨드/배치 export 전용 (NO native storage)

 **PostgreSQL 우선 채택 이유**:
   1. **데이터 무결성**: 관계형 제약조건(FK, CHECK, UNIQUE)으로 데이터 정합성 보장
   2. **트랜잭션 지원**: ACID 속성으로 배치 처리 신뢰성 확보
   3. **표준 SQL**: 복잡한 분석 쿼리와 집계 연산에 최적화
   4. **운영 안정성**: 백업, 복제, 모니터링 도구가 검증됨
   5. **확장성**: pgvector, PostGIS, Full-text search 등 풍부한 extension
   6. **팀 숙련도**: PostgreSQL 운영 경험과 생태계 이해도

 **Phase 2+ (향후 확장)**:
 - **Neo4j 그래프 DB 추가**:
   - N-depth 관계 쿼리 (예: "CVE → Tech Stack → Component → Layer → MITRE" 한 번에 탐색)
   - 공격 경로 분석 (Attack Path Analysis)
   - Cypher 쿼리로 복잡한 패턴 매칭
 - **별도 Vector DB 도입** (pgvector 대체):
   - 전문 벡터 검색 엔진 (Pinecone, Weaviate, Milvus 중 선택)
   - 대규모 임베딩 저장 및 유사도 검색 성능 최적화
   - AI/ML 모델과 직접 통합
 - **Multi-DB 동기화**: PostgreSQL을 Master로, Graph/Vector DB는 특화 용도로 활용

 - **Batch Processing Workflow (Phase 1 구현)**:
   - **단계 1: 크롤링** - 외부 소스(NVD, GitHub, MITRE)에서 데이터 수집 (스케줄 기반)
   - **단계 2: Staging** - 임시 테이블(staging_cve, staging_mitre_techniques)에 원시 데이터 저장
   - **단계 3: 검토** - 수동/자동 검증 프로세스 (status: pending → reviewed → approved/rejected)
   - **단계 4: 배치 등록** - 승인된 데이터를 프로덕션 DB로 예약 이전 (매일 02:00 AM)
   - **추적 테이블**: batch_processing_jobs, crawling_schedule로 전체 프로세스 모니터링

 - **CVE-MITRE 통합 전략**:
   - Tech Stack Domain (T)을 통한 자동 매핑: CVE → 영향받는 기술 스택 → MITRE Techniques
   - 매핑 테이블: cve_tech_stack_mapping, cve_component_mapping으로 관계 추적
   - 양방향 탐색: "이 CVE는 어떤 기법을 사용?" / "이 기법은 어떤 CVE와 연관?"

 - 지식 그래프는 환경이나 도메인의 "디지털 트윈(digital twin)" 역할을 하며, 관계형 DB의 JOIN과 인덱스를 통해 전체 연결 구조를 효율적으로 조회할 수 있다.
 - GR DB는 예를 들어 "DMZ 구역(Zone 1)에 위치한 컴포넌트들 중 치명적(Critical) 취약점이 존재하는 것만 찾아줘"와 같은 복잡한 질의를 SQL로 수행 가능하다.
 - 지속적인 업데이트는 Batch Processing Workflow를 통해 자동화된다. 크롤러가 정기적으로 NVD, MITRE 등에서 최신 데이터를 수집하고, 검증 후 프로덕션 DB에 반영한다.
 - 컨설팅 업무에서 수집하는 다크웹 크리덴셜 정보도 GR DB에 연결해, 특정 회사·제품과 연관 지을 수 있다(실제 위협 인텔 그래프들이 다크웹 데이터를 통합하는 방식과 유사).

- 데이터를 “원자 단위”로 저장한다는 설계는 매우 합리적이다. 의미 있는 최소 단위로 정보를 쪼개두면 재사용성과 조합 가능성이 최대화되기 때문이다. 이를 위해서는 보안 도메인에 대한 견고한 스키마·온톨로지 정의가 필수다. 즉, Software / Version / Vulnerability / Attack Technique / Mitigation / Configuration  / Setting 등의 엔터티 유형과, 그들 간의 관계를 명확히 모델링하는 것이다. 이는 초기에는 큰 작업이지만, 일단 구조가 잡히면 이후 데이터 추가는 비교적 루틴한 작업이 된다. “Apache(웹 서버)”와 “Apache(재단)” 같은 단어 중의성 문제는 CPE 같은 표준 식별자를 통해 해결할 수 있다.



2. GR Framework 
 - 정보보안 특히 모의해킹 분야에는 mitre attack framework가 존재함. 
 - 이는 해킹이 어떻게? 진행되는지에 대한 것을 구체화 시키며 해킹 전반의 흐름을 알 수 있게 해주는 framework.
 - 그러나 어디에서? 라는 물음에는 답하기가 어려움. 
 - GR Framework 는 IT 인프라을 3D(3차원) 분류 기준을 통해 입체적으로 구분하고 이에 취약점을 매핑하여 인프라의 각 구성요소에서 어떤 취약점이 발생하며 그 구성요소들은 IT 인프라에서 어디에 위치하는지를 알려줄 수 있음
 - GR Framework 는 이미 세계 표준으로 사용되어지는 Mitre attack과 서로 매핑하여 해킹과 보안에 있어서 더 정확하고 가시적인 흐름을 제공할 수 있음

 - 분류 기준에 대해서는 '00_인프라_구조도_분류체계_v2.0.md'에 기술되어 있음

 **핵심 철학: 좌표계 기반 자동 추론 시스템 (Coordinate-Based Inference System)**

 GR Framework의 혁신은 **기능 태그를 통한 자동 좌표 결정과 보안 정책 추론**에 있다.

 **1. 좌표계 형성 (2D Coordinate System)**
 ```
 수직축 (Layer): 기술 스택의 논리적 계층
   L0 (External) → L1 (Perimeter) → L2 (Application) → L3 (Data)
   → L4 (Management) → L5 (Endpoint) → L6 (Validation)
   → L7 (Coordination) → Cross-Layer

 수평축 (Zone): 신뢰 경계와 보안 수준
   Zone 0-A (0%) ← Zone 0-B (10%) ← Zone 1 (30%) ← Zone 2 (50%)
   ← Zone 3 (80%) ← Zone 4 (90%) → Zone 5 (20%)

 각 제품/컴포넌트 = (Layer, Zone) 좌표 + Function Tags
 ```

 **2. 자동 좌표 결정 (Automatic Coordinate Determination)**

 제품의 기능 분석 → Function Tags 부여 → Layer/Zone 좌표 자동 도출

 예시: PostgreSQL 신규 버전
 ```
 기능 분석:
   - "관계형 데이터베이스" → D1.1 (RDBMS)
   - "PostgreSQL 15.4" → T2.1 (PostgreSQL)
   - "데이터 저장/관리" → Layer 3 (Data)
   - "민감 데이터 처리" → Zone 3 (Data, 80% Trust)

 자동 결정된 좌표: (L3, Zone 3)
 자동 적용 정책: Layer 3 공통 정책 + Zone 3 공통 정책 + 경계 정책
 ```

 **3. 관계 추론 (Relationship Inference)**

 **(1) 같은 좌표 = 공통 보안 정책**
 ```
 좌표 (L3, Zone 3) 제품들:
   - PostgreSQL, MySQL, Oracle DB, MongoDB

 자동 적용되는 공통 보안 정책:
   ✅ 암호화: TLS 1.3 (S3.1)
   ✅ 접근 제어: RBAC (S2.1)
   ✅ 감사 로깅: 모든 쿼리 기록 (M3.1)
   ✅ 백업: 일일 증분 백업 (D5.1)
   ✅ 네트워크: VPN/PrivateLink 전용 (N5.1)
 ```

 **(2) 경계 간 = 경계 보안 정책**
 ```
 Layer 2 (Application) → Layer 3 (Data) 통신:
   ✅ API Gateway 필수 (N7.1)
   ✅ SQL Injection 방어 (S1.1)
   ✅ Input Validation
   ✅ Connection Pooling 제한

 Zone 2 (Application) → Zone 3 (Data) 통신:
   ✅ 네트워크 격리 (VPN/PrivateLink)
   ✅ DB 계정 분리 (read-only vs read-write)
   ✅ IP Whitelist
   ✅ Query Timeout 설정
 ```

 **4. 신규 제품 자동 매핑 (New Product Auto-Mapping)**

 새로운 제품이 등장하면 기존 프레임워크에 자동으로 통합:
 ```
 예시: CockroachDB (분산 관계형 DB) 신규 등장

 Step 1: 기능 분석
   - "분산 관계형 데이터베이스" → D1.1 (RDBMS)
   - "CockroachDB v23.1" → T2.X (신규 태그 생성)
   - "데이터 저장/관리" → Layer 3 (Data)
   - "민감 데이터 처리" → Zone 3 (Data)

 Step 2: 좌표 자동 결정
   좌표: (L3, Zone 3)

 Step 3: 보안 정책 자동 상속
   - PostgreSQL과 동일 좌표 → PostgreSQL 정책 상속
   - Layer 3 공통 정책 자동 적용
   - Zone 3 공통 정책 자동 적용
   - 경계 정책 자동 적용

 Step 4: 차이점 분석 및 추가 정책
   - CockroachDB 특화 기능 (분산 트랜잭션) → 추가 정책 정의
   - 새로운 CVE 발견 시 → T2.X 태그에 자동 매핑
 ```

 **5. 배포 위치 독립성 (Deployment-Agnostic)**

 **핵심 원칙**: 좌표는 기능과 신뢰 수준으로 결정되며, 배포 위치(온프레미스/클라우드)는 좌표에 영향을 주지 않는다.

 ```
 PostgreSQL on AWS RDS:
   좌표: (L3, Zone 3)
   Platform: P1.1 (AWS IaaS)
   보안 정책: Layer 3 + Zone 3 정책 (동일)

 PostgreSQL on-premise:
   좌표: (L3, Zone 3)
   Platform: P1.5 (On-Premise)
   보안 정책: Layer 3 + Zone 3 정책 (동일)

 PostgreSQL on Azure:
   좌표: (L3, Zone 3)
   Platform: P1.1 (Azure IaaS)
   보안 정책: Layer 3 + Zone 3 정책 (동일)

 → 좌표가 같으면 보안 정책도 같다!
 → Platform 태그는 운영 컨텍스트 (비용, 규제, 가용성) 정보
 ```

 **6. 프레임워크의 가치 (Framework Value)**

 - ✅ **자동화**: 기능 태그 → 좌표 → 보안 정책 (수동 설정 불필요)
 - ✅ **확장성**: 새 제품 등장 시 기존 정책 자동 재사용
 - ✅ **일관성**: 같은 좌표 = 같은 보안 기준 (인적 오류 방지)
 - ✅ **관계 추론**: 좌표 거리로 제품 간 보안 관계 파악
 - ✅ **배포 독립성**: 온프레미스/멀티 클라우드/하이브리드 모두 지원
 - ✅ **CVE 매핑**: Tech Stack Tag (T) 기반 자동 취약점 매핑
 - ✅ **MITRE 통합**: 공격 기법과 방어 전략 자동 연결

 **6-1. 정책 체크리스트 및 준수도 측정 (Policy Checklist & Compliance Framework)**

 **핵심 원칙**: 하나의 제품 = 하나의 좌표 + 정책 체크리스트

 **문제 인식**:
 - ❌ 하나의 제품에 여러 좌표 할당 → 정책 충돌 및 운영 복잡도 증가
 - ❌ 여러 기능을 가진 제품(예: Kubernetes)의 보안 요구사항 표현 어려움
 - ❌ 정책 구현 여부를 정량적으로 측정하기 어려움

 **해결책: Security Policy Checklist System**

 ```
 Component: Kubernetes v1.28
   Primary Coordinate: (Cross-Layer, Zone 4)    # 단일 좌표 (가장 중요한 역할 기준)
   Function Tags: [P3.2, R2.2, M7.3, S5.2, ...]  # 다중 기능 표현

   Policy Checklist (자동 생성):
     좌표 기반: 18 policies (Layer + Zone + Boundary)
     Function Tag 기반: 29 policies (각 태그별 정책)
     Total Required: 47 policies

   Compliance Measurement (준수도 측정):
     Implemented: 39/47 policies (82.9%)
     Grade: B (GOOD, MODERATE risk)
     Gaps: 8 policies (2 Critical, 3 High, 2 Medium, 1 Low)
 ```

 **체크리스트 자동 생성 프로세스**:
 ```
 1. 좌표 기반 정책 수집
    - Layer 공통 정책
    - Zone 공통 정책
    - Layer × Zone 경계 정책

 2. Function Tag 기반 정책 수집
    - 각 태그별 특화 정책
    - 태그 조합 정책

 3. 중복 제거 및 우선순위 정렬
    - CRITICAL > MANDATORY > RECOMMENDED > OPTIONAL

 4. 준수도 평가
    - 가중치 기반 점수 계산
    - 등급 부여 (A+, A, B, C, D, F)
    - Gap 식별 및 우선순위화
 ```

 **준수도 등급 체계**:
 - **A+ (95-100%)**: EXCELLENT, MINIMAL risk
 - **A (90-94%)**: VERY_GOOD, LOW risk
 - **B (80-89%)**: GOOD, MODERATE risk
 - **C (70-79%)**: ACCEPTABLE, MEDIUM_HIGH risk
 - **D (60-69%)**: POOR, HIGH risk
 - **F (<60%)**: CRITICAL, SEVERE risk

 **Gap Analysis (갭 분석)**:
 ```
 Gap 우선순위 = Risk Impact × 0.7 - Remediation Effort × 0.3

 Example Gap:
   Policy: P3.2-4 Runtime Security
   Status: NOT_IMPLEMENTED
   Risk Impact: CRITICAL
   Effort: HIGH (40 hours)
   Priority: #1 (highest)
   Recommendation: Deploy Falco or Sysdig
   Due Date: 2025-02-01
   Assigned To: Security Team
 ```

 **체크리스트 프레임워크의 가치**:
 - ✅ **정책 충돌 방지**: 단일 좌표 원칙으로 정책 일관성 유지
 - ✅ **다중 기능 지원**: Function Tags로 복잡한 제품의 역할 완전 표현
 - ✅ **정량적 측정**: 0-100% 준수도 점수로 보안 수준 명확화
 - ✅ **Gap 가시화**: 미구현 정책 식별 및 위험도 기반 우선순위화
 - ✅ **지속적 개선**: 주기적 재평가로 보안 성숙도 향상 추적
 - ✅ **규제 준수**: 감사 증명 자료 자동 생성

 **데이터베이스 스키마** (요약):
 - `policy_checklists`: 컴포넌트별 체크리스트 (1:1)
 - `checklist_policies`: 체크리스트별 정책 목록 (다대다)
 - `compliance_scores`: 시간대별 준수도 점수 추적
 - `compliance_gaps`: 미구현 정책 및 해결 계획

 **상세 문서**:
 - 📄 **02_Security_Policy_Checklist_Framework.md** (1,095 lines)
   - 체크리스트 생성 알고리즘 상세
   - Kubernetes, PostgreSQL 구체적 사례
   - 준수도 측정 공식 및 Gap 분석
   - 대시보드 및 리포팅 설계
   - 16주 구현 로드맵

 **7. MITRE ATT&CK과의 차별점**

 | 항목 | MITRE ATT&CK | GR Framework |
 |------|--------------|--------------|
 | 초점 | 공격 흐름 (How?) | 인프라 위치 (Where?) |
 | 구조 | Tactics → Techniques | Layer × Zone × Tags |
 | 질문 | "어떻게 공격하나?" | "어디를 공격하나?" |
 | 목적 | 공격 패턴 분류 | 방어 정책 자동화 |
 | 활용 | Red Team 공격 시뮬레이션 | Blue Team 방어 정책 설계 |
 | 통합 | GR Framework와 매핑 | MITRE와 상호 보완 |

 **GR Framework + MITRE ATT&CK = 완전한 보안 프레임워크**
 - MITRE: "Initial Access (TA0001) → Execution (TA0002) → ..."
 - GR Framework: "Zone 0-A (외부) → Zone 1 (경계) → Zone 2 (애플리케이션) → Zone 3 (데이터)"
 - 통합 결과: "어떤 공격 기법(MITRE)이 어느 위치(GR)에서 발생하며, 어떤 정책으로 막을 것인가"

 **Phase 1 완료 현황 (2025-11-20)**:
 - ✅ v2.0 아키텍처 완성: 9 Layers × 7 Zones × 10 Domains (280+ Tags)
 - ✅ 34개 문서 작성 완료 (Layer 9개, Zone 7개, Domain 10개, DB Schema 4개, 기타 4개)
 - ✅ Database Schema 설계: 34 tables (PostgreSQL 15+, 원자화된 관계형 구조)
 - ✅ CVE-MITRE ATT&CK 통합: Tech Stack Domain (T)을 통한 완전한 매핑
 - ✅ Batch Processing Workflow: 크롤링 → Staging → 검토 → 예약 등록

 **Phase 1 주요 설계 결정 사항 (Architecture Decisions)**:

 *1. Database Architecture: Multi-Database 전략 (3-Tier Design)*

 **최종 목표 (Multi-Database Architecture)**:
 ```
 PostgreSQL (관계형 DB) ← Master, Write 전용
   ↓ 동기화
 Neo4j (그래프 DB) ← Read, 관계 탐색 특화
   ↓ 동기화
 Pinecone/Weaviate/Milvus (벡터 DB) ← Read, 임베딩 검색 특화
 ```

 **각 DB의 역할**:
 1. **PostgreSQL (관계형 DB)**:
    - 원자화된 데이터 저장 (34 tables, Source of Truth)
    - ACID 트랜잭션으로 데이터 무결성 보장
    - 배치 처리 (Staging → Production) 중심
    - STIX 2.1 온디맨드/배치 export 전용 (NO native storage)

 2. **Neo4j (그래프 DB)**:
    - 복잡한 관계 탐색 (N-depth 쿼리)
    - CVE → Tech Stack → Component → Layer → MITRE 패턴 매칭
    - 공격 경로 분석 (Attack Path Analysis)
    - Cypher 쿼리로 시각화 지원 (GR Atlas 연동)

 3. **Vector DB (Pinecone/Weaviate/Milvus)**:
    - 취약점/기술 문서 임베딩 저장
    - 유사 CVE 검색 ("이 취약점과 비슷한 사례는?")
    - AI/ML 모델 직접 통합
    - RAG (Retrieval-Augmented Generation) 지원

 **Phase 1 구현 (현재)**:
 - PostgreSQL 15+ 관계형 DB (34 tables)
 - pgvector extension (임시 벡터 검색, Phase 2에서 전문 Vector DB로 대체)
 - Graph/Vector DB는 Phase 2+에서 추가

 **Phase 1에서 PostgreSQL 우선 선택 이유**:
 1. **프로젝트 초기 단계**: 데이터 구조 확정이 우선, 관계형 DB가 스키마 설계에 유리
 2. **데이터 무결성**: FK, CHECK, UNIQUE 제약조건으로 정합성 보장
 3. **배치 처리 적합**: Staging → Production 워크플로우에 트랜잭션 필수
 4. **운영 안정성**: 백업, 복제, 모니터링 도구가 성숙함
 5. **팀 숙련도**: PostgreSQL 운영 경험 풍부
 6. **단계적 확장 가능**: 구조 확정 후 Graph/Vector DB 추가하는 전략

 **Phase 2+ 확장 계획**:
 - Neo4j 추가: PostgreSQL에서 주기적으로 관계 데이터 동기화
 - Vector DB 추가: 문서 임베딩 생성 후 벡터 저장소로 이관
 - Multi-DB 동기화 파이프라인 구축 (CDC, ETL)

 **Trade-off 분석**:
 - ✅ 장점: 각 DB 강점 활용, 용도별 최적화, 확장성
 - ⚠️ 단점: 동기화 복잡도, 운영 비용 증가, 데이터 일관성 관리
 - 💡 전략: PostgreSQL을 Single Source of Truth로, 다른 DB는 Read 전용 Replica

 *2. 3D Classification Framework 확장: v1.0 → v2.0*

 **Layer 확장**: 8 Layers → 9 Layers
 - **추가**: Cross-Layer Management (레이어 간 관리 기능)
 - **이유**: Service Mesh, API Gateway 같은 레이어 간 조정 기능 분류 필요

 **Zone 확장**: 5 Zones → 7 Zones
 - **추가**: Zone 0-A (Untrusted External, 0% Trust), Zone 0-B (Trusted Partner, 10% Trust)
 - **이유**:
   - Zero Trust 아키텍처 지원 (외부도 세분화 필요)
   - 파트너사 연동 구간 명확히 분리
   - 신뢰 수준 세밀화 (0% / 10% / 20% / ...)

 **Function Tag 확장**: 210+ Tags → 280+ Tags (10 Domains)
 - **신규 Domain**:
   - **T (Tech Stack)**: PostgreSQL, React, Python 등 구체적 기술 스택 (CVE 매핑 핵심)
   - **I (Interface)**: REST API, gRPC, MQTT 등 통신 프로토콜
 - **확장 이유**:
   1. **CVE 매핑 정확도**: CVE는 특정 기술 스택(예: PostgreSQL 15.3)에 매핑되어야 함
   2. **MITRE 통합**: Tech Stack → Vulnerability → MITRE Technique 자동 연결
   3. **실무 활용성**: 실제 인프라는 구체적인 제품/버전으로 구성됨

 *3. Batch Processing Architecture: 크롤링 → 검증 → 등록*

 **Workflow 설계**:
 ```
 External Sources (NVD, GitHub, MITRE ATT&CK)
   ↓ 스케줄 기반 크롤링 (crawling_schedule)
 Staging Tables (staging_cve, staging_mitre_techniques)
   ↓ 검증 프로세스 (status: pending → reviewed → approved/rejected)
   ↓ 수동 검토 또는 자동 룰 기반
 Batch Processing (batch_processing_jobs)
   ↓ 예약 실행 (매일 02:00 AM)
 Production DB (cve, mitre_techniques, components)
   ↓ 자동 매핑 실행
 Mapping Tables (cve_tech_stack_mapping, cve_component_mapping)
 ```

 **구현 테이블** (4 tables):
 - `staging_cve`: 크롤링된 CVE 데이터 임시 저장 (JSONB raw_data)
 - `staging_mitre_techniques`: 크롤링된 MITRE 데이터 임시 저장
 - `batch_processing_jobs`: 배치 작업 실행 이력 추적
 - `crawling_schedule`: 크롤링 스케줄 관리 (cron 표현식)

 **설계 원칙**:
 1. **데이터 품질 우선**: 모든 데이터는 검증 후 프로덕션 DB 진입
 2. **이력 추적**: 모든 변경사항 로깅 (batch_processing_jobs)
 3. **롤백 가능**: Staging 데이터 보존으로 문제 발생 시 재처리 가능
 4. **자동화**: 스케줄 기반 무인 운영 (단, 중요 데이터는 수동 승인)

 *4. CVE-MITRE Integration: Tech Stack Domain 기반*

 **통합 전략**:
 ```
 CVE (예: CVE-2024-1234)
   ↓ 매핑 테이블: cve_tech_stack_mapping
 Tech Stack Tags (예: T2.1 PostgreSQL)
   ↓ 컴포넌트 연결: cve_component_mapping
 Components (예: Database Server)
   ↓ Layer/Zone 위치: layer_id, zone_id
 Infrastructure Context (Layer 3 - Data, Zone 3 - Data)
   ↓ 연관 관계: mitre_cve_mapping
 MITRE Techniques (예: T1190 - Exploit Public-Facing Application)
 ```

 **양방향 탐색 지원**:
 - Forward: CVE → 영향받는 기술 스택 → 취약한 컴포넌트 → MITRE 공격 기법
 - Backward: MITRE 기법 → 활용 가능한 CVE → 대상 기술 스택 → 방어 방법

 **자동 매핑 프로세스**:
 1. CVE 데이터에서 CPE (Common Platform Enumeration) 파싱
 2. CPE를 Tech Stack Tags와 매칭 (예: cpe:2.3:a:postgresql:postgresql:15.3 → T2.1)
 3. Tech Stack이 속한 Components 자동 식별
 4. MITRE Techniques와 CVE 관계 추론 (ML 기반 또는 룰 기반)

 **활용 시나리오**:
 - "PostgreSQL CVE가 발생하면 어떤 MITRE 기법으로 악용 가능?"
 - "TA0001 Initial Access를 위해 사용 가능한 최신 CVE는?"
 - "우리 인프라의 Layer 2 (Application)에 영향을 주는 CVE 목록"

 *5. 향후 고려사항 (Phase 2+)*

 **Multi-Database 완성: 3-Tier Architecture**

 **Graph Database (Neo4j) 추가**:
 - PostgreSQL을 Master DB로 유지 (Single Source of Truth)
 - Neo4j를 복잡한 관계 탐색용 Read Replica로 추가
 - CDC (Change Data Capture) 기반 실시간 동기화: PostgreSQL → Neo4j
 - 활용: CVE-MITRE 관계 시각화, 공격 경로 분석, GR Atlas 연동

 **Vector Database (Pinecone/Weaviate/Milvus) 추가**:
 - pgvector extension 대체 (전문 벡터 검색 엔진으로 마이그레이션)
 - 취약점 설명, MITRE 기법 문서를 임베딩으로 변환 후 저장
 - 유사도 검색: "이 CVE와 비슷한 취약점", "관련 공격 기법 추천"
 - RAG (Retrieval-Augmented Generation) 기반 AI 어시스턴트 구현
 - 활용: 지능형 검색, 추천 시스템, AI 챗봇

 **AI/ML 통합**:
 - CVE-MITRE 자동 매핑 정확도 향상 (현재: 룰 기반 → 향후: ML 기반)
 - 취약점 심각도 예측 모델 (XGBoost, Random Forest)
 - 공격 경로 자동 추론 (Graph Neural Network + Neo4j)
 - 벡터 임베딩 모델: OpenAI Embeddings, Sentence Transformers

 **Multi-DB 동기화 파이프라인**:
 - PostgreSQL (Write) → Kafka/Debezium → Neo4j + Vector DB (Read)
 - ETL 스케줄러: Apache Airflow
 - 데이터 일관성 보장: Event Sourcing, CQRS 패턴

 **STIX 2.1 Export**:
 - 온디맨드 export API 구현 (PostgreSQL → STIX JSON)
 - 배치 export 스케줄러 (주간, 월간 전체 데이터)
 - 외부 시스템 연동용 (SIEM, Threat Intelligence Platform)

 - GR Framework 의 확장 기능 중 하나는 GR Atlas.
 
 * GR Atlas
 	- GR Atlas 는 분류 기준을 통해 분류 된 인프라를 기업들의 네트워크 구성도 처럼 시각화 해서 보여주는 IT 인프라 및 보안의 다이나믹 인터렉티브 MAP. 
 	- 단순히 IT 인프라에 관한 MAP이 아닌 MItre Attack 과 취약점들을 맵핑함.
 	- 시각화 된 map의 인프라 구성요소를 누르면 해당 구성요소에 설치될 수 있는 상세 구성요소(제품, 소프트웨어 등)을 리스트업 함
 	- 상세 구성요소를 클릭하면 해당 구성요소에서 발생할 수 있는 Tatic(mitre 기반) 을 보여주며 이를 통한 technique(mitre 기반)을 리스트업 하며 mitre에서는 여기서 끝나지만 GR Atlas 는 technique에 사용되는 각종 기술에 대한 것들도 모두 리스트업 함. 
 	- GR DB에 저장된 원자화 된 취약점에 대한 정보들을 조합하여 GR Atlas를 통해 구성요소에서 발생하는 기술들에 대한 세세한 정보를 확인할 수 있음

	- 또한 기업의 네트워크 구조를 재현하고 각종 해킹 사건이나 CVE, 개별 기술들을 검색한다면 map 에 하이라이트 방식(각종 색상을 이용)으로 흐름도를 보여주며 기업의 보안 설정 들을 대입한다면 현재 보안에 취약한 구성요소들을 보여줄 수 있음 
 	- 이를 통해 사용자들은 IT 인프라와 보안에 대해 훨씬 쉬운 접근이 가능함 
 	

 - GR Framework 의 3D 분류 기준(7layer, 5zone, tag)을 기반으로 GR Atlas를 통해 사용자들에게 각 zone과 layer 별 보안이 잘 되어있는지를 확인시켜줄 수 있음 


3. GR IaC
 - 기존의 IaC(terraform 과 ansible을 예로 들자면)의 경웅 자동화로 인프라를 만들 수 있지만 취약점을 재현하는데 있어서 어려움이 있음.
 - LLM 을 통해서 취약한 환경에대해 명세서를 만들고 IaC로 환경을 구성한다 해도 llm의 신뢰도가 완벽하지 않기 때문에 실제 구현이 안될 경우가 있을 수 있음 
 - 이는 상품화에 있어서 커다란 걸림돌임 
 - 그러나 GR DB와 GR Framework 는 취약점에 대한 상세한 정보와 인프라 구조에 대한 틀을 잡고 있기 때문에 이 둘의 매핑을 이용하면 IaC를 통한 취약점 재현의 신뢰성을 향상 시킬 수 있음 
 - 한 취약점을 구현한다고 하면 먼저 GR DB를 통해 그 취약점이 어떤 인프라 요소에서 발생하는지 확인을 하고 그 인프라 요소가 어떤 zone에 있고 어떤 layer 에 위치하는지 그리고 이 구성요소를 사용하는 일반적인 인프라 구성은 어떤것들이 있는지 확인하고 그중 하나를 선택하여 환경을 구성하고 취약점을 재현하기 위해서 잘못된 로직, 보안에 취약한 함수사용, 잘못된 설정 등을 GR DB를 통해 확인하여 ansible playbook을 만들어서 확실히 취약한 환경을 구성하게 할 수 있음 
 - 이 것을 실제 환경 재현에도 사용할 수 있고 도커환경을 구성하는데 사용할 수도 있음

4. GR Edu
 - GR Edu 는 보안교육 플랫폼으로 인터넷 강의, 실습환경, 자격증, 대회 등을 제공
 - 각 강의는 커리큘럼 / 섹션 / 렉처 로 구성 됨 
 - 렉처는 보안에 대한 이론, 기술에 대한 정보를 담고있는 실제 강의(동영상 ot 텍스트)
 - 섹션은 렉처를 특정 테마를 맞게 조합한 것(ex. 권한 상승 섹션 : 리눅스 권한상승 렉처 + 윈도우 권한상승 렉처) 
 - 커리큘럼은 섹션들을 특정 테마에 맞게 모아둔 것으로 커리큘럼 안에 커리큘럼이 있을 수도 있음
 ex) beginer 커리큘럼 : 웹 해킹 커리큘럼 + 모바일 해킹 커리큘럼
 ex) 웹 해킹 커리큘럼 : web 개론 섹션 + sqli 섹션 + 인증 우회 섹션 

 - 실습 환경은 다른 플랫폼들과 차별성 있이 GR IaC 를 이용하여 훨씬 다양하고 최신 해킹 사건들에 대한 실습을 진행할 수 있음
 - 또한 GR IaC를 통해서 시간이 많이 들여야하는 인프라 환경 구성을 간편하게 한 뒤 이를 이용하여 정기적으로 wargame 대회를 열 수 있음 
 
 - 교육에 있어서는 GR Atlas와 mitre attack의 매핑을 이용하여 전체 해킹의 흐름과 보안에 대한 보다 쉬운 이해 시킬 수 있음
 - 또한 이를 이용하여 학습자 개개인의 실력 측정과 결과에 따른 커리큘럼 추천 까지 가능함 


5. GR solution 
 - GR 생태계를 이용하여 다양한 솔루션 제작이 가능함 
 - GR framework를 이용한 zerotrust 솔루션
 - GR framework를 이용한 자동화 진단 툴 
 - 그 외도 여러가지 사업화 아이템에 응용이 가능함 


6. GR 컨설팅 
 - 기존 모의해킹, 침투테스트, 취약점 진단에 GR atlas 를 이용하여 정확히 고객 보안 시스템의 약점과 보완점을 가시적으로 보여줄 수 있음
 - 보안 담당자 뿐만 아니라 기업 임원, 개발자, 관리자에게도 시각적으로 문제점을 보여줄 수 있음
 - redteam playbook으로 활용 가능함
 - GR atlas를 이용하여 컨설턴트 들의 개인 역량 개발에도 도움을 줄 수 있음(부족한 부분 체크 및 교육 가능)




GR 생태계는 이러한 시스템으로 운영되며 GR DB와 GR Framework 의 계속적인 업그레이드를 통해 응용 비지니스와의 선순환 구조를 만들어 발전가능 생태계를 만드는 것이 특징임 
