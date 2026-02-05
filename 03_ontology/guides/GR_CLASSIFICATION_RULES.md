# GR 원자 분류 규칙 (Classification Rules)
> Version: 1.0 | Date: 2026-02-05
> 
> 이 문서는 모든 원자의 분류를 **100% 결정론적**으로 수행하기 위한 규칙입니다.
> AI 에이전트가 이 규칙만으로 동일한 분류 결과를 도출할 수 있어야 합니다.

---

## 1. ID Prefix → 디렉토리 (1:1 매핑)

| Prefix | 디렉토리 | 설명 |
|--------|----------|------|
| `ATK-` | `attacks/` | 공격 기법 및 공격 카테고리 |
| `DEF-` | `defenses/` | 방어 정책, 절차, 방어 카테고리 |
| `VUL-` | `vulnerabilities/` | 취약점 |
| `TOOL-` | `tools/` | 도구 지식 |
| `INFRA-` | `infrastructure/` | 인프라 구성요소 (배포 가능한 실체) |
| `TECH-` | `technology/` | 기술 개념, 프로토콜 |
| `COMP-` | `compliance/` | 컴플라이언스 프레임워크, 규정 |

> ❌ `GR-SEC-*` prefix는 폐지. 기존 파일은 적절한 prefix로 재명명.

---

## 2. 핵심 규칙: Prefix → is_infrastructure

```
INFRA-*  → is_infrastructure: true
그 외 전부 → is_infrastructure: false
```

**이유**: 오직 `INFRA-*` prefix만 "배포 가능한 실체"를 나타냄.
DEF-*, TOOL-*, COMP-* 등은 모두 **지식**(knowledge)을 나타냄.

---

## 3. Type 결정 규칙

### 3.1 인프라 원자 (INFRA-* only)

| Type | 조건 | 예시 |
|------|------|------|
| `component` | 핵심 인프라 구성요소 | Server, Database, Cloud VM, Router |
| `component_tool` | 배포된 운영/보안 도구 | SIEM 인스턴스, EDR 에이전트, 스캐너 |
| `component_control` | 배포된 보안 통제 장치 | WAF 어플라이언스, IDS/IPS, Firewall |

**component vs component_tool vs component_control 판별:**
1. 주 목적이 보안 통제(차단/탐지/방지)인가? → `component_control`
2. 주 목적이 보안/운영 도구(분석/스캔/모니터링)인가? → `component_tool`
3. 그 외 인프라 → `component`

### 3.2 지식 원자 (INFRA-* 외 전부)

| Prefix | 기본 Type | 카테고리일 때 |
|--------|----------|-------------|
| `ATK-` | `technique` | `concept` |
| `DEF-` | `control_policy` | `concept` |
| `VUL-` | `vulnerability` | `concept` |
| `TOOL-` | `tool_knowledge` | `concept` |
| `COMP-` | `control_policy` | `concept` |
| `TECH-` | `concept` | — |

**추가 type:**
| Type | 조건 | 예시 |
|------|------|------|
| `principle` | 보안 원칙/철학 | Least Privilege, Zero Trust 원칙 |
| `pattern` | 시그니처, 페이로드, 핑거프린트 | SQLi payload, DBMS fingerprint |
| `protocol` | 통신 프로토콜/표준 | HTTP, TLS, OAuth, LDAP |

### 3.3 "카테고리" vs "구체적" 판별 규칙

```
카테고리(concept): 이름이 상위 분류를 나타내며, 구체적인 기법/취약점/절차가 아닌 것
  예: "Network Attack", "Email Defense", "Cloud Defense", "Collection (TA0009)"

구체적: 이름이 실행 가능한 특정 기법/취약점/절차를 나타내는 것
  예: "SQL Injection", "Rate Limiting", "NIST CSF", "Certificate Pinning"
```

**3가지 질문으로 판별:**
1. 이것을 "실행"하거나 "적용"할 수 있는가? → 구체적 (기본 type 사용)
2. 이것은 다른 원자들을 "포함"하는 상위 분류인가? → concept
3. 이것을 한 문장으로 구체적으로 설명할 수 있는가? → 구체적

