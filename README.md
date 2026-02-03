# GR Ontology

> **보안 지식의 표준 온톨로지 - 인프라 맥락 기반 AI 추론 시스템**
> 
> **Schema Version**: 2.0 (2026-02-03)

---

## 프로젝트 소개

GR Ontology는 보안 지식을 **연결된 그래프(Knowledge Graph)**로 구조화하여, AI가 **"어디서(WHERE) + 어떻게(HOW)"** 보안 위협을 이해하고 추론할 수 있게 하는 **통합 보안 온톨로지**입니다.

### 핵심 가치

| 기존 문제 | GR 솔루션 |
|-----------|-----------|
| MITRE ATT&CK: 공격 기법만, 인프라 맥락 없음 | 모든 기법에 WHERE(인프라 위치) 부여 |
| CVE: 취약점 나열, 관계 부족 | 인프라-취약점-공격-방어 연결 |
| 파편화된 보안 지식 | 통합 온톨로지로 연결 |
| LLM 할루시네이션 | 사실 기반 지식 그래프로 보완 |

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     GR Ontology v2.0                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [원자 Atom]              [관계 Relation]              │
│   최소 지식 단위            원자 간 연결                 │
│   - 인프라 요소 ────────┐   - is_a, requires            │
│   - 공격 기법           │   - enables, prevents         │
│   - 방어 기법           │   - applies_to                │
│   - 취약점              │   - implements                │
│                         │                               │
│   entity_class ─────────┘   ※ related_to 금지          │
│   true/false 구분                                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    3D 좌표계 (인프라 요소만)             │
│                                                         │
│   Layer (수직)    ×    Zone (수평)    ×   Function      │
│   L0-L7, Cross         Z0A,Z0B,Z1-Z5      A2.1, S3.2... │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                      활용 (Applications)                 │
│                                                         │
│   RAG/LLM │ DAST │ Atlas │ Edu │ IaC │ Fine-tuning     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 디렉토리 구조

```
GR_Project_v3/
│
├── 00_docs/                     # 프로젝트 운영 문서
├── 01_vision/                   # 비전 & 마스터플랜
├── 02_framework/                # 3D 분류체계 상세
│   └── GR_DB/
│       ├── 01_차원1_Deployment_Layer/
│       ├── 02_차원2_Security_Zone/
│       └── 03_차원3_Function/
│
├── 03_ontology/                 # 온톨로지 정의
│   ├── constitution/            # 헌법 (원칙)
│   ├── schema/core/             # 핵심 스키마 (v2.0)
│   │   ├── atom_schema.yaml
│   │   └── relation_types.yaml
│   └── taxonomy/                # 분류 체계
│       ├── layers.yaml
│       ├── zones.yaml
│       └── atom_tags.yaml       # 원자 특성 태그
│
├── 04_knowledge_base/           # 지식 저장소 (원자들)
│   ├── concepts/
│   ├── infrastructure/
│   └── security/
│       ├── attacks/
│       ├── defenses/
│       └── vulnerabilities/
│
├── 05_engine/                   # Engine A/B 설계
├── 06_applications/             # 애플리케이션
│   ├── atlas/                   # 시각화 엔진
│   └── dast/
│
├── 07_references/               # 참조 자료
└── archive/                     # 철학/정책 문서
```

---

## 핵심 개념

### 원자 분류: entity_class

모든 원자는 **인프라 요소**와 **지식**으로 구분됩니다.

| entity_class | 설명 | type | 좌표 |
|:------------:|------|------|------|
| **true** | 배포 가능한 인프라 | component, component_tool, component_control | gr_coordinates (layer, zone, function) |
| **false** | 지식/개념/기법 | technique, vulnerability, concept, protocol, tool_knowledge, control_policy... | scope (target_layers, target_zones) |

### 인프라 원자 예시

```yaml
identity:
  id: "COMP-APP-WAS-001"
  name: "Web Application Server"

classification:
  domain: application
  type: component
  entity_class: true             # ✅ 인프라 요소
  gr_coordinates:
    layer: "L7"
    zone: "Z2"
    function: ["A2.1", "S2.2"]   # 계층적 Function 좌표
  atom_tags: ["WEB", "LINUX"]    # 평면적 특성 태그

relations:
  structural:
    is_a: ["CON-MIDDLEWARE-001"]
  implementation:
    implements: ["PROTO-HTTP-001"]
```

### 지식 원자 예시

```yaml
identity:
  id: "ATK-INJ-SQL-001"
  name: "SQL Injection"

classification:
  domain: security
  type: technique
  entity_class: false            # ✅ 지식 요소
  scope:                         # 인프라가 아니므로 scope 사용
    target_layers: ["L7"]
    target_zones: ["Z2", "Z3"]
  atom_tags: ["INJ", "WEB", "INITIAL"]

relations:
  structural:
    is_a: ["CON-INJECTION-001"]
  causal:
    enables: ["ATK-DATA-EXFIL-001"]
    requires: ["TECH-SQL-001"]
  applicability:
    applies_to: ["COMP-RDBMS-001"]
```

### 관계 (Relation)

| 카테고리 | 관계 | 의미 |
|----------|------|------|
| structural | is_a | 상위 개념 |
| structural | part_of | 구성 요소 |
| causal | enables | 가능하게 함 |
| causal | prevents | 방지함 |
| causal | requires | 필요로 함 |
| applicability | applies_to | 적용 대상 |
| implementation | implements | 프로토콜 구현 |

**⚠️ `related_to`는 금지됩니다** - 정밀한 관계 타입을 사용하세요.

---

## AI 활용

### 1. RAG (Retrieval-Augmented Generation)
```
질문 → 임베딩 검색 + atom_tags 필터 → 관계 그래프 탐색 → LLM 컨텍스트
```

### 2. Fine-tuning
```
온톨로지 → Q&A 데이터 변환 → LLM 학습 → 보안 전문 모델
```

### 3. Agent
```
LLM Agent → 온톨로지 API로 그래프 탐색 → 맥락 기반 추론
```

---

## 로드맵

- **Phase 1**: 온톨로지 구축 (웹 보안 도메인, 500개 원자)
- **Phase 2**: 확장 (네트워크, 클라우드, 2000개 원자)
- **Phase 3**: AI 연동 (RAG, Fine-tuning, 자체 LLM)

---

## 주요 참조 문서

| 문서 | 설명 |
|------|------|
| [Atom 작성 가이드](00_docs/GR_Atom_작성가이드.md) | 원자 작성 방법 |
| [스키마 정의](03_ontology/schema/core/atom_schema.yaml) | 원자 스키마 v2.0 |
| [관계 타입](03_ontology/schema/core/relation_types.yaml) | 허용된 관계 |
| [Atom Tags](03_ontology/taxonomy/atom_tags.yaml) | 원자 특성 태그 |
| [Atlas 명세](06_applications/atlas/GR_ATLAS_SPECIFICATION.md) | 시각화 엔진 |

---

## 라이선스

Proprietary - GOTROOT Security

---

> **"보안 지식을 연결하여, AI가 맥락을 이해하게 한다"**
