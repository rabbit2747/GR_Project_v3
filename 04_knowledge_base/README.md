# SQLi Knowledge Base

> MVP DAST SQLi 프로젝트의 원자화된 지식 저장소

## 구조

```
01_Knowledge_Base/
├── atoms/
│   ├── principles/      # Level 4: 원리
│   ├── concepts/        # Level 3: 개념
│   ├── techniques/      # Level 2: 기법
│   └── instances/       # Level 1: 인스턴스
│       ├── payloads/    # 구체적 페이로드
│       ├── bypasses/    # 우회 패턴
│       └── fingerprints/# 핑거프린트
│
├── id_registry.yaml     # ID 할당 레지스트리
└── README.md
```

## 스키마

- 헌법: `../../constitution/GR_KNOWLEDGE_ATOMIZATION_CONSTITUTION.md`
- 원자 스키마: `../../schema/atom_schema.yaml`
- 관계 타입: `../../schema/relation_types.yaml`

## ID 체계

```
GR-SEC-{TYPE}-{SEQUENCE}

TYPE:
  PRI = principle (원리)
  CON = concept (개념)
  TEC = technique (기법)
  VUL = vulnerability (취약점)
  PAT = pattern (패턴)
```

## 소스 문서

`../00_Foundation/` 디렉토리의 문서들을 기반으로 원자화:
- 01_SQLi_Complete_Guide.md
- 02_Bypass_Techniques.md
- 03~05_DBMS_*.md
- 06_NoSQL_Injection.md
- 07_Advanced_Exploitation.md
- 08_Lateral_Movement.md
