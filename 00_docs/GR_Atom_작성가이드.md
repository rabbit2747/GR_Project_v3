# GR Atom 작성 가이드

> **목적**: 일관된 품질의 원자를 작성하기 위한 표준 가이드
> **최종 수정**: 2025-01-29

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

## 2. 추상화 수준 (Level 1-4)

| Level | 이름 | 설명 | 예시 |
|-------|------|------|------|
| **4** | 원리 (Principle) | 보편적 진리 | "입력과 코드 혼합 위험", "최소 권한 원칙" |
| **3** | 개념 (Concept) | 추상적 분류 | "Injection", "인증 우회", "미들웨어" |
| **2** | 기법 (Technique) | 구체적 방법 | "UNION-based SQLi", "WAS", "RDBMS" |
| **1** | 인스턴스 (Instance) | 특정 사례 | "' OR 1=1 --", "Apache Tomcat 9.0" |

**규칙**: 하위 레벨은 반드시 상위 레벨을 참조 (`is_a` 관계)

---

## 3. 원자 유형 및 ID 체계

### 3.1 ID 프리픽스

| 유형 | ID 프리픽스 | 설명 | 예시 |
|------|-------------|------|------|
| Infrastructure | INFRA-* | 인프라 구성요소 | WAS, DB, 방화벽 |
| Attack | ATK-* | 공격 기법 | SQL Injection, XSS |
| Defense | DEF-* | 방어 기법 | WAF, 암호화 |
| Vulnerability | VUL-* | 취약점 유형 | CWE 기반 |
| Tool | TOOL-* | 도구 | Burp Suite, nmap |
| Concept | CON-* | 개념/원칙 | Zero Trust, Defense in Depth |
| Technology | TECH-* | 기술 | Protocol, Algorithm |
| Compliance | COMP-* | 컴플라이언스 | ISO 27001, GDPR |

### 3.2 ID 규칙

- 형식: `{DOMAIN}-{SUBDOMAIN}-{NAME}-{###}`
- 예: `INFRA-APP-WAS-001`, `ATK-INJECT-SQL-001`
- 숫자는 001부터 순차 부여

---

## 4. 원자 기본 구조

```yaml
identity:
  id: "INFRA-APP-WAS-001"           # 필수: 고유 ID
  name: "Web Application Server"    # 필수: 정식 명칭
  normalization:
    normalized_name: "web_application_server"  # 필수: 정규화된 이름
    normalization_version: "1.0"
  aliases:                          # 권장: 검색용 별칭
    - "WAS"
    - "App Server"
    - "웹 애플리케이션 서버"

classification:
  domain: "infrastructure"          # 필수: 도메인
  type: "component"                 # 필수: 유형
  abstraction_level: 2              # 필수: 추상화 수준 (1-4)
  gr_coordinates:                   # 필수: GR 좌표
    layer: "L7"
    zone: "Zone2"
    tags: ["A-runtime", "S-session"]

definition:
  what: |
    [200-300자] 이것이 무엇인가? 핵심 특징과 역할 설명
  why: |
    [150-200자] 왜 중요한가? 존재 이유와 가치
  how: |
    [200-400자] 어떻게 작동하는가? 동작 원리나 프로세스

relations:
  structural:
    is_a:
      - "CON-MIDDLEWARE-001"        # 상위 개념
    has_children:
      - "INFRA-APP-WAS-TOMCAT-001"  # 하위 유형
    related_to:
      - "INFRA-DATA-RDBMS-001"      # 관련 개념
  causal:
    enables:
      - "ATK-EXEC-DESER-001"        # 가능하게 하는 것
    requires:
      - "INFRA-RUNTIME-JVM-001"     # 필요로 하는 것

properties:
  technical:
    # 원자 유형별 기술 속성
    components: []
    protocols: []
    # ...

metadata:
  trust:
    source: "official"
    references:
      - "공식 문서 URL"
      - "MITRE/CWE/OWASP 참조"
    confidence: 0.95                # 0.0-1.0 신뢰도
    verified:
      status: verified
      date: 2025-01-29
      by: "작성자"
  temporal:
    created: 2025-01-29
    modified: 2025-01-29
    revision: 1
  security:
    sensitivity: public
  ai:
    embedding_text: |
      LLM 임베딩을 위한 요약 텍스트
    search_keywords:
      - "keyword1"
      - "keyword2"
```

---

## 5. 주요 관계 타입

### 5.1 구조적 관계 (Structural)

```
is_a           → A는 B의 하위 개념이다
has_children   → A는 B를 하위 개념으로 갖는다
has_parts      → A는 B를 구성요소로 갖는다
related_to     → A는 B와 관련된다
```

### 5.2 인과 관계 (Causal)

```
requires       → A는 B를 필요로 한다
enables        → A는 B를 가능하게 한다
prevents       → A는 B를 방지한다
causes         → A는 B를 유발한다
```

### 5.3 보안 관계

```
targets        → 공격이 대상으로 하는 것
exploits       → 공격이 악용하는 취약점
mitigates      → 방어가 완화하는 것
protects       → 방어가 보호하는 것
vulnerable_to  → 인프라가 취약한 공격/취약점
```

**최소 관계 수**: 5개 이상

---

## 6. 권장 섹션

### 6.1 Core Concepts (핵심 개념)

