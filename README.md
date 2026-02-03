# GR Ontology

> **보안 지식의 표준 온톨로지 - 인프라 맥락 기반 AI 추론 시스템**

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
│                     GR Ontology                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [원자 Atom]              [관계 Relation]              │
│   최소 지식 단위            원자 간 연결                 │
│   - 인프라 요소             - is_a, requires            │
│   - 공격 기법               - enables, prevents         │
│   - 방어 기법               - applies_to                │
│   - 취약점                  - countered_by              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    3D 좌표계 (Classification)            │
│                                                         │
│   Layer (수직)    ×    Zone (수평)    ×    Tags         │
│   L0-L7, Cross         Zone0A-Zone5       M,N,S,A,D...  │
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
GR_Project_v2/
│
├── 01_ontology/                 # 온톨로지 정의
│   ├── constitution/            # 헌법 (원칙)
│   ├── schema/                  # 스키마 정의
│   │   ├── core/                # 핵심 스키마
│   │   └── extensions/          # 도메인별 확장
│   ├── taxonomy/                # 분류 체계 (Layer/Zone/Tags)
│   └── guides/                  # 작성 가이드
│
├── 02_knowledge_base/           # 지식 저장소 (원자들)
│   ├── infrastructure/          # 인프라 원자
│   ├── technology/              # 기술 지식 (SQL, 프로토콜 등)
│   ├── security/                # 보안 원자
│   │   ├── attacks/             # 공격 기법
│   │   ├── defenses/            # 방어 기법
│   │   ├── vulnerabilities/     # 취약점
│   │   └── tools/               # 도구
│   ├── concepts/                # 개념/원칙
│   └── mappings/                # 외부 표준 매핑 (MITRE, CWE)
│
├── 03_applications/             # 활용 애플리케이션
│   ├── dast/                    # 자동화 진단 도구
│   ├── atlas/                   # 시각화
│   ├── edu/                     # 교육 플랫폼
│   └── iac/                     # IaC 생성
│
├── 04_infrastructure/           # 기술 인프라
│   ├── database/                # DB 스키마
│   └── tools/                   # 자동화 도구
│
├── 05_docs/                     # 문서
│   ├── vision/                  # 비전/전략
│   ├── technical/               # 기술 문서
│   └── guides/                  # 사용 가이드
│
└── 99_references/               # 참고 자료
```

---

## 핵심 개념

### 원자 (Atom)

온톨로지의 최소 지식 단위입니다.

```yaml
identity:
  id: "ATK-SQLI-UNION-001"
  name: "UNION-based SQL Injection"

classification:
  domain: security
  type: attack_technique
  gr_coordinates:
    layer: "L7"
    zone: "Zone2"

definition:
  what: "UNION 연산자를 이용해..."
  why: "데이터베이스 정보 유출..."
  how: "1) 컬럼 수 파악 2) ..."

relations:
  requires: ["TECH-SQL-UNION-001"]
  enables: ["ATK-DATA-EXFIL-001"]
  countered_by: ["DEF-PARAMETERIZED-QUERY-001"]
```

### 관계 (Relation)

원자 간 연결로, AI 추론의 핵심입니다.

| 관계 | 의미 | 예시 |
|------|------|------|
| `is_a` | 상위 개념 | SQLi is_a Injection |
| `requires` | 필요 조건 | UNION SQLi requires SQL UNION 지식 |
| `enables` | 가능하게 함 | SQLi enables Data Exfiltration |
| `countered_by` | 방어 기법 | SQLi countered_by Parameterized Query |
| `applies_to` | 적용 대상 | SQLi applies_to RDBMS |

---

## AI 활용

### 1. RAG (Retrieval-Augmented Generation)
```
질문 → 관련 원자 검색 → 관계 따라 연관 원자 수집 → LLM에 컨텍스트 제공
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

## 관련 문서

| 문서 | 설명 |
|------|------|
| [온톨로지 헌법](01_ontology/constitution/) | 원자화 원칙 |
| [원자 작성 가이드](01_ontology/guides/) | 원자 작성 방법 |
| [마스터플랜](05_docs/vision/) | 프로젝트 비전 및 전략 |

---

## 라이선스

Proprietary - GOTROOT Security

---

> **"보안 지식을 연결하여, AI가 맥락을 이해하게 한다"**
