# GR Knowledge Atomization Constitution

> AI를 위한 지식 원자화 헌법
> Version: 2.2
> Effective Date: 2026-02-03
> Status: RATIFIED

---

## 서문 (Preamble)

```
본 문서는 GR Framework의 지식 데이터베이스(GR DB)를 구축함에 있어
모든 정보의 원자화(Atomization)에 적용되는 최상위 원칙을 정의한다.

이 헌법의 목적:
1. 모든 보안/IT 지식을 AI가 활용할 수 있는 형태로 구조화
2. 일관된 원자화 기준 제공
3. 도메인에 관계없이 적용 가능한 범용 프레임워크 수립
4. AI의 학습, 검색, 추론에 최적화된 지식 표현

이 헌법은 GR DB에 저장되는 모든 정보에 적용되며,
새로운 도메인 확장 시에도 이 원칙을 준수해야 한다.

스키마 정의: ../schema/atom_schema.yaml
관계 타입 정의: ../schema/relation_types.yaml
```

---

## 제1장: 기본 이념 (Fundamental Philosophy)

### 제1장 제1조: 대상은 AI다 (AI-First)

```
┌─────────────────────────────────────────────────────────────┐
│                    제1장 제1조: AI-First                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GR DB의 1차 소비자는 인간이 아닌 AI 시스템이다.            │
│                                                              │
│  이는 다음을 의미한다:                                      │
│                                                              │
│  1. 암묵적 지식 배제                                        │
│     - 인간에게 "당연한" 것도 명시적으로 기술               │
│     - 맥락 의존적 표현 금지                                 │
│     - 모든 전제조건을 명시                                  │
│                                                              │
│  2. 구조 우선                                               │
│     - 자연어 서술보다 관계와 속성으로 표현                  │
│     - 기계가 파싱 가능한 형태                               │
│     - 의미적 검색과 추론이 가능한 구조                      │
│                                                              │
│  3. 조합 가능성                                             │
│     - 단독으로도, 조합되어서도 의미 있는 단위              │
│     - AI가 새로운 답을 조합해낼 수 있는 블록               │
│                                                              │
│  인간 가독성은 2차 목표로, AI 활용성과 충돌 시             │
│  AI 활용성을 우선한다.                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 제1장 제2조: 지식은 그래프다 (Everything is Graph)

```
┌─────────────────────────────────────────────────────────────┐
│                제1장 제2조: Everything is Graph              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  모든 지식은 노드(Node)와 엣지(Edge)로 표현된다.           │
│                                                              │
│  원자(Atom) = 노드                                          │
│  - 하나의 개념, 기법, 도구, 취약점 등                       │
│  - 고유 식별자를 가짐                                       │
│  - 자기 완결적 정의를 포함                                  │
│                                                              │
│  관계(Relation) = 엣지                                      │
│  - 원자 간의 연결                                           │
│  - 타입이 있음 (is_a, causes, requires 등)                 │
│  - 방향성이 있음                                            │
│                                                              │
│  이 구조는:                                                 │
│  - 경로 탐색 (A에서 B로 가는 방법)                         │
│  - 관계 추론 (A가 B에 영향을 미치는가)                     │
│  - 패턴 발견 (유사한 구조 찾기)                            │
│  을 가능하게 한다.                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 제1장 제3조: 단일 진실 공급원 (Single Source of Truth)

```
┌─────────────────────────────────────────────────────────────┐
│             제1장 제3조: Single Source of Truth              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  하나의 개념은 하나의 원자로만 존재한다.                    │
│                                                              │
│  원칙:                                                       │
│  - 중복 원자 금지                                           │
│  - 동일 개념의 다른 표현은 alias로 처리                    │
│  - 다른 추상화 레벨은 별도 원자 + 관계로 연결              │
│                                                              │
│  예외:                                                       │
│  - 도메인별 특화 뷰는 확장(Extension)으로 처리             │
│  - 원본 원자를 참조하되, 추가 속성 부여 가능               │
│                                                              │
│  SSOT 실무 규칙:                                            │
│  - 중복 검사는 normalized_name 기준                         │
│  - 유사도 >= 0.85: 수동 검토 필요                          │
│  - 의미적 유사도 >= 0.92: 병합 또는 관계 연결 검토        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 제2장: 원자화 원칙 (Atomization Principles)

### 제2장 제1조: 자기 완결성 원칙 (Self-Containment)

모든 원자는 외부 맥락 없이 독립적으로 이해 가능해야 한다.

**위반 사례:**
```yaml
bad_example:
  name: "이 취약점"           # 무엇을 지칭하는가?
  description: "앞서 설명한 방법으로"  # 어디에?
