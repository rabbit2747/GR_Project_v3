# GR Project v3 - Index

> v1의 상세 프레임워크 + v2의 정리된 지식베이스를 통합한 버전

---

## 프로젝트 구조

```
GR_Project_v3/
├── 00_docs/           # 프로젝트 운영 문서
├── 01_vision/         # 핵심 비전 & 마스터플랜 (v1 복원)
├── 02_framework/      # 3D 분류체계 상세 (v1 복원)
├── 03_ontology/       # 온톨로지 스키마 (v2)
├── 04_knowledge_base/ # 지식베이스 (v2)
├── 05_engine/         # Engine A/B 설계 (v1 복원)
├── 06_applications/   # 애플리케이션 (v2)
├── 07_references/     # 참조 자료 (v2)
└── archive/           # 철학/정책 문서 (v1 복원)
```

---

## 📁 폴더별 상세

### 00_docs/ - 프로젝트 운영 문서
- `GR_마스터플랜_비전.md` - 간소화된 비전 문서
- `GR_마스터플랜_아키텍처.md` - 간소화된 아키텍처 문서
- `GR_Project_Status.md` - 프로젝트 현황
- `SESSION_QUICKSTART.md` - 세션 시작 가이드

### 01_vision/ - 핵심 비전 & 마스터플랜 ⭐ 중요
| 문서 | 설명 | 핵심 내용 |
|:---|:---|:---|
| `GR 생태계 기획.md` | **좌표 기반 정책 체크리스트** | Policy Checklist Framework, 자동 추론 시스템 |
| `GR_생태계_마스터플랜_전문용_v2.2.md` | 기술 전문가용 마스터플랜 | 3D 분류체계, LLM 전략, CVE-MITRE 통합 |
| `GR_생태계_마스터플랜(일반용)v3.1.md` | 비즈니스용 마스터플랜 | 사업 비전, 수익 모델, 로드맵 |
| `GR_ONTOLOGY_MASTERPLAN_v1.0.md` | 온톨로지 마스터플랜 | 지식 구조화 전략, 관계 모델 |

### 02_framework/ - 3D 분류체계 ⭐⭐ 핵심
```
02_framework/
├── 00_인프라_구조도_분류체계_v2.0.md  # 3D 분류체계 핵심 문서 (62KB)
├── DB_아키텍처_설계서_v2.4.md          # DB 아키텍처 상세 (125KB)
└── GR_DB/
    ├── 00_분류체계_개요.md
    ├── 01_차원1_Deployment_Layer/     # 9개 Layer 상세 (L0-L7 + Cross)
    │   ├── Layer_0_External.md
    │   ├── Layer_1_Physical/
    │   ├── Layer_2_Network/
    │   ├── Layer_3_Compute/
    │   ├── Layer_4_Platform/
    │   ├── Layer_5_Data/
    │   ├── Layer_6_Runtime/
    │   ├── Layer_7_Application/
    │   └── CrossLayer_Management/
    ├── 02_차원2_Security_Zone/        # 7개 Zone 상세 (Z0A, Z0B, Z1-Z5)
    │   ├── Zone_0-A_Untrusted.md
    │   ├── Zone_0-B_Trusted_Partner.md
    │   ├── Zone_1_Perimeter.md
    │   ├── Zone_2_Application.md
    │   ├── Zone_3_Data.md
    │   ├── Zone_4_Management.md
    │   └── Zone_5_Endpoint.md
    ├── 03_차원3_Function/         # 10개 Function Domain (A-T)
    │   ├── Domain_A_Application.md
    │   ├── Domain_C_Compliance.md
    │   ├── Domain_D_Data.md
    │   ├── Domain_I_Interface.md
    │   ├── Domain_M_Monitoring.md
    │   ├── Domain_N_Networking.md
    │   ├── Domain_P_Platform.md
    │   ├── Domain_R_Resource.md
    │   ├── Domain_S_Security.md
    │   └── Domain_T_TechStack.md
    ├── 04_Database_Schema/            # ER 다이어그램, 배치 처리
    └── 05_Vulnerability_Catalog/      # 취약점 카탈로그 (CWE, OWASP, CVE)
```

### 03_ontology/ - 온톨로지 스키마
```
03_ontology/
├── constitution/
│   └── GR_KNOWLEDGE_ATOMIZATION_CONSTITUTION.md  # 지식 원자화 헌장
├── schema/
│   ├── core/
│   │   ├── atom_schema.yaml      # Atom 스키마 정의
│   │   └── relation_types.yaml   # 관계 유형 정의
│   └── extensions/
│       └── security.yaml         # 보안 확장 스키마
├── taxonomy/
│   ├── layers.yaml               # Layer 분류 (YAML)
│   ├── zones.yaml                # Zone 분류 (YAML)
│   └── atom_tags.yaml        # Atom Tags 분류 (원자 특성)
└── guides/
    └── PHASE1_ATOM_LIST.md       # Phase 1 Atom 목록
```

