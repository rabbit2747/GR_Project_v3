# GR Atom 작성 가이드

> **목적**: 일관된 품질의 원자를 작성하기 위한 표준 가이드
> **버전**: 2.0
> **최종 수정**: 2026-02-03
> 
> **참조 스키마**: `03_ontology/schema/core/atom_schema.yaml` v2.0

---

## 1. 원자(Atom)란?

```
원자 = GR 온톨로지의 최소 지식 단위

특징:
  - 하나의 명확한 개념/기법/요소를 표현
  - 다른 원자와 관계로 연결됨
  - AI 추론에 활용 가능한 구조화된 정보
  - 자체 LLM 학습에 사용 가능한 설명 포함
```

**예시:**
- "SQL Injection" → 하나의 원자
- "UNION-based SQLi" → 또 하나의 원자 (SQL Injection의 하위 기법)
- "Prepared Statement" → 또 하나의 원자 (방어 기법)

---

## 2. 핵심 개념: is_infrastructure

### 2.1 정의

모든 원자는 **인프라 요소**인지 **지식**인지 구분해야 합니다.

```yaml
is_infrastructure: true   # 인프라 요소 (배포/설치 가능)
is_infrastructure: false  # 지식 (개념/기법/취약점)
```

### 2.2 판정 기준 (4가지 질문)

| 질문 | Yes면 is_infrastructure: true |
|------|:-----------------------------:|
| 네트워크 주소를 가질 수 있는가? | ✅ |
| 프로세스로 실행될 수 있는가? | ✅ |
| 물리적 형태가 있을 수 있는가? | ✅ |
| 시스템 자원을 소비하는가? | ✅ |

**하나라도 Yes → `is_infrastructure: true`**

### 2.3 Type별 자동 판정

| is_infrastructure | type |
|:-----------------:|------|
| **true** | component, component_tool, component_control |
| **false** | concept, technique, vulnerability, principle, pattern, protocol, tool_knowledge, control_policy |

---

## 3. 추상화 수준 (Level 1-4)

| Level | 이름 | 설명 | 예시 |
|-------|------|------|------|
| **4** | 원리 (Principle) | 보편적 진리 | "입력과 코드 혼합 위험", "최소 권한 원칙" |
| **3** | 개념 (Concept) | 추상적 분류 | "Injection", "인증 우회", "미들웨어" |
| **2** | 기법 (Technique) | 구체적 방법 | "UNION-based SQLi", "WAS", "RDBMS" |
| **1** | 인스턴스 (Instance) | 특정 사례 | "' OR 1=1 --", "Apache Tomcat 9.0" |

**규칙**: 하위 레벨은 반드시 상위 레벨을 참조 (`is_a` 관계)

---

## 4. 원자 유형 및 ID 체계

### 4.1 Type 목록

**인프라 요소 (is_infrastructure: true)**
| type | 설명 | 예시 |
|------|------|------|
| component | 인프라 구성요소 | Server, Database, VM |
| component_tool | 배포된 도구 | SIEM, EDR |
| component_control | 배포된 보안 통제 | WAF 장비, IDS/IPS |

**지식 요소 (is_infrastructure: false)**
| type | 설명 | 예시 |
|------|------|------|
| concept | 개념, 사상 | Zero Trust |
| technique | 공격/방어 기법 | SQL Injection |
| vulnerability | 취약점 | CVE, CWE |
| principle | 원칙 | Least Privilege |
| pattern | 패턴, 시그니처 | Payload |
| protocol | 프로토콜, 표준 | HTTP, TLS |
| tool_knowledge | 도구 지식 | Metasploit 사용법 |
| control_policy | 정책/절차 | 접근통제 정책 |

### 4.2 ID 프리픽스

| 유형 | ID 프리픽스 | is_infrastructure |
|------|-------------|:-----------------:|
| Infrastructure | INFRA-*, COMP-* | true |
| Attack | ATK-* | false |
| Defense | DEF-* | false |
| Vulnerability | VUL-* | false |
| Tool | TOOL-* | true/false |
| Concept | CON-* | false |
| Protocol | PROTO-* | false |
| Compliance | COMP-* | false |