```

**준수 사례:**
```yaml
good_example:
  id: "GR-SEC-VUL-00089"
  name: "SQL Injection"
  definition:
    what: "사용자 입력이 SQL 쿼리의 구문으로 해석되어 의도하지 않은 쿼리가 실행되는 취약점"
```

**검증 기준:**
- "이 원자만 읽고 이해할 수 있는가?"
- "외부 문서 참조 없이 의미가 명확한가?"
- "모든 참조가 ID로 명시되어 있는가?"

### 제2장 제2조: 다중 추상화 원칙 (Multi-Level Abstraction)

```
┌─────────────────────────────────────────────────────────────┐
│                    추상화 레벨 정의                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 4: 원리 (Principle)                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "신뢰할 수 없는 입력과 코드의 혼합은 위험하다"      │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↑ abstracts                        │
│  Level 3: 개념 (Concept)                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "Injection 취약점 패밀리"                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↑ is_a                             │
│  Level 2: 기법 (Technique)                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "UNION-based SQL Injection"                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↑ instance_of                      │
│  Level 1: 인스턴스 (Instance)                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "' UNION SELECT password FROM users--"               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Type과 Abstraction Level의 독립성:**
- `type` = "무엇의 범주인가" (vulnerability, technique, tool 등)
- `abstraction_level` = "얼마나 구체적인가" (1~4)
- 둘은 **독립적인 두 축**이다

예: vulnerability도 Level 3(개념)일 수 있고, Level 1(특정 CVE)일 수도 있다.

**Type 분류 원칙 (v2.0):**
```
┌─────────────────────────────────────────────────────────────┐
│                    Type 분류 체계 v2.0                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  type은 entity_class에 따라 구분됨:                         │
│                                                              │
│  [entity_class: true] 인프라 요소 (배포 가능)               │
│  • component         : 인프라/시스템 구성요소              │
│  • component_tool    : 배포되는 도구 (Burp Suite 등)       │
│  • component_control : 배포되는 보안 통제 (WAF 등)         │
│                                                              │
│  [entity_class: false] 지식 요소 (개념/기법)                │
│  • concept           : 개념, 사상, 전술                    │
│  • technique         : 공격/방어 기법                      │
│  • vulnerability     : 취약점                              │
│  • protocol          : 프로토콜, 포맷 (지식으로 취급)      │
│  • pattern           : 패턴, 시그니처                      │
│  • principle         : 원칙                                │
│  • tool_knowledge    : 도구에 관한 지식 (사용법 등)        │
│  • control_policy    : 보안 정책 (문서, 규정)              │
│                                                              │
│  세부 분류는 atom_tags로 표현:                              │
│                                                              │
│  예: application_server                                     │
│      → type: component, atom_tags: [APP, SERVER]           │
│                                                              │
│  예: attack_tactic                                          │
│      → type: concept, atom_tags: [ATK, TACTIC]             │
│                                                              │
│  예: cloud_platform                                         │
│      → type: component, atom_tags: [CLOUD, PLATFORM]       │
│                                                              │
│  이유:                                                      │
│  1. entity_class로 인프라/지식 명확히 구분                 │
│  2. atom_tags의 유연성 활용 (복합 분류 가능)               │
│  3. AI 학습 및 검색 일관성 유지                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 제2장 제3조: 명시적 관계 원칙 (Explicit Relations)

원자 간의 모든 관계는 타입이 정의되고 명시적으로 선언되어야 한다.

**관계 타입 정의:** `../schema/relation_types.yaml` 참조

**핵심 규칙:**
- **Canonical 관계만 저장**: is_a, causes, requires 등
- **Inverse는 저장 금지**: has_subtype, caused_by, prevented_by 등
- **Inverse는 쿼리 시 파생**: 그래프 엔진이 자동 계산

### 제2장 제4조: 메타데이터 필수 원칙 (Mandatory Metadata)

모든 원자는 아래 필수 메타데이터를 포함해야 한다:

| 카테고리 | 필수 필드 |
|----------|-----------|
| trust | source, confidence |
| temporal | created, modified, revision |
| security | sensitivity |
| ai | embedding_text, search_keywords |

**스키마 상세:** `../schema/atom_schema.yaml` 참조

### 제2장 제5조: 환경적 제약 원칙 (Environmental Constraints)

환경/맥락에 따라 달라지는 속성은 조건부로 표현해야 한다.

```yaml
constraints:
  - property: "effectiveness"
    base_value: 0.8
    conditions:
      - when:
          context_type: "version"
          condition: "mysql_version >= 8.0"
        then:
          value: 0.3
          reason: "MySQL 8.0에서 기본 보안 강화됨"