### 04_knowledge_base/ - 지식베이스
```
04_knowledge_base/
├── concepts/              # 개념 정의 (GR-SEC-CON-xxxxx)
├── infrastructure/        # 인프라 컴포넌트 (INFRA-xxx)
└── security/
    ├── attacks/           # 공격 기법
    │   ├── authentication/
    │   ├── injection/
    │   │   └── sqli/      # SQLi 상세 (8개 가이드 + payloads/techniques)
    │   ├── client-side/
    │   ├── server-side/
    │   └── network/
    ├── defenses/          # 방어 기법
    │   ├── detection/
    │   ├── prevention/
    │   └── response/
    ├── tools/             # 보안 도구
    └── vulnerabilities/   # 취약점 정의 (VUL-xxx)
```

### 05_engine/ - Engine A/B 설계
```
05_engine/
├── Engine_A/              # 지식 수집/원자화 엔진
│   ├── Engine A 기획.md
│   └── Engine A 종합 계획서_v1.0.md
└── Engine_B/              # 분류/온톨로지 엔진
    └── Engine B_분류엔진_기획서_v1.3.md
```

### 06_applications/ - 애플리케이션
```
06_applications/
├── atlas/                 # GR Atlas 시각화 엔진 ⭐ (v1에서 복원)
│   └── GR_ATLAS_SPECIFICATION.md  # Atlas 기능 명세
├── dast/                  # DAST 스캐너 관련
└── gr-engine-core/        # 엔진 코어
```

**GR Atlas**: IT 인프라를 지도처럼 시각화하는 기능
- 3D 좌표계 기반 인프라 맵
- 취약점/공격 흐름 하이라이트
- MITRE ATT&CK 연동 drill-down
- 자동화 진단, 컨설팅, 교육 등에 내장되는 공통 컴포넌트

### 07_references/ - 참조 자료
- `strix/` - Strix 참조 구현

### archive/philosophy/ - 철학/정책 문서
- `00_Framework_Philosophy.md` - 프레임워크 철학
- `02_Security_Policy_Checklist_Framework.md` - 보안 정책 체크리스트 상세
- `03_GR_IaC_Lab_System_Design.md` - IaC 랩 시스템 설계

---

## 🎯 핵심 문서 Quick Reference

### 사업/투자 프레젠테이션용
1. `01_vision/GR_생태계_마스터플랜(일반용)v3.1.md`
2. `01_vision/GR 생태계 기획.md` (정책 자동화 부분)

### 기술 심층 이해용
1. `02_framework/00_인프라_구조도_분류체계_v2.0.md`
2. `02_framework/DB_아키텍처_설계서_v2.4.md`
3. `01_vision/GR_생태계_마스터플랜_전문용_v2.2.md`

### 3D 좌표 시스템 상세
1. `02_framework/GR_DB/01_차원1_Deployment_Layer/` (Layer 상세)
2. `02_framework/GR_DB/02_차원2_Security_Zone/` (Zone 상세)
3. `02_framework/GR_DB/03_차원3_Function/` (Function 상세)

### 지식 원자화 체계
1. `03_ontology/constitution/GR_KNOWLEDGE_ATOMIZATION_CONSTITUTION.md`
2. `01_vision/GR_ONTOLOGY_MASTERPLAN_v1.0.md`

### Engine 설계
1. `05_engine/Engine_A/Engine A 종합 계획서_v1.0.md`
2. `05_engine/Engine_B/Engine B_분류엔진_기획서_v1.3.md`

---

## 📊 v1 vs v2 vs v3 비교

| 항목 | v1 | v2 | v3 |
|:---|:---:|:---:|:---:|
| 총 파일 수 | 236 | ~90 | **861** |
| 마스터플랜 상세도 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 3D 분류체계 상세 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Policy Checklist | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| YAML 스키마 | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 지식베이스 구조화 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Engine 설계 | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |

---

## 🚀 다음 단계 (TODO)

1. [ ] Knowledge Base 원자 파일 스키마 v2.0 마이그레이션
2. [ ] 통합 마스터플랜 문서 작성 (v1+v2 내용 병합)
3. [ ] Context Modifier 시스템 설계 추가
4. [ ] Instance DB 구조 설계
5. [ ] 3D 좌표 → 정책 자동 추론 API 설계

---

*Updated: 2026-02-03*
*Schema Version: 2.0*
