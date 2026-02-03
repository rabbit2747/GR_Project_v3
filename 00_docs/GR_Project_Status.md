# GR Ontology 프로젝트 현황

> 최종 수정: 2025-01-29

---

## 1. 프로젝트 개요

### 1.1 목적
IT 보안 지식을 체계적으로 원자화(Atomization)하여 구축하는 지식 그래프 시스템

### 1.2 핵심 개념
- **GR Atom**: 지식의 최소 단위 (YAML 형식)
- **GR Ontology**: Atom들의 연결로 구성된 지식 그래프
- **추상화 레벨**: Level 1(인스턴스) ~ Level 4(원칙)

### 1.3 디렉토리 구조
```
GR_Project_v2-main/
├── 00_docs/                    # 문서
├── 01_schema/                  # GR Atom 스키마 정의
├── 02_knowledge_base/          # 원자화된 지식 저장소
│   ├── concepts/               # 개념 atoms
│   │   ├── principles/         # Level 4 원칙
│   │   ├── tools/              # 도구 카테고리
│   │   ├── defenses/           # 방어 카테고리
│   │   ├── attacks/            # 공격 카테고리
│   │   ├── vulnerabilities/    # 취약점 카테고리
│   │   ├── technology/         # 기술 카테고리
│   │   ├── infrastructure/     # 인프라 카테고리
│   │   └── compliance/         # 컴플라이언스 카테고리
│   ├── infrastructure/         # 인프라 atoms
│   ├── security/               # 보안 atoms
│   │   ├── attacks/
│   │   ├── defenses/
│   │   ├── tools/
│   │   └── vulnerabilities/
│   └── technology/             # 기술 atoms
└── 03_tools/                   # 유틸리티 도구
```

---

## 2. 완료된 작업

### 2.1 스키마 설계 ✅
- GR Atom YAML 스키마 정의 완료
- 3D 분류 체계 (Layer × Zone × Tags) 확립
- 추상화 레벨 체계 (Level 1~4) 정의

### 2.2 초기 데이터 구축 ✅
- 초기 약 500개 atoms 생성 완료

### 2.3 확장 계획 수립 및 실행 ✅

#### Phase 1: Level 4 원칙 + Level 3 루트 개념 (15개)
| 카테고리 | 수량 | 상태 |
|----------|------|------|
| Level 4 Principles | 5개 | ✅ 완료 |
| Level 3 Root Concepts | 10개 | ✅ 완료 |

**생성된 Level 4 원칙:**
- GR-SEC-PRI-LEAST-PRIVILEGE-001
- GR-SEC-PRI-DEFENSE-DEPTH-001
- GR-SEC-PRI-ZERO-TRUST-001
- GR-SEC-PRI-FAIL-SECURE-001
- GR-SEC-PRI-SEPARATION-DUTIES-001

**생성된 Level 3 루트 개념:**
- GR-SEC-TOOL-001, GR-SEC-VULN-001, GR-SEC-DEF-001
- GR-SEC-ATK-001, GR-SEC-CONCEPT-001, GR-SEC-INFRA-001
- GR-SEC-COMP-001, GR-SEC-PROTOCOL-001, GR-SEC-CRYPTO-001
- GR-SEC-MALWARE-001

#### Phase 2: 도구 + 방어 카테고리 (27개)
| 카테고리 | 수량 | 상태 |
|----------|------|------|
| Tool Categories | 15개 | ✅ 완료 |
| Defense Categories | 12개 | ✅ 완료 |

#### Phase 3: 공격 + 취약점 + 기술 카테고리 (45개)
| 카테고리 | 수량 | 상태 |
|----------|------|------|
| Attack Categories | 20개 | ✅ 완료 |
| Vulnerability Categories | 10개 | ✅ 완료 |
| Technology Categories | 15개 | ✅ 완료 |

#### Phase 4: 인프라 + 컴플라이언스 카테고리 (17개)
| 카테고리 | 수량 | 상태 |
|----------|------|------|
| Infrastructure Categories | 12개 | ✅ 완료 |
| Compliance Categories | 5개 | ✅ 완료 |

### 2.4 현재 통계

| 지표 | 값 |
|------|-----|
| **총 Atom 수** | 558개 |
| **총 유효 참조** | 818개 |
| **존재하는 참조** | 539개 |
| **누락된 참조** | 279개 |
| **참조 커버리지** | 65.9% |