### 4.3 ID 규칙

- 형식: `{PREFIX}-{SUBDOMAIN}-{NAME}-{###}`
- 예: `INFRA-APP-WAS-001`, `ATK-INJ-SQL-001`
- 숫자는 001부터 순차 부여

---

## 5. 원자 기본 구조

### 5.1 인프라 원자 (is_infrastructure: true)

```yaml
identity:
  id: "COMP-APP-WAS-001"
  name: "Web Application Server"
  normalization:
    normalized_name: "web application server"
    normalization_version: "1.0"
  aliases:
    - "WAS"
    - "App Server"
    - "웹 애플리케이션 서버"

classification:
  domain: application
  type: component
  is_infrastructure: true           # ✅ 인프라 요소
  abstraction_level: 2
  gr_coordinates:                   # 3D 좌표 (위치)
    layer: "L7"
    zone: "Z2"
    function: ["A2.1", "S2.2"]      # ※ tags 아님!
  atom_tags: ["WEB", "LINUX"]       # 원자 특성 태그

definition:
  what: |
    웹 애플리케이션을 실행하는 서버 소프트웨어...
  why: |
    비즈니스 로직 실행과 웹 서비스 제공을 위해...
  how: |
    HTTP 요청을 받아 서블릿/JSP를 처리하고...

relations:
  structural:
    is_a: ["CON-MIDDLEWARE-001"]
  causal:
    enables: ["ATK-EXEC-DESER-001"]
    requires: ["INFRA-RUNTIME-JVM-001"]
  implementation:
    implements: ["PROTO-HTTP-001"]   # 프로토콜 구현

properties:
  technical:
    default_port: 8080
    # ...

metadata:
  trust:
    source: official
    confidence: 0.95
  temporal:
    created: 2026-02-03
    modified: 2026-02-03
    revision: 1
  ai:
    embedding_text: |
      Web Application Server는 웹 애플리케이션을...
    search_keywords:
      - "WAS"
      - "웹서버"
      - "애플리케이션 서버"
```

### 5.2 지식 원자 (is_infrastructure: false)

```yaml
identity:
  id: "ATK-INJ-SQL-001"
  name: "SQL Injection"
  normalization:
    normalized_name: "sql injection"
    normalization_version: "1.0"
  aliases:
    - "SQLi"
    - "SQL 인젝션"

classification:
  domain: security
  type: technique
  is_infrastructure: false          # ✅ 지식 요소
  abstraction_level: 2
  scope:                            # 적용 범위 (gr_coordinates 대신)
    target_layers: ["L7"]
    target_zones: ["Z2", "Z3"]
  atom_tags: ["INJ", "WEB", "INITIAL", "MYSQL", "PGSQL"]

definition:
  what: |
    사용자 입력이 SQL 쿼리에 삽입되어 데이터베이스를 조작하는 공격...
  why: |
    데이터 유출, 인증 우회, 시스템 장악이 가능하기 때문에...
  how: |
    1) 입력 필드 식별 2) 메타문자 주입 3) 쿼리 조작...

relations:
  structural:
    is_a: ["CON-INJECTION-001"]
  causal:
    enables: ["ATK-DATA-EXFIL-001"]
    requires: ["TECH-SQL-001"]
    prevents: []
  applicability:
    applies_to: ["COMP-RDBMS-001", "COMP-WAS-001"]
    effective_against: ["DEF-INPUT-VALID-001"]

properties:
  technical:
    mitre_id: "T1190"
    cwe_id: "CWE-89"
    # ...

metadata:
  # ... (동일 구조)
```

---

## 6. 관계 타입

### 6.1 허용된 관계 (Canonical)

**구조적 (structural)**
```
is_a         → 상위 개념이다 (SQLi is_a Injection)
part_of      → 구성 요소다 (Payload part_of Attack)
instance_of  → 구체적 사례다 (' OR 1=1 instance_of SQLi)
abstracts    → 추상화한다 (원리 → 개념)
```

