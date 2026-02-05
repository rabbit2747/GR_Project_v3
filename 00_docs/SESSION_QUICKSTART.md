# GR Ontology 세션 시작 가이드

> 새 세션에서 빠르게 컨텍스트를 파악하기 위한 문서

---

## 이 프로젝트는?

**IT 보안 지식을 원자(Atom) 단위로 쪼개서 저장하는 지식 그래프 시스템**

```
예: "SQL Injection"이라는 개념 → ATK-INJECT-SQL-001.yaml 파일로 저장
    - 정의, 관계, 속성, 메타데이터 포함
    - 다른 Atom들과 연결됨 (is_a, has_children 등 정밀 관계)
```

---

## 현재 상태 (2025-01-29 기준)

| 항목 | 값 |
|------|-----|
| 총 Atom 수 | **558개** |
| 참조 커버리지 | **65.9%** |
| 누락된 참조 | 279개 |

---

## 핵심 파일 위치

```
GR_Project_v2-main/
├── 00_docs/
│   ├── GR_Project_Status.md       ← 상세 현황
│   ├── GR_Atomization_Pipeline.md ← 파이프라인 설계
│   └── SESSION_QUICKSTART.md      ← 이 파일
├── 01_schema/
│   └── gr_atom_schema.yaml        ← Atom 스키마
└── 02_knowledge_base/             ← 모든 Atom 저장소
```

---

## 추상화 레벨 체계

| Level | 이름 | 예시 |
|-------|------|------|
| 4 | Principle | 최소 권한 원칙, 심층 방어 |
| 3 | Concept | Web Attack, Network Protocol |
| 2 | Technique | SQL Injection, AES 알고리즘 |
| 1 | Instance | Apache 서버, Mimikatz 도구 |

---

## 확장 철학

1. **100% 완성은 목표가 아님** - 지속적 확장이 목표
2. **재귀적 확장** - 원자화 중 발견된 용어도 원자화
3. **다중 소스** - MITRE, OWASP, CVE 등에서 동시 수집
4. **병렬 Agent** - 여러 Agent가 동시에 확장

---

## 다음 할 일 옵션

### A. 누락 참조 처리
279개 누락 참조 중 우선순위:
- TECH- (66개), ATK- (61개), DEF- (48개)

### B. 소스 기반 확장
정제된 소스에서 원자화:
1. MITRE ATT&CK 전체 기법
2. MITRE CWE 취약점
3. OWASP Top 10

### C. 파이프라인 자동화
`GR_Atomization_Pipeline.md` 참고하여 도구 개발

---

## 상세 문서

- **프로젝트 현황**: `00_docs/GR_Project_Status.md`
- **파이프라인 설계**: `00_docs/GR_Atomization_Pipeline.md`