### 2.5 파이프라인 설계 ✅
- 원자화 파이프라인 9단계 설계 완료
- 소스 분류 체계 확립 (정제됨/반정제/정제필요)
- 신뢰성 높은 소스 목록 정리 완료

---

## 3. 진행 중인 작업

### 3.1 누락된 참조 현황

| 카테고리 | 누락 수 | 우선순위 |
|----------|---------|----------|
| TECH- (기술) | 66개 | 높음 |
| ATK- (공격) | 61개 | 높음 |
| DEF- (방어) | 48개 | 중간 |
| INFRA- (인프라) | 36개 | 중간 |
| VUL- (취약점) | 29개 | 중간 |
| COMP- (컴플라이언스) | 23개 | 낮음 |
| TOOL- (도구) | 13개 | 낮음 |
| GR- (루트) | 2개 | 높음 |
| MALWARE- (악성코드) | 1개 | 낮음 |

---

## 4. 향후 계획

### 4.1 단기 과제 (즉시)
- [ ] 누락된 279개 참조 중 우선순위 높은 것 처리
- [ ] 파이프라인 자동화 도구 개발

### 4.2 중기 과제 (파이프라인 구축)

#### 소스별 원자화 우선순위

**Phase 1: 뼈대 구축 (정제된 소스)**
- [ ] MITRE ATT&CK 전체 기법 원자화
- [ ] MITRE CWE 주요 취약점 원자화
- [ ] MITRE D3FEND 방어 기법 원자화
- [ ] OWASP Top 10 (Web, API, Mobile) 원자화

**Phase 2: 살 붙이기 (반정제 소스)**
- [ ] NVD/CVE 주요 취약점 원자화
- [ ] Metasploit 모듈 메타데이터 원자화
- [ ] Nuclei 템플릿 원자화
- [ ] CIS Benchmarks 컨트롤 원자화

**Phase 3: 확장 (정제 필요 소스)**
- [ ] 벤더 문서 (Microsoft, AWS 등)
- [ ] RFC 주요 프로토콜
- [ ] 학술 자료

### 4.3 장기 과제 (지속적 운영)
- 다중 Agent 병렬 처리 시스템 구축
- 소스 변경 감지 및 자동 업데이트
- 품질 검증 자동화

---

## 5. 핵심 원칙

### 5.1 확장 철학
- **100% 완성은 목표가 아님**: 지식은 계속 확장됨
- **재귀적 확장**: 원자화 중 발견된 용어도 원자화 대상
- **다중 소스 동시 수집**: 병렬 Agent로 속도 극대화
- **깊이와 넓이 동시 확장**: BOF → Registry → CPU 구조

### 5.2 품질 기준
- IT 용어는 모호하지 않음 - 모든 것이 명세로 정의되어 있음
- 신뢰성 높은 소스 우선 (MITRE, OWASP, NIST)
- 일관된 ID 체계와 스키마 준수

---

## 6. 참고 문서

| 문서 | 위치 | 설명 |
|------|------|------|
| 원자화 파이프라인 | `00_docs/GR_Atomization_Pipeline.md` | 데이터 수집/정제/적재 파이프라인 |
| GR Atom 스키마 | `01_schema/gr_atom_schema.yaml` | Atom YAML 스키마 정의 |
| 확장 계획 | `02_knowledge_base/expansion_plan_v1.yaml` | 초기 확장 계획 (완료) |

---

## 7. 세션 시작 가이드

새로운 세션에서 작업을 시작할 때:

### 7.1 현황 파악
```bash
# 현재 atom 수 확인
find 02_knowledge_base -name "*.yaml" | wc -l

# 커버리지 확인
# (참조 추출 및 비교 스크립트 실행)
```

### 7.2 작업 선택
1. **누락 참조 처리**: 279개 중 우선순위 높은 것부터
2. **소스 기반 확장**: MITRE ATT&CK 등 정제된 소스에서 추가
3. **파이프라인 개발**: 자동화 도구 구현

### 7.3 작업 시 참고
- 이 문서: `00_docs/GR_Project_Status.md`
- 파이프라인: `00_docs/GR_Atomization_Pipeline.md`
- 스키마: `01_schema/gr_atom_schema.yaml`

---

## 변경 이력

| 날짜 | 변경 내용 |
|------|-----------|
| 2025-01-29 | 최초 작성, Phase 1-4 완료, 파이프라인 설계 완료 |