**인과적 (causal)**
```
causes       → 야기한다 (SQLi causes DataBreach)
enables      → 가능하게 한다 (FileRead enables RCE)
prevents     → 방지한다 (PreparedStatement prevents SQLi)
```

**조건적 (conditional)**
```
requires     → 필요로 한다 (xp_cmdshell requires sysadmin)
conflicts_with → 상충한다 (대칭)
alternative_to → 대체 가능하다 (대칭)
```

**적용 (applicability)**
```
applies_to       → 적용 대상이다 (SQLi applies_to RDBMS)
effective_against → 효과적이다 (Bypass effective_against WAF)
```

**구현 (implementation)**
```
implements   → 프로토콜/표준을 구현한다 (Apache implements HTTP)
```

### 6.2 금지된 관계

```yaml
# ❌ 절대 금지
related_to: [...]   # 의미 모호, 무한 확장 가능

# 대안:
# - 정밀한 관계 타입 사용 (is_a, enables, applies_to 등)
# - 느슨한 연관은 atom_tags로 처리
```

---

## 7. GR 좌표계 vs atom_tags

### 7.1 차이점

| 구분 | gr_coordinates.function | atom_tags |
|------|------------------------|-----------|
| **대상** | 인프라만 (is_infrastructure: true) | 모든 원자 |
| **의미** | "어디에 위치하는가" (3D 좌표) | "어떤 특성인가" (분류) |
| **구조** | 계층적 (A2.1, S3.2) | 평면적 (INJ, WEB) |
| **참조** | 02_framework/.../Function_Tag/ | 03_ontology/taxonomy/atom_tags.yaml |

### 7.2 예시

```yaml
# 인프라 원자
gr_coordinates:
  layer: "L7"
  zone: "Z2"
  function: ["A2.2", "S2.1", "M2.1"]  # 3D 좌표 Function

atom_tags: ["WEB", "LINUX", "PROXY"]   # 특성 분류

---

# 지식 원자 (gr_coordinates 없음)
scope:
  target_layers: ["L7"]
  target_zones: ["Z2", "Z3"]

atom_tags: ["INJ", "WEB", "MYSQL"]     # 특성 분류
```

---

## 8. 품질 체크리스트

### 필수 항목

- [ ] ID가 명명 규칙을 따르는가?
- [ ] type이 올바른가?
- [ ] is_infrastructure가 type과 일치하는가?
- [ ] 인프라 원자: gr_coordinates (layer, zone, function)가 모두 있는가?
- [ ] 지식 원자: scope (target_layers, target_zones)가 있는가?
- [ ] atom_tags가 1개 이상인가?
- [ ] definition.what이 작성되었는가?
- [ ] 관계가 3개 이상인가?
- [ ] `related_to`를 사용하지 않았는가?
- [ ] Zone 형식이 "Z숫자"인가? (Z3 ❌ → Z3 ✅)

### 권장 항목

- [ ] definition.why, definition.how가 있는가?
- [ ] 관계가 5개 이상인가?
- [ ] embedding_text가 충실한가?
- [ ] search_keywords가 5개 이상인가?

---

## 9. 외부 참조

### 표준 프레임워크
- MITRE ATT&CK: https://attack.mitre.org/
- MITRE D3FEND: https://d3fend.mitre.org/
- CWE: https://cwe.mitre.org/
- OWASP: https://owasp.org/

### 프로젝트 내부 참조
- 스키마: `03_ontology/schema/core/atom_schema.yaml`
- 관계 타입: `03_ontology/schema/core/relation_types.yaml`
- Atom Tags: `03_ontology/taxonomy/atom_tags.yaml`
- Layer: `03_ontology/taxonomy/layers.yaml`
- Zone: `03_ontology/taxonomy/zones.yaml`
- Function: `02_framework/GR_DB/03_차원3_Function_Tag/`

---

## 10. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 2.0 | 2026-02-03 | is_infrastructure 추가, related_to 금지, function/atom_tags 구분, Zone 형식 변경 |
| 1.0 | 2025-01-29 | 초기 버전 |

---

*GR Ontology - 지식을 연결하여 AI가 맥락을 이해하게 한다*