```

### 제2장 제6조: 확장 가능성 원칙 (Extensibility)

기본 스키마를 준수하면서 도메인별 확장이 가능해야 한다.

- 기본 스키마: `../schema/atom_schema.yaml` (불변)
- 도메인 확장: `../schema/extensions/{domain}.yaml`
- 확장은 `properties.{domain}` 필드에 추가

---

## 제3장: 스키마 (Schema)

### 제3장 제1조: 원자 스키마

원자의 구조는 `../schema/atom_schema.yaml`에 정의된다.

```yaml
# 핵심 구조 요약
atom:
  identity:     # id, name, normalized_name, aliases
  classification:  # domain, type, abstraction_level, gr_coordinates
  definition:   # what, why, how
  relations:    # structural, causal, conditional, temporal, applicability, epistemic
  properties:   # 도메인별 확장
  constraints:  # 환경적 제약
  metadata:     # trust, temporal, lineage, security, ai
```

### 제3장 제2조: 관계 타입

관계의 타입과 규칙은 `../schema/relation_types.yaml`에 정의된다.

**관계 카테고리:**
- structural: is_a, part_of, instance_of, abstracts
- causal: causes, enables, prevents
- conditional: requires, conflicts_with, alternative_to
- temporal: precedes, supersedes
- applicability: applies_to, effective_against
- epistemic: contradicts, disputes, refines

### 제3장 제3조: 도메인 확장

도메인별 확장 스키마는 `../schema/extensions/`에 정의된다.

현재 등록된 확장:
- `security.yaml`: 보안 도메인 (severity, cvss, cwe 등)

---

## 제4장: AI 활용 지침 (AI Utilization)

### 제4장 제1조: RAG 최적화

```yaml
chunking:
  principle: "하나의 원자 = 하나의 청크"
  rationale: "원자의 자기 완결성이 청크 경계와 일치"

embedding_text:
  format: "{name}은(는) {what}이다. {why} 때문에 중요하다."
  length: "50-200 단어"

search_keywords:
  include: ["정식 명칭", "약어", "동의어", "관련 기술 용어"]
  min_count: 5
```

### 제4장 제2조: Agent Reasoning 최적화

```yaml
conditional_reasoning:
  pattern: "A를 하려면 B가 필요하다"
  implementation: "requires 관계 활용"

alternative_reasoning:
  pattern: "A가 안 되면 B를 시도"
  implementation: "alternative_to 관계 활용"

chain_reasoning:
  pattern: "A 다음에 B, B 다음에 C"
  implementation: "precedes/enables 관계로 순서 파악"
```

### 제4장 제3조: 학습 데이터 생성

원자로부터 자동 생성 가능한 학습 데이터:
- Q&A 쌍: definition 필드 → 질문/답변
- 관계 트리플: (subject, relation, object)
- 추론 체인: premise + premise → conclusion

---

## 제5장: 거버넌스 (Governance)

### 제5장 제1조: 원자 생명주기

```
proposal → review → approved → [modified] → [deprecated]
  (draft)  (pending)  (active)    (active)    (deprecated)
```

- **ID 불변성**: 한 번 부여된 ID는 절대 변경 불가
- **폐기 처리**: 삭제 대신 deprecated + superseded_by 관계

### 제5장 제2조: 품질 기준

**필수 기준 (불충족 시 거부):**
- 스키마 100% 준수
- 중복 원자 없음 (normalized_name 기준)
- 자기 완결성 충족

**권장 기준 (품질 점수 반영):**
- 관계 수 >= 3
- 임베딩 텍스트 50-200 단어
- 검색 키워드 >= 5개

### 제5장 제3조: 버전 관리

```yaml
versioning:
  constitution: "2.0"  # 이 문서의 버전
  schema: "1.2"        # atom_schema.yaml 버전

  atom_revision:
    rule: "수정 시마다 revision +1"
    required: "lineage.transformations에 변경 기록"
```

### 제5장 제4조: ID 체계

```
형식: GR-{DOMAIN}-{TYPE}-{SEQUENCE}

도메인: SEC(보안), NET(네트워크), SYS(시스템), APP(애플리케이션),
       DAT(데이터), CLD(클라우드), IOT(IoT), AIM(AI/ML)

타입: CON(개념), TEC(기법), TOL(도구), VUL(취약점),
     CTL(통제), PRT(프로토콜), CMP(컴포넌트), PAT(패턴), PRI(원리)

