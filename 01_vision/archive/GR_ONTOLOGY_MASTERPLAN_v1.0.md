# GR Ontology 마스터플랜 v1.0

> **문서 버전**: 1.0
> **작성일**: 2025-01-28
> **상태**: 승인 대기

---

## 1. Executive Summary

### 1.1 프로젝트 정체성

```
GR = 인프라 맥락 기반 통합 보안 온톨로지

"보안은 인프라 위에서 일어난다"
모든 공격/방어/취약점에 WHERE(인프라 맥락)를 부여하여
AI가 맥락을 이해하고 추론할 수 있게 하는 지식 체계
```

### 1.2 핵심 가치 제안

| 기존 문제 | GR 솔루션 |
|-----------|-----------|
| MITRE ATT&CK: 공격 기법만, 인프라 맥락 없음 | 모든 기법에 WHERE 부여 |
| CVE: 취약점 나열, 관계 부족 | 인프라-취약점-공격-방어 연결 |
| 상용 LLM 의존 | 자체 LLM/RAG용 지식베이스 |
| 파편화된 보안 지식 | 통합 온톨로지로 연결 |

### 1.3 최종 산출물

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

## 2. 비전 및 목표

### 2.1 비전

> **"보안 지식의 표준 온톨로지를 구축하여, 인프라 맥락 기반의 AI 추론을 가능하게 한다"**

### 2.2 핵심 원칙

1. **인프라가 앵커(Anchor)**
   - 모든 보안 지식은 인프라 위에서 맥락을 가짐
   - 공격/방어/취약점 모두 "어디서(WHERE)"와 연결

2. **관계 중심 (Ontology)**
   - 단순 나열이 아닌 연결된 지식 그래프
   - AI가 관계를 통해 추론 가능

3. **자체 LLM 지원**
   - 오픈소스 LLM도 활용 가능한 수준의 지식 포함
   - 온톨로지(구조) + 설명(텍스트) 병행

4. **실용성 우선**
   - 학술적 완벽성보다 실무 적용 가능성
   - 진단 도구, 교육 시스템에 바로 사용 가능

### 2.3 성공 지표 (KPI)

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| 원자 수 | Phase 1: 500개, Phase 2: 2000개 | DB count |
| 관계 밀도 | 원자당 평균 5개 이상 관계 | 관계수/원자수 |
| RAG 정확도 | 일반 RAG 대비 30% 향상 | A/B 테스트 |
| 커버리지 | MITRE Top 50 기법 100% 매핑 | 매핑 완료율 |

---

## 3. 아키텍처

### 3.1 지식 구조

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

### 3.2 GR 좌표계 (3D Classification)

#### Layer (수직 - 9단계)
```
L0: External Services     - 외부 SaaS/API (통제 밖)
L1: Physical             - 물리 인프라 (데이터센터, 케이블링)
L2: Network              - 네트워크 (라우터, 방화벽, VPN)
L3: Compute              - 컴퓨팅 (클라우드, 하이퍼바이저)
L4: Platform             - 플랫폼 (CI/CD, IaC, 형상관리)
L5: Data                 - 데이터 (DB, 스토리지, 데이터웨어하우스)
L6: Runtime              - 런타임 (컨테이너, 메시지큐, 캐시)
L7: Application          - 애플리케이션 (웹/모바일 UI, API)
Cross: Observability     - 횡단 (모니터링, 보안, 테스팅)
```

#### Zone (수평 - 7단계)
```
Zone 0-A: Untrusted External  - 신뢰도 0% (인터넷, 공격자)
Zone 0-B: Trusted Partners    - 신뢰도 10% (인증된 외부 API)
Zone 1:   Perimeter           - 경계 (CDN, WAF, DDoS 방어)
Zone 2:   Service             - 서비스 (비즈니스 로직, API)
Zone 3:   Data                - 데이터 (DB, 암호화 필수)
Zone 4:   Management          - 관리 (인프라 관리, 운영)
Zone 5:   Endpoint            - 엔드포인트 (사용자 디바이스)
```

#### Functions (10개 도메인)
```
M: Monitoring    - 모니터링, 메트릭
N: Networking    - 네트워킹, 프로토콜
S: Security      - 보안, 인증, 암호화
A: Application   - 애플리케이션, 비즈니스 로직
D: Data          - 데이터 저장, 처리
R: Runtime       - 런타임, 실행 환경
C: Compute       - 컴퓨팅 리소스
P: Platform      - 플랫폼 서비스
T: Tech Stack    - 기술 스택
I: Integration   - 통합, API, 메시지
```