```yaml
core_concepts:
  - name: "Thread Pool"
    description: "동시 요청 처리를 위한 스레드 재사용 메커니즘"
    security_relevance: "과도한 요청 시 DoS 가능"
```

**작성 기준**: 해당 원자 이해에 필수적인 개념만 포함 (3-7개)

### 6.2 Security Profile (보안 프로파일)

```yaml
security:
  attack_surface:
    exposed_ports:
      - port: 8080
        service: "HTTP"
        risk: "medium"
    exposed_interfaces:
      - "Management Console"
      - "REST API"

  common_vulnerabilities:
    - id: "VUL-DESER-001"
      name: "Insecure Deserialization"
      cwe: "CWE-502"

  attack_techniques:
    - id: "ATK-RCE-DESER-001"
      name: "Deserialization RCE"
      mitre: "T1190"

  defenses:
    - id: "DEF-WAF-001"
      name: "Web Application Firewall"
      effectiveness: "high"
```

### 6.3 Products (제품) - 인프라 원자용

```yaml
products:
  open_source:
    - name: "Apache Tomcat"
      vendor: "Apache Foundation"
      use_case: "경량, 단독 실행"
  commercial:
    - name: "Oracle WebLogic"
      vendor: "Oracle"
      use_case: "엔터프라이즈"
```

### 6.4 MITRE/CWE 매핑 - 공격/방어 원자용

```yaml
mitre_mapping:
  technique_id: "T1190"
  technique_name: "Exploit Public-Facing Application"
  tactic: "Initial Access"

cwe_mapping:
  cwe_id: "CWE-89"
  cwe_name: "SQL Injection"
```

---

## 7. 원자 유형별 특화 가이드

### 7.1 인프라 원자 (INFRA-*)

**필수 추가 섹션**:
- `products`: 실제 제품 목록
- `protocols`: 사용 프로토콜
- `security.attack_surface`: 노출 포트/인터페이스

**관계 중점**:
- `connects_to`: 네트워크 토폴로지
- `runs_on`: 실행 환경
- `vulnerable_to`: 관련 취약점

### 7.2 공격 원자 (ATK-*)

**필수 추가 섹션**:
- `mitre_mapping`: ATT&CK 매핑
- `typical_flow`: 공격 단계
- `indicators`: 탐지 지표

**관계 중점**:
- `targets`: 공격 대상 인프라
- `exploits`: 악용 취약점
- `enables`: 후속 공격
- `countered_by`: 방어 기법

### 7.3 방어 원자 (DEF-*)

**필수 추가 섹션**:
- `d3fend_mapping`: D3FEND 매핑
- `implementation`: 구현 방법
- `effectiveness`: 효과성 평가

**관계 중점**:
- `mitigates`: 완화 대상 (공격/취약점)
- `protects`: 보호 대상 인프라
- `requires`: 필요 조건
- `complements`: 보완 기법

### 7.4 취약점 원자 (VUL-*)

**필수 추가 섹션**:
- `cwe_id`: CWE 매핑
- `severity`: 심각도
- `exploitation`: 악용 방법

**관계 중점**:
- `affects`: 영향받는 인프라
- `exploited_by`: 악용 공격 기법
- `mitigated_by`: 완화 방법
- `related_cves`: 실제 CVE 사례

---

## 8. 품질 체크리스트

### 필수 항목

- [ ] ID가 명명 규칙을 따르는가?
- [ ] GR 좌표(Layer/Zone/Tags)가 모두 지정되었는가?
- [ ] definition의 what/why가 모두 작성되었는가?
- [ ] 관계가 5개 이상인가?
- [ ] 출처가 명시되었는가?
- [ ] confidence 값이 설정되었는가?

### 권장 항목

- [ ] core_concepts가 3개 이상인가?
- [ ] 보안 관련 원자의 경우 security 섹션이 있는가?
- [ ] 인프라 원자의 경우 products 섹션이 있는가?
- [ ] protocols 정보가 있는가?

### 품질 기준

- [ ] 전문 용어가 적절히 설명되었는가?
- [ ] 문장이 명확하고 간결한가?
- [ ] 보안 관련성이 충분히 설명되었는가?
- [ ] 관계가 양방향으로 일관성 있는가?
- [ ] 고립된 원자가 아닌가? (관계 없는 원자는 의미 없음)

---

## 9. 작성 프로세스

```
1. 주제 선정
   └── 우선순위 목록에서 선택

2. 자료 조사
   ├── 공식 문서
   ├── MITRE/CWE/OWASP
   ├── 기술 블로그
   └── 실무 경험

3. 템플릿 복사
   └── 기존 원자 참고

4. 섹션별 작성
   ├── Identity → Classification → Definition
   └── Relations → Security → Properties → Metadata

5. 품질 검증
   ├── 체크리스트 확인
   └── 관계 일관성 검토

6. 피어 리뷰
   └── PR 생성 및 리뷰

7. 머지 및 인덱싱
   └── 관계 연결 확인
```

---

## 10. 외부 참조

### 표준 프레임워크
- MITRE ATT&CK: https://attack.mitre.org/
- MITRE D3FEND: https://d3fend.mitre.org/
- CWE: https://cwe.mitre.org/
- OWASP: https://owasp.org/

### 프로젝트 참조
- 스키마: `01_schema/gr_atom_schema.yaml`
- 기존 원자 예시: `02_knowledge_base/` 디렉토리

---

*GR Ontology - 지식을 연결하여 AI가 맥락을 이해하게 한다*