예시: GR-SEC-VUL-00001, GR-NET-PRT-00042
```

---

## 제6장: 부칙 (Supplementary)

### 제6장 제1조: 헌법 개정

- 제안: 누구나 가능 (GitHub Issue/PR)
- 검토 기간: 최소 14일
- 승인: 주요 기여자 과반수 동의
- 소급 적용: 원칙적으로 안 함 (보안/무결성 예외)

### 제6장 제2조: 스키마 파일

| 파일 | 용도 |
|------|------|
| `../schema/atom_schema.yaml` | 원자 구조 정의 |
| `../schema/relation_types.yaml` | 관계 타입 정의 |
| `../schema/extensions/*.yaml` | 도메인별 확장 |

---

## 부록 A: 원자 작성 체크리스트

**필수:**
- [ ] ID 형식: GR-{DOMAIN}-{TYPE}-{SEQUENCE}
- [ ] normalized_name 생성됨
- [ ] abstraction_level과 type 조합 적절
- [ ] definition.what 50-500자
- [ ] relations에 canonical 관계만 사용 (inverse 금지)
- [ ] 레벨별 필수 관계 충족
- [ ] trust.source, confidence 설정
- [ ] security.sensitivity 설정
- [ ] ai.embedding_text 50-200단어
- [ ] ai.search_keywords 5개 이상

**금지:**
- [ ] 지시어('이', '그', '저')로 시작하는 설명 없음
- [ ] 외부 참조 없이 이해 가능
- [ ] inverse 관계 사용 안 함 (has_instance, prevented_by, follows 등)

---

## 부록 B: 예시 원자

```yaml
identity:
  id: "GR-SEC-VUL-00001"
  name: "SQL Injection"
  normalization:
    normalized_name: "sql injection"
    normalization_version: "1.0"
  aliases: ["SQLi", "SQL 인젝션"]

classification:
  domain: security
  type: vulnerability
  abstraction_level: 3
  gr_coordinates:
    layer: "L7"
    zone: "Z3"
    tags: ["A-WEB-API", "D-DB-SQL", "S-VUL-INJ"]

definition:
  what: |
    사용자가 제공한 입력이 SQL 쿼리의 데이터가 아닌
    실행 가능한 코드로 해석되어, 공격자가 의도하지 않은
    SQL 명령을 실행할 수 있게 되는 보안 취약점이다.
  why: |
    데이터베이스의 기밀 정보 유출, 인증 우회, 데이터 무결성
    파괴, 나아가 운영체제 명령 실행까지 이어질 수 있다.
  how: |
    애플리케이션이 사용자 입력을 검증/이스케이프 없이
    SQL 쿼리 문자열에 직접 연결하면 발생한다.

relations:
  structural:
    is_a: ["GR-SEC-CON-00001"]  # Injection
  causal:
    causes: ["GR-SEC-CON-00010", "GR-SEC-CON-00011"]
    enables: ["GR-SEC-TEC-00050", "GR-SEC-TEC-00051"]
  conditional:
    requires: ["GR-APP-CMP-00001", "GR-APP-CMP-00002"]
  applicability:
    applies_to: ["GR-DAT-TOL-00001", "GR-DAT-TOL-00002"]

properties:
  security:
    severity: critical
    cvss_base: 9.8
    cwe: "CWE-89"

metadata:
  trust:
    source: official
    confidence: 1.0
    verified:
      status: verified
      date: "2025-01-26"
  temporal:
    created: "2025-01-26"
    modified: "2025-01-26"
    revision: 1
  security:
    sensitivity: public
    weaponization_risk: medium
  ai:
    embedding_text: |
      SQL Injection(SQLi)은 웹 애플리케이션의 가장 위험한
      보안 취약점 중 하나로, 사용자 입력이 SQL 쿼리의
      실행 코드로 해석되어 공격자가 데이터베이스를
      무단으로 조회, 수정, 삭제할 수 있게 한다.
    search_keywords:
      - "SQL Injection"
      - "SQLi"
      - "SQL 인젝션"
      - "데이터베이스 해킹"
      - "쿼리 조작"
    related_queries:
      - "SQL Injection이란?"
      - "SQLi 방어 방법은?"
```

---

## 부록 C: 개정 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 2.1 | 2025-02-03 | Type 분류 원칙 명확화 (9개 고정, 세부는 Tags) |
| 2.0 | 2025-01-26 | 스키마 분리, 장-조 체계 정비 |
| 1.3 | 2025-01-26 | 내부 정합성 강화 |
| 1.2 | 2025-01-26 | Canonical 원칙 명확화 |
| 1.1 | 2025-01-26 | 메타데이터 확장 |
| 1.0 | 2025-01-26 | 최초 제정 |

---

## 서명

```
본 헌법은 GR Framework 프로젝트의 지식 원자화에 대한
최상위 규범으로서 제정되었으며, 모든 기여자와 시스템은
이를 준수해야 한다.

제정일: 2025-01-26
최종 개정: 2025-02-03
헌법 버전: 2.1
스키마 버전: 1.2

---
GR Framework Project
```