### 3.3 원자(Atom) 구조

```yaml
# 원자의 표준 구조
Atom:
  # ─── 정체성 ───
  id: "DOMAIN-TYPE-NAME-###"
  name: "정식 명칭"
  aliases: ["별칭들"]

  # ─── GR 분류 ───
  classification:
    domain: infrastructure | security | attack | defense | tool | concept
    type: component | technique | vulnerability | control | protocol
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
    is_a: []           # 상위 개념
    has_subtypes: []   # 하위 유형
    connects_to: []    # 연결 대상
    depends_on: []     # 의존성
    attacks: []        # 공격 대상 (공격 기법인 경우)
    defends: []        # 방어 대상 (방어 기법인 경우)
    exploits: []       # 악용 취약점
    mitigates: []      # 완화 대상

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

  # ─── 진단 힌트 ───
  diagnosis: {}

  # ─── 메타데이터 ───
  metadata:
    created_at: ""
    updated_at: ""
    version: ""
    confidence: 0.0-1.0
    sources: []
```

### 3.4 원자 분량 가이드라인

| 섹션 | 목적 | 권장 분량 |
|------|------|-----------|
| definition | LLM 기본 이해 | 500-800자 |
| core_concepts | 심화 지식 | 개념당 100-200자 |
| relations | 온톨로지 추론 | 5-15개 관계 |
| security | 보안 실무 | 500-1000자 |
| products | 실제 적용 | 200-400자 |
| diagnosis | 자동화 도구 | 구조화된 데이터 |

**총 원자 분량**: A4 2-4페이지 (YAML 포함)

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
```

---

## 5. 기존 표준 연동

### 5.1 MITRE ATT&CK 매핑

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

### 5.2 CVE/CWE 연동

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

### 5.3 MITRE D3FEND 연동

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

## 6. 실행 계획

### 6.1 Phase 1: Foundation (4주)

**목표**: 웹 애플리케이션 보안 도메인 완성

```
Week 1-2: 인프라 원자 생성
  ├── INFRA-APP-WAS-001 (WAS)
  ├── INFRA-APP-WEBSERVER-001 (Web Server)
  ├── INFRA-DATA-RDBMS-001 (RDBMS)
  ├── INFRA-NET-LB-001 (Load Balancer)
  ├── INFRA-NET-WAF-001 (WAF)
  ├── INFRA-APP-CACHE-001 (Cache)
  └── ... (총 30개)

Week 3: 공격/취약점 원자 생성
  ├── ATK-INJECT-SQL-001 (SQL Injection)
  ├── ATK-INJECT-XSS-001 (XSS)
  ├── ATK-INJECT-CMD-001 (Command Injection)
  ├── VUL-INJECT-* (관련 취약점)
  └── ... (총 30개)

Week 4: 방어 원자 + 관계 연결
  ├── DEF-PREVENT-* (예방 기법)
  ├── DEF-DETECT-* (탐지 기법)
  ├── 모든 원자 간 관계 연결
  └── RAG 테스트
```

**산출물**:
- 원자 100개
- 관계 500개 이상
- 웹 보안 RAG 프로토타입

### 6.2 Phase 2: Expansion (8주)

**목표**: 주요 도메인 확장 + MITRE 매핑

```
Week 1-4: 도메인 확장
  ├── 네트워크 보안 (30개)
  ├── 클라우드 보안 (30개)
  ├── 컨테이너/K8s 보안 (30개)
  └── 인증/인가 (30개)

Week 5-6: MITRE ATT&CK 매핑
  ├── Top 50 Techniques 완전 매핑
  ├── 각 기법에 GR 좌표 부여
  └── 인프라 연결

Week 7-8: D3FEND 연동 + 검증
  ├── 주요 방어 기법 매핑
  ├── 공격-방어 관계 완성
  └── RAG 성능 A/B 테스트
```

**산출물**:
- 원자 500개
- MITRE Top 50 완전 매핑
- RAG 성능 30% 향상 검증

### 6.3 Phase 3: Intelligence (12주)

**목표**: AI 서비스 구축

```
Week 1-4: 자체 LLM 파인튜닝
  ├── Llama/Mistral 기반 실험
  ├── GR 데이터로 파인튜닝
  └── 성능 벤치마크

Week 5-8: 서비스 프로토타입
  ├── 진단 도구 RAG 연동
  ├── 교육 시스템 프로토타입
  └── IaC 생성 실험

Week 9-12: 통합 및 최적화
  ├── 서비스 통합
  ├── 피드백 반영
  └── 프로덕션 준비