---

## 4. 현재 오분류 파일 처리 규칙

### 4.1 DEF-* 파일 (87개)
- 현재: `type: control`, `is_infrastructure: true` (75개) ← **오류**
- 수정: `is_infrastructure: false`
  - 카테고리 → `type: concept`
  - 구체적 방어 정책/절차 → `type: control_policy`

### 4.2 COMP-* 파일 (17개)
- 현재: `type: control`, `is_infrastructure: true` (12개) ← **오류**
- 수정: `is_infrastructure: false`
  - 프레임워크/규정 → `type: control_policy`
  - 카테고리 → `type: concept`

### 4.3 TOOL-* 파일 (75개)
- 현재: `type: tool` ← **구 type**
- 수정:
  - 구체적 도구 → `type: tool_knowledge`
  - 카테고리 → `type: concept`

### 4.4 INFRA-* 오분류 (13개)
- `type: concept` (11개): 카테고리 원자 → `TECH-*`로 prefix 변경
- `type: protocol` (2개): LDAP, Kerberos → `TECH-*`로 prefix 변경
- `type: "component"` (1개): 따옴표 제거

### 4.5 GR-SEC-* 파일 (36개)
- type에 따라 적절한 prefix로 재명명:
  - technique(10) → `ATK-*`
  - vulnerability(2) → `VUL-*`
  - principle(6) → `TECH-*`
  - pattern(8) → `ATK-*` (공격 패턴)
  - concept(10) → `TECH-*`

---

## 5. atom_tags 배정 규칙

### 5.1 기본 원칙
- **최소 2개, 최대 10개**
- atom_tags.yaml 통제 어휘만 사용
- 카테고리 무관하게 조합 가능

### 5.2 필수 태그 선택 가이드

| 원자 특성 | 선택할 태그 카테고리 |
|----------|-------------------|
| 공격 기법 | attack_phase에서 1개+ |
| 취약점 | vulnerability_type에서 1개+ |
| 특정 기술 관련 | technology_stack에서 1개+ |
| 특정 OS/플랫폼 | platform에서 해당 것 |
| 특정 DB | dbms에서 해당 것 |
| 특정 프로토콜 | protocol에서 해당 것 |
| 방어 관련 | defense에서 관련 것 |

### 5.3 태그 배정 질문법
1. **"이것은 어떤 공격 단계와 관련되는가?"** → attack_phase 태그
2. **"이것은 어떤 기술 스택에서 사용되는가?"** → technology_stack 태그
3. **"이것은 어떤 플랫폼에 해당하는가?"** → platform 태그
4. **"이것은 어떤 취약점 유형과 관련되는가?"** → vulnerability_type 태그
5. **"이것은 어떤 방어 도구/방법과 관련되는가?"** → defense 태그

---

## 6. 서브디렉토리 규칙

각 prefix 디렉토리 내부의 서브디렉토리는 **주제별 그룹핑**:

```
attacks/
  ├── mitre/       # MITRE ATT&CK 매핑
  ├── web/         # 웹 공격
  ├── network/     # 네트워크 공격
  ├── cloud/       # 클라우드 공격
  └── windows/     # Windows 공격
```

서브디렉토리는 분류 규칙에 영향을 주지 않음 (정리용).

---

## 7. 검증 체크리스트

모든 원자 파일은 다음을 만족해야 함:

- [ ] ID prefix가 디렉토리와 일치
- [ ] `is_infrastructure`가 prefix 규칙에 따라 설정
- [ ] `type`이 3.1/3.2 규칙에 따라 설정
- [ ] `atom_tags`가 2개 이상
- [ ] `atom_tags`가 atom_tags.yaml에 정의된 값만 사용
- [ ] `function` 필드: `is_infrastructure: true`만 보유
- [ ] `type: control`, `type: tool` 구 type 없음 (분리 완료)