```

**산출물**:
- 자체 보안 LLM v1.0
- 서비스 프로토타입 3개
- 원자 2000개

---

## 7. 원자 생성 파이프라인

### 7.1 생성 프로세스

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

### 7.2 품질 기준

| 항목 | 기준 | 검증 방법 |
|------|------|-----------|
| 정의 완성도 | what/why/how 모두 작성 | 체크리스트 |
| 관계 밀도 | 최소 5개 관계 | 자동 검증 |
| GR 좌표 | Layer/Zone/Tags 모두 지정 | 자동 검증 |
| 보안 정보 | 취약점 또는 방어 최소 3개 | 체크리스트 |
| 출처 명시 | 최소 2개 출처 | 메타데이터 확인 |

### 7.3 자동화 도구

```python
# 원자 생성 보조 스크립트 (향후 개발)
class AtomGenerator:
    def generate_from_topic(topic, atom_type):
        """주제로부터 원자 초안 생성"""

    def validate_atom(atom):
        """원자 품질 검증"""

    def suggest_relations(atom):
        """관련 원자 추천"""

    def check_consistency(atom):
        """기존 원자와 일관성 확인"""
```

---

## 8. 기술 스택

### 8.1 저장소

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

### 8.2 AI/LLM

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

### 8.3 개발 환경

```yaml
Language: Python 3.11+
Framework: FastAPI (API), Pydantic (Schema)
Database: PostgreSQL, Neo4j (Phase 2)
Container: Docker, Kubernetes
CI/CD: GitHub Actions
Documentation: MkDocs
```

---

## 9. 위험 요소 및 대응

### 9.1 위험 식별

| 위험 | 영향 | 가능성 | 대응 |
|------|------|--------|------|
| 범위 과다 | 높음 | 높음 | 도메인별 단계적 확장 |
| 품질 저하 | 높음 | 중간 | 검증 프로세스 강화 |
| 유지보수 부담 | 중간 | 높음 | 자동화 도구 개발 |
| 기존 표준과 불일치 | 중간 | 중간 | MITRE/CVE 매핑 우선 |
| 기술 부채 | 중간 | 중간 | 정기 리팩토링 |

### 9.2 완화 전략

1. **범위 관리**: 도메인별 완성 후 확장 (웹 → 네트워크 → 클라우드)
2. **품질 게이트**: 원자당 체크리스트, 피어 리뷰
3. **자동화 투자**: 생성/검증 도구 조기 개발
4. **표준 준수**: MITRE ID 필수 매핑, UCO 호환성 고려

---

## 10. 거버넌스

### 10.1 문서 체계

```
GR_PROJECT/
├── constitution/          # 헌법 (기존)
├── schema/               # 스키마 정의 (기존)
├── atoms/                # 원자 저장소 (신규)
│   ├── infrastructure/
│   ├── attack/
│   ├── defense/
│   ├── vulnerability/
│   └── tool/
├── docs/                 # 문서
│   ├── masterplan.md     # 이 문서
│   ├── atom_guide.md     # 원자 작성 가이드
│   └── api_reference.md  # API 문서
└── tools/                # 도구
    ├── generator/        # 원자 생성기
    ├── validator/        # 검증기
    └── migrator/         # 마이그레이션
```

### 10.2 변경 관리

- **스키마 변경**: 헌법 수정 절차 적용
- **원자 추가**: PR 리뷰 후 머지
- **관계 수정**: 영향 분석 필수

### 10.3 버전 관리

```
원자 버전: 개별 version 필드
스키마 버전: schema/atom_schema.yaml 버전
문서 버전: 문서 헤더 버전
```

---

## 11. 다음 단계 (Immediate Actions)

### 11.1 이번 주 할 일

1. **원자 템플릿 확정**
   - WAS 원자를 표준 템플릿으로 채택
   - 필수/선택 필드 확정

2. **우선순위 목록 작성**
   - Phase 1 대상 원자 100개 목록화
   - 생성 순서 결정

3. **생성 도구 프로토타입**
   - Claude API 연동
   - 템플릿 기반 생성

### 11.2 이번 달 목표

- [ ] 인프라 원자 30개 완성
- [ ] 공격/취약점 원자 30개 완성
- [ ] 방어 원자 20개 완성
- [ ] 관계 연결 완료
- [ ] RAG 프로토타입 테스트

---

## 12. 승인

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| 프로젝트 오너 | | | |
| 기술 리드 | | | |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 1.0 | 2025-01-28 | 최초 작성 | Claude & Human |

