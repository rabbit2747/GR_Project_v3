# GR IaC Lab Auto-Generation System - 설계 문서

## 📋 문서 정보
- **문서명**: GR IaC Lab 자동 생성 시스템 설계
- **버전**: 1.0
- **작성일**: 2025-01-21
- **목적**: CVE 기반 취약점 실습 환경 자동 생성 시스템 설계

---

## 1. 시스템 개요

### 1.1 핵심 가치 제안

**"CVE 번호 하나로 → 2분 안에 → 실전 같은 취약점 실습 환경 자동 생성"**

```
입력: CVE-2025-64709
출력 (2분 후):
  - 실습 환경 URL: https://lab-abc123.gr-edu.com
  - 공격자 계정: attacker / pass123
  - 피해자 계정: victim1 / pass456
  - 실습 가이드: 5단계 미션
  - 자동 종료: 2시간 후
```

### 1.2 8단계 파이프라인

```
1. CVE 입력 (사용자)
   ↓
2. DB 검색 (GR DB - vuln_cve 테이블)
   ↓
3. 세세한 해석 (AI/LLM - Root Cause 분석)
   ↓
4. 환경 선택 (시나리오 Archetype 매핑)
   ↓
5. 시나리오 작성 (스토리 생성)
   ↓
6. 요소 정의 (인프라 컴포넌트 리스트업)
   ↓
7. IaC 생성 (Terraform + Ansible)
   ↓
8. 환경 배포 (Lab Orchestrator)
```

### 1.3 GR Framework와의 통합

**기존 GR Framework 자산 활용**:
- ✅ Layer/Zone 좌표계 → 네트워크 토폴로지
- ✅ Function Tags → 인프라 요소 선택
- ✅ Security Policies → 방화벽 규칙
- ✅ CVE-MITRE 매핑 → 공격 시나리오
- ✅ Components 분류 → IaC 템플릿 선택

---

## 2. 시스템 아키텍처

### 2.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                    GR IaC Lab System                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Web UI /   │─────>│   CVE        │─────>│  Scenario    │ │
│  │   API        │      │   Service    │      │  Engine      │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│         │                     │                      │         │
│         │                     ▼                      ▼         │
│         │              ┌─────────────┐       ┌─────────────┐  │
│         │              │   GR DB     │       │   LLM       │  │
│         │              │  (PostgreSQL)│       │  Service    │  │
│         │              └─────────────┘       └─────────────┘  │
│         │                     │                      │         │
│         ▼                     ▼                      ▼         │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              IaC Generator Service                       │ │
│  │  - Template Manager                                      │ │
│  │  - Variable Injector                                     │ │
│  │  - Code Validator                                        │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                      │
│         ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Lab Orchestrator                            │ │
│  │  - Terraform Executor                                    │ │
│  │  - Ansible Runner                                        │ │
│  │  - Resource Manager (TTL, Cleanup)                       │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                      │
│         ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │           Cloud Infrastructure                           │ │
│  │  AWS / Azure / GCP / On-Premise                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 핵심 컴포넌트

#### CVE Service
```yaml
역할:
  - CVE 번호 검증 및 조회
  - GR DB에서 취약점 메타데이터 추출
  - 지원 여부 판정 (full/partial/unsupported)

주요 API:
  - GET /api/cve/{cve_id}/info
  - GET /api/cve/{cve_id}/lab-support
  - POST /api/cve/search (키워드 검색)
```

#### Scenario Engine
```yaml
역할:
  - 취약점 → 시나리오 Archetype 매핑
  - LLM 기반 스토리 생성
  - 필요한 인프라 요소 결정

주요 기능:
  - archetype_matcher(): CVE → 시나리오 추천
  - story_generator(): 교육용 내러티브 생성
  - component_selector(): GR Tags → 인프라 요소
```

#### IaC Generator Service
```yaml
역할:
  - Terraform 코드 생성 (인프라)
  - Ansible Playbook 생성 (설정)
  - 템플릿 + 변수 주입 방식

주요 모듈:
  - template_manager: 템플릿 저장/버전 관리
  - variable_injector: CVE 정보 → 변수 값
  - code_validator: 생성된 코드 검증
```

#### Lab Orchestrator
```yaml
역할:
  - Terraform apply/destroy 실행
  - Ansible playbook 실행
  - 리소스 수명 관리 (TTL)

주요 기능:
  - create_lab(): 환경 생성
  - destroy_lab(): 환경 삭제
  - extend_ttl(): 시간 연장
  - get_status(): 상태 조회
```

---

## 3. 데이터베이스 스키마 (GR DB 확장)

### 3.1 취약점 실습 지원 정보

#### vuln_lab_support 테이블
```sql
-- CVE별 실습 자동 생성 지원 정보
CREATE TABLE vuln_lab_support (
    id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50) NOT NULL UNIQUE REFERENCES cve(cve_id),

    -- 지원 수준
    support_level VARCHAR(20) NOT NULL,  -- full, partial, unsupported
    support_notes TEXT,

    -- 자동 생성 가능 여부
    auto_generation_enabled BOOLEAN DEFAULT FALSE,
    manual_review_required BOOLEAN DEFAULT TRUE,

    -- 구조화된 취약점 정보 (JSON)
    vuln_detail JSONB NOT NULL,
    /*
    {
      "affected_product": "GenericShop-WebApp",
      "affected_component": "OrderController",
      "root_cause_type": "Business Logic",
      "root_cause_detail": "Missing authorization check",
      "preconditions": ["authenticated_user", "api_access"],
      "trigger_method": "Modify order_id in URL",
      "impact": ["info_disclosure", "privilege_escalation"],
      "api_info": {
        "method": "GET",
        "path": "/api/orders/{order_id}",
        "auth_required": true,
        "authz_missing": "check_ownership(order_id, user_id)"
      }
    }
    */

    -- 추천 시나리오
    recommended_archetype_id INTEGER REFERENCES scenario_archetypes(id),
    alternative_archetype_ids INTEGER[],

    -- 생성 통계
    lab_creation_count INTEGER DEFAULT 0,
    avg_creation_time_seconds INTEGER,
    success_rate DECIMAL(5,2),

    -- 메타데이터
    analyzed_by VARCHAR(100),  -- 'AI_BATCH', 'MANUAL', 'HYBRID'
    analyzed_at TIMESTAMP,
    last_verified TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vuln_lab_cve ON vuln_lab_support(cve_id);
CREATE INDEX idx_vuln_lab_support_level ON vuln_lab_support(support_level);
CREATE INDEX idx_vuln_lab_archetype ON vuln_lab_support(recommended_archetype_id);
CREATE INDEX idx_vuln_lab_detail ON vuln_lab_support USING GIN (vuln_detail);
```

### 3.2 시나리오 Archetype

#### scenario_archetypes 테이블
```sql
-- 실습 환경 시나리오 템플릿 (쇼핑몰, 기업, 공장 등)
CREATE TABLE scenario_archetypes (
    id SERIAL PRIMARY KEY,

    -- 기본 정보
    archetype_code VARCHAR(50) NOT NULL UNIQUE,  -- 'online_shop_checkout'
    archetype_name VARCHAR(255) NOT NULL,        -- '온라인 쇼핑몰 결제 시스템'
    description TEXT,

    -- 시나리오 속성
    industry VARCHAR(100),              -- 'retail', 'finance', 'manufacturing'
    service_type VARCHAR(100),          -- 'e-commerce', 'hr-portal', 'scada'
    typical_users TEXT[],               -- ['customer', 'admin', 'staff']

    -- 인프라 구조 (JSON)
    infra_structure JSONB NOT NULL,
    /*
    {
      "layers": [
        {"layer": "L0", "components": ["attacker-vm"]},
        {"layer": "L1", "components": ["nginx-proxy", "waf"]},
        {"layer": "L2", "components": ["web-app", "api-server"]},
        {"layer": "L3", "components": ["mysql-db", "redis-cache"]}
      ],
      "zones": [
        {"zone": "Zone_1", "subnet": "dmz", "components": ["nginx-proxy"]},
        {"zone": "Zone_2", "subnet": "app", "components": ["web-app"]},
        {"zone": "Zone_3", "subnet": "data", "components": ["mysql-db"]}
      ],
      "data_flow": [
        {"from": "attacker-vm", "to": "nginx-proxy", "protocol": "HTTPS"},
        {"from": "nginx-proxy", "to": "web-app", "protocol": "HTTP"},
        {"from": "web-app", "to": "mysql-db", "protocol": "MySQL"}
      ]
    }
    */

    -- 기본 컴포넌트 (Array of component IDs or tags)
    default_components JSONB,
    /*
    [
      {"name": "nginx", "tags": ["N1.1", "S3.1"], "required": true},
      {"name": "webapp", "tags": ["D2.1", "A1.1"], "required": true},
      {"name": "database", "tags": ["D1.1", "S3.1"], "required": true}
    ]
    */

    -- IaC 템플릿 참조
    terraform_template_id INTEGER REFERENCES lab_templates(id),
    ansible_template_id INTEGER REFERENCES lab_templates(id),

    -- 사용 통계
    usage_count INTEGER DEFAULT 0,
    avg_satisfaction_score DECIMAL(3,2),

    -- 메타데이터
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_archetype_code ON scenario_archetypes(archetype_code);
CREATE INDEX idx_archetype_industry ON scenario_archetypes(industry);
CREATE INDEX idx_archetype_structure ON scenario_archetypes USING GIN (infra_structure);
```

### 3.3 인프라 Atom (재사용 가능한 인프라 구성 요소)

#### infra_atoms 테이블
```sql
-- IaC에서 재사용 가능한 인프라 원자 단위
CREATE TABLE infra_atoms (
    id SERIAL PRIMARY KEY,

    -- 기본 정보
    atom_code VARCHAR(100) NOT NULL UNIQUE,  -- 'postgresql_base'
    atom_name VARCHAR(255) NOT NULL,
    atom_type VARCHAR(50) NOT NULL,          -- 'compute', 'network', 'storage', 'security'
    description TEXT,

    -- GR 좌표 매핑
    layer_id VARCHAR(20) REFERENCES layers(id),
    zone_id VARCHAR(20) REFERENCES zones(id),
    related_tags TEXT[],  -- Function Tags와 연결

    -- 기술 스택
    tech_stack VARCHAR(100),  -- 'postgresql', 'nginx', 'docker'
    version_pattern VARCHAR(100),  -- '15.x', '1.23.x', 'latest'

    -- IaC 코드 조각
    terraform_snippet TEXT,
    /*
    module "postgresql" {
      source  = "./modules/postgresql"
      version = var.postgres_version
      ...
    }
    */

    ansible_snippet TEXT,
    /*
    - role: postgresql
      vars:
        postgres_version: "{{ postgres_version }}"
    */

    docker_image VARCHAR(255),  -- 'postgres:15.4-alpine'

    -- 의존성
    depends_on_atoms INTEGER[],  -- 다른 atom IDs
    conflicts_with_atoms INTEGER[],

    -- 설정 변수
    required_vars JSONB,  -- {'db_name': 'string', 'db_user': 'string'}
    default_vars JSONB,   -- {'db_port': 5432, 'max_connections': 100}

    -- 보안 설정
    security_hardening TEXT,  -- 보안 강화 설정 스크립트
    vulnerable_config TEXT,   -- 취약한 설정 (실습용)

    -- 사용 통계
    usage_count INTEGER DEFAULT 0,
    avg_deployment_time_seconds INTEGER,

    -- 메타데이터
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_atom_code ON infra_atoms(atom_code);
CREATE INDEX idx_atom_type ON infra_atoms(atom_type);
CREATE INDEX idx_atom_layer ON infra_atoms(layer_id);
CREATE INDEX idx_atom_zone ON infra_atoms(zone_id);
CREATE INDEX idx_atom_tags ON infra_atoms USING GIN (related_tags);
```

### 3.4 IaC 템플릿

#### lab_templates 테이블
```sql
-- Terraform/Ansible 템플릿 저장소
CREATE TABLE lab_templates (
    id SERIAL PRIMARY KEY,

    -- 기본 정보
    template_code VARCHAR(100) NOT NULL UNIQUE,
    template_name VARCHAR(255) NOT NULL,
    template_type VARCHAR(50) NOT NULL,  -- 'terraform', 'ansible'
    description TEXT,

    -- 시나리오 연결
    archetype_id INTEGER REFERENCES scenario_archetypes(id),
    cve_pattern VARCHAR(100),  -- 이 템플릿이 적용 가능한 CVE 패턴

    -- 템플릿 코드
    template_content TEXT NOT NULL,
    template_version VARCHAR(20) DEFAULT '1.0.0',

    -- 변수 정의
    variables JSONB NOT NULL,
    /*
    {
      "cve_id": {"type": "string", "required": true},
      "vuln_component": {"type": "string", "required": true},
      "attacker_ip": {"type": "string", "default": "auto"},
      "db_init_sql": {"type": "string", "required": true}
    }
    */

    -- 사용하는 Atom 목록
    required_atoms INTEGER[],  -- infra_atoms IDs

    -- 출력 정보
    outputs JSONB,
    /*
    {
      "lab_url": "output.web_app_url",
      "attacker_ssh": "output.attacker_vm_ip",
      "credentials": ["admin_user", "victim_user"]
    }
    */

    -- 검증
    validation_script TEXT,  -- 생성 후 검증 스크립트
    estimated_cost_usd DECIMAL(8,2),
    estimated_time_seconds INTEGER,

    -- 버전 관리
    parent_template_id INTEGER REFERENCES lab_templates(id),
    is_active BOOLEAN DEFAULT TRUE,

    -- 사용 통계
    usage_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2),
    avg_execution_time_seconds INTEGER,

    -- 메타데이터
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_template_code ON lab_templates(template_code);
CREATE INDEX idx_template_type ON lab_templates(template_type);
CREATE INDEX idx_template_archetype ON lab_templates(archetype_id);
CREATE INDEX idx_template_active ON lab_templates(is_active);
```

### 3.5 실습 환경 인스턴스

#### lab_instances 테이블
```sql
-- 생성된 실습 환경 추적
CREATE TABLE lab_instances (
    id SERIAL PRIMARY KEY,

    -- 기본 정보
    instance_id VARCHAR(100) NOT NULL UNIQUE,  -- 'lab-abc123'
    cve_id VARCHAR(50) NOT NULL REFERENCES cve(cve_id),
    archetype_id INTEGER REFERENCES scenario_archetypes(id),

    -- 사용자 정보
    user_id INTEGER,  -- 실습생 ID (외부 시스템)
    user_email VARCHAR(255),

    -- 상태
    status VARCHAR(50) NOT NULL,  -- 'creating', 'ready', 'running', 'stopping', 'stopped', 'error'
    status_message TEXT,

    -- 수명 관리
    created_at TIMESTAMP DEFAULT NOW(),
    ready_at TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,  -- TTL
    destroyed_at TIMESTAMP,

    -- 접속 정보
    access_info JSONB,
    /*
    {
      "lab_url": "https://lab-abc123.gr-edu.com",
      "attacker_credentials": {"user": "attacker", "pass": "pass123"},
      "victim_credentials": {"user": "victim1", "pass": "pass456"},
      "ssh_endpoints": ["52.23.45.67:22"],
      "guide_url": "https://gr-edu.com/guides/cve-2025-64709"
    }
    */

    -- 인프라 정보
    cloud_provider VARCHAR(50),  -- 'aws', 'azure', 'gcp', 'on-premise'
    cloud_region VARCHAR(50),
    resource_ids JSONB,  -- AWS 인스턴스 ID 등

    -- IaC 정보
    terraform_state_path VARCHAR(500),
    terraform_workspace VARCHAR(100),
    ansible_inventory TEXT,

    -- 사용 통계
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP,

    -- 비용
    estimated_cost_usd DECIMAL(8,2),
    actual_cost_usd DECIMAL(8,2),

    -- 메타데이터
    template_ids JSONB,  -- 사용된 템플릿 IDs
    created_by VARCHAR(100),
    notes TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_instance_id ON lab_instances(instance_id);
CREATE INDEX idx_instance_cve ON lab_instances(cve_id);
CREATE INDEX idx_instance_user ON lab_instances(user_id);
CREATE INDEX idx_instance_status ON lab_instances(status);
CREATE INDEX idx_instance_expires ON lab_instances(expires_at);
CREATE INDEX idx_instance_created ON lab_instances(created_at);
```

### 3.6 실습 로그 및 피드백

#### lab_activity_logs 테이블
```sql
-- 실습 환경 사용 로그
CREATE TABLE lab_activity_logs (
    id SERIAL PRIMARY KEY,
    instance_id VARCHAR(100) NOT NULL REFERENCES lab_instances(instance_id),

    -- 활동 정보
    activity_type VARCHAR(50) NOT NULL,  -- 'access', 'exploit_attempt', 'success', 'failure'
    activity_detail JSONB,

    -- 타임스탬프
    occurred_at TIMESTAMP DEFAULT NOW(),

    -- 출처
    source_ip VARCHAR(45),
    user_agent TEXT
);

CREATE INDEX idx_activity_instance ON lab_activity_logs(instance_id);
CREATE INDEX idx_activity_type ON lab_activity_logs(activity_type);
CREATE INDEX idx_activity_time ON lab_activity_logs(occurred_at);
```

#### lab_feedback 테이블
```sql
-- 실습 환경 피드백
CREATE TABLE lab_feedback (
    id SERIAL PRIMARY KEY,
    instance_id VARCHAR(100) NOT NULL REFERENCES lab_instances(instance_id),
    cve_id VARCHAR(50) NOT NULL REFERENCES cve(cve_id),

    -- 평가
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5),
    difficulty_score INTEGER CHECK (difficulty_score BETWEEN 1 AND 5),
    realism_score INTEGER CHECK (realism_score BETWEEN 1 AND 5),

    -- 피드백
    feedback_text TEXT,
    issues_encountered TEXT[],

    -- 메타데이터
    user_id INTEGER,
    submitted_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feedback_instance ON lab_feedback(instance_id);
CREATE INDEX idx_feedback_cve ON lab_feedback(cve_id);
CREATE INDEX idx_feedback_satisfaction ON lab_feedback(satisfaction_score);
```

---

## 4. 핵심 프로세스 상세 설계

### 4.1 CVE → 구조화된 정보 (3단계)

**입력**: CVE-2025-64709

**처리 과정**:

```python
class CVEAnalyzer:
    def analyze_cve_detailed(self, cve_id: str) -> VulnDetail:
        # 1. 기본 정보 수집
        cve_data = self.fetch_from_nvd(cve_id)
        vendor_advisories = self.fetch_vendor_advisories(cve_id)
        poc_links = self.search_poc_exploits(cve_id)

        # 2. LLM 분석
        prompt = f"""
        Analyze the following CVE and extract structured information:

        CVE ID: {cve_id}
        NVD Description: {cve_data['description']}
        Vendor Advisory: {vendor_advisories}
        PoC Links: {poc_links}

        Extract:
        1. Affected product and component
        2. Root cause type (config/code/logic/network)
        3. Detailed root cause explanation
        4. Preconditions for exploitation
        5. Step-by-step trigger method
        6. Impact (info disclosure/privilege escalation/RCE/etc)
        7. API/HTTP details if applicable

        Return as JSON following this schema:
        {{
          "affected_product": "...",
          "affected_component": "...",
          "root_cause_type": "...",
          ...
        }}
        """

        llm_result = self.llm_service.analyze(prompt)

        # 3. 검증 및 보정
        validated = self.validate_llm_output(llm_result)

        # 4. GR DB에 저장
        self.save_to_vuln_lab_support(cve_id, validated)

        return validated
```

**출력 예시**:
```json
{
  "affected_product": "GenericShop-WebApp v2.x",
  "affected_component": "OrderController /api/orders/{order_id}",
  "root_cause_type": "Business Logic",
  "root_cause_detail": "Missing authorization check - API only verifies authentication but does not check if the logged-in user owns the requested order_id",
  "preconditions": [
    "Attacker must have a valid account",
    "API endpoint must be accessible",
    "Order IDs must be predictable (sequential integers)"
  ],
  "trigger_method": "1. Login with attacker account\n2. View own order (e.g., /api/orders/12345)\n3. Modify order_id in URL to victim's order ID\n4. Server returns victim's order details without authorization check",
  "impact": [
    "Horizontal privilege escalation",
    "PII disclosure (name, address, phone)",
    "Potential payment manipulation"
  ],
  "api_info": {
    "method": "GET",
    "path": "/api/orders/{order_id}",
    "auth_required": true,
    "authz_missing": "check_ownership(order_id, current_user.id)"
  },
  "cvss_score": 7.5,
  "cwe": "CWE-639"
}
```

### 4.2 시나리오 Archetype 매핑 (4단계)

**입력**: 구조화된 CVE 정보 (위 JSON)

**매핑 로직**:

```python
class ScenarioMatcher:
    def match_archetype(self, vuln_detail: VulnDetail) -> List[Archetype]:
        candidates = []

        # Rule-based 매칭
        if "order" in vuln_detail.affected_component.lower():
            candidates.append(("online_shop_checkout", 0.9))

        if "payment" in vuln_detail.affected_component.lower():
            candidates.append(("online_shop_checkout", 0.95))
            candidates.append(("banking_transfer_portal", 0.7))

        if "employee" in vuln_detail.affected_product.lower():
            candidates.append(("company_hr_portal", 0.8))

        # LLM 기반 매칭 (fallback)
        if len(candidates) == 0:
            llm_recommendation = self.llm_match(vuln_detail)
            candidates.append((llm_recommendation, 0.6))

        # 정렬 및 반환
        candidates.sort(key=lambda x: x[1], reverse=True)

        return [self.get_archetype(c[0]) for c in candidates[:3]]
```

**출력**:
```yaml
Recommended Archetypes:
  1. online_shop_checkout (95% match)
     - 쇼핑몰 결제/주문 시스템
     - IDOR 취약점과 완벽히 부합

  2. company_procurement (60% match)
     - 기업 내부 구매 시스템
     - 대안 시나리오로 가능
```

### 4.3 시나리오 스토리 생성 (5단계)

**입력**:
- CVE 구조화 정보
- 선택된 Archetype (online_shop_checkout)

**생성 로직**:

```python
class StoryGenerator:
    def generate_scenario_story(
        self,
        vuln_detail: VulnDetail,
        archetype: Archetype
    ) -> Story:
        template = self.load_template(archetype.archetype_code)

        prompt = f"""
        Generate an educational security lab scenario story.

        Vulnerability: {vuln_detail.root_cause_detail}
        Scenario Type: {archetype.archetype_name}
        Target Audience: Security students/professionals

        Generate:
        1. Background (2-3 sentences about the service)
        2. Vulnerability Description (clear, educational)
        3. Attack Scenario (attacker perspective)
        4. Impact (business + technical)
        5. Learning Objectives (3-5 points)
        6. Ethical Guidelines (misuse warning)

        Tone: Educational, realistic, ethical
        Language: Korean
        Length: 300-500 words
        """

        story = self.llm_service.generate(prompt)

        # 템플릿 채우기
        final_story = template.format(
            background=story['background'],
            vulnerability=story['vulnerability'],
            ...
        )

        return final_story
```

**출력 예시**:

```markdown
# CVE-2025-64709 실습 시나리오: 쇼핑몰 주문 조회 IDOR 취약점

## 배경

'GR Shop'은 연간 거래액 100억 원 규모의 중견 온라인 쇼핑몰입니다.
회원은 로그인 후 "내 주문 내역" 메뉴에서 과거 주문 상세 정보를 확인할 수 있습니다.
이 기능은 고객 만족도가 높아 자주 사용되지만, 최근 보안 감사에서 심각한 결함이 발견되었습니다.

## 취약점 설명

주문 상세 조회 API(`GET /api/orders/{order_id}`)는 사용자가 로그인했는지만 확인하고,
**해당 주문이 실제로 그 사용자의 것인지는 검증하지 않습니다**.

이는 전형적인 IDOR(Insecure Direct Object Reference) 취약점으로,
공격자가 URL의 `order_id` 값만 바꾸면 다른 사용자의 주문 정보를 열람할 수 있습니다.

## 공격 시나리오

1. **공격자 Alice**는 GR Shop에 정상적으로 회원가입하고 1건의 주문을 진행합니다.
2. 자신의 주문 내역을 확인하던 중, URL이 `/api/orders/12345` 형태임을 발견합니다.
3. 개발자 도구를 열고, `12345`를 `12346`, `12347`로 바꿔가며 요청을 보냅니다.
4. 놀랍게도 다른 사용자들의 주문 정보(이름, 주소, 전화번호, 주문 상품)가 그대로 노출됩니다.
5. Alice는 자동화 스크립트로 `12000`~`15000` 범위의 모든 주문을 수집할 수 있습니다.

## 비즈니스 영향

- **개인정보 유출**: 수천 명의 고객 연락처, 배송지 정보 유출
- **법적 책임**: 개인정보보호법 위반으로 최대 5억 원 과징금
- **신뢰 손실**: 언론 보도 시 브랜드 이미지 실추
- **추가 범죄**: 보이스피싱, 스팸 등 2차 피해 가능

## 학습 목표

1. IDOR 취약점의 개념과 실제 발생 사례 이해
2. 인증(Authentication)과 인가(Authorization)의 차이 체득
3. 주문 소유권 검증 로직의 올바른 구현 방법 습득
4. Burp Suite 등 프록시 도구로 API 조작 실습
5. 수정된 코드로 취약점이 해결되었는지 재확인

## 실습 윤리 지침

⚠️ **경고**: 이 실습은 교육 목적의 격리된 환경에서만 진행됩니다.
실제 서비스에 대한 무단 침투 시도는 불법이며, 형사 처벌 대상입니다.

✅ **실습 환경**: 이 Lab은 실제 고객 정보가 아닌 더미 데이터를 사용합니다.
✅ **허용 범위**: 제공된 URL과 계정 내에서만 테스트하십시오.
✅ **악용 금지**: 습득한 기술을 악의적 목적으로 사용하지 마십시오.
```

### 4.4 인프라 요소 정의 (6단계)

**입력**:
- 선택된 Archetype (online_shop_checkout)
- CVE 정보

**요소 선택 로직**:

```python
class ComponentSelector:
    def select_components(
        self,
        archetype: Archetype,
        vuln_detail: VulnDetail
    ) -> List[InfraAtom]:
        components = []

        # 1. Archetype 기본 구조에서 필수 컴포넌트
        for comp in archetype.default_components:
            if comp['required']:
                atom = self.find_atom_by_tags(comp['tags'])
                components.append(atom)

        # 2. CVE 특화 컴포넌트
        if vuln_detail.affected_component == "API":
            components.append(self.find_atom("api_gateway"))

        if "database" in vuln_detail.affected_product.lower():
            db_atom = self.find_atom("mysql_vulnerable_idor")
            components.append(db_atom)

        # 3. GR Layer/Zone 매핑
        for comp in components:
            comp.layer = self.map_to_layer(comp)
            comp.zone = self.map_to_zone(comp)

        return components
```

**출력 예시**:

```yaml
Selected Components:

Layer 0 (External):
  - attacker-kali-vm
    Atom: kali_linux_base
    Tags: [T5.3 (Kali Linux), I2.1 (CLI)]
    Role: 공격자 머신

Layer 1 (Perimeter):
  - nginx-reverse-proxy
    Atom: nginx_proxy
    Tags: [N1.1 (Proxy), S3.1 (TLS)]
    Role: 리버스 프록시

Layer 2 (Application):
  - shop-webapp
    Atom: spring_boot_vuln_idor
    Tags: [D2.1 (Web App), T2.3 (Spring Boot), A1.1 (REST API)]
    Role: 취약한 주문 조회 API 포함

Layer 3 (Data):
  - mysql-database
    Atom: mysql_with_dummy_data
    Tags: [D1.1 (RDBMS), T2.1 (MySQL), D5.1 (Backup)]
    Role: 주문/사용자 데이터 저장

Network:
  - lab-vpc
    Subnets: [dmz, app, data]
    Security Groups: [sg-nginx, sg-app, sg-db]
```

### 4.5 IaC 코드 생성 (7단계)

**입력**:
- 선택된 컴포넌트 리스트
- Archetype 템플릿
- CVE 정보

**생성 로직**:

```python
class IaCGenerator:
    def generate_terraform(
        self,
        components: List[InfraAtom],
        archetype: Archetype,
        vuln_detail: VulnDetail
    ) -> str:
        # 1. 기본 템플릿 로드
        template = self.template_manager.get_terraform_template(
            archetype.terraform_template_id
        )

        # 2. 변수 준비
        variables = {
            'cve_id': vuln_detail.cve_id,
            'lab_name': f"lab-{generate_id()}",
            'components': []
        }

        # 3. 각 컴포넌트를 Terraform 모듈로 변환
        for comp in components:
            atom = self.atom_manager.get_atom(comp.atom_code)

            module_vars = {
                'name': comp.name,
                'image': atom.docker_image,
                'layer': comp.layer,
                'zone': comp.zone,
                **atom.default_vars
            }

            # 취약 설정 주입 (실습용)
            if comp.name == 'shop-webapp':
                module_vars['vuln_config'] = atom.vulnerable_config

            variables['components'].append({
                'module': atom.atom_code,
                'vars': module_vars
            })

        # 4. 템플릿 렌더링
        rendered = template.render(**variables)

        # 5. 검증
        self.validator.validate_terraform(rendered)

        return rendered
```

**출력 예시** (Terraform):

```hcl
# Auto-generated by GR IaC Lab System
# CVE: CVE-2025-64709
# Scenario: online_shop_checkout

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "lab_id" {
  default = "lab-abc123"
}

variable "ttl_hours" {
  default = 2
}

# Network
module "lab_network" {
  source = "./modules/lab_network"

  lab_id = var.lab_id

  subnets = {
    dmz  = "10.0.1.0/24"
    app  = "10.0.2.0/24"
    data = "10.0.3.0/24"
  }
}

# Layer 0: Attacker VM
module "attacker_vm" {
  source = "./modules/kali_linux"

  lab_id    = var.lab_id
  vpc_id    = module.lab_network.vpc_id
  subnet_id = module.lab_network.subnet_dmz

  ami           = data.aws_ami.kali_linux.id
  instance_type = "t3.medium"

  tags = {
    Layer = "L0"
    Zone  = "Zone_0-A"
    Role  = "Attacker"
  }
}

# Layer 1: Nginx Proxy
module "nginx_proxy" {
  source = "./modules/nginx_proxy"

  lab_id    = var.lab_id
  vpc_id    = module.lab_network.vpc_id
  subnet_id = module.lab_network.subnet_dmz

  backend_target = module.shop_webapp.private_ip
  ssl_cert       = module.lab_network.ssl_cert

  tags = {
    Layer = "L1"
    Zone  = "Zone_1"
    Role  = "ReverseProxy"
  }
}

# Layer 2: Shop WebApp (VULNERABLE)
module "shop_webapp" {
  source = "./modules/spring_boot_vuln_idor"

  lab_id    = var.lab_id
  vpc_id    = module.lab_network.vpc_id
  subnet_id = module.lab_network.subnet_app

  docker_image = "gr-registry.io/shop-app:vuln-idor-2025-64709"

  environment = {
    DB_HOST     = module.mysql_db.endpoint
    DB_NAME     = "shopdb"
    DB_USER     = "shopuser"
    DB_PASSWORD = module.mysql_db.password

    # VULNERABILITY INJECTION
    SKIP_AUTHORIZATION_CHECK = "true"
    LOG_SQL_QUERIES         = "true"
  }

  tags = {
    Layer = "L2"
    Zone  = "Zone_2"
    Role  = "WebApp"
    CVE   = "CVE-2025-64709"
  }
}

# Layer 3: MySQL Database
module "mysql_db" {
  source = "./modules/mysql_with_dummy_data"

  lab_id    = var.lab_id
  vpc_id    = module.lab_network.vpc_id
  subnet_id = module.lab_network.subnet_data

  db_name     = "shopdb"
  db_user     = "shopuser"
  db_password = random_password.db_password.result

  # Dummy data SQL
  init_sql_path = "${path.module}/data/shop_dummy_data.sql"

  tags = {
    Layer = "L3"
    Zone  = "Zone_3"
    Role  = "Database"
  }
}

# Outputs
output "lab_access_info" {
  value = {
    lab_url         = "https://${module.nginx_proxy.public_dns}"
    attacker_ssh    = "ssh root@${module.attacker_vm.public_ip}"
    attacker_pass   = random_password.attacker_password.result
    victim1_account = "victim1@shop.com / ${random_password.victim1_password.result}"
    victim2_account = "victim2@shop.com / ${random_password.victim2_password.result}"
    guide_url       = "https://gr-edu.com/guides/cve-2025-64709"
    expires_at      = timeadd(timestamp(), "${var.ttl_hours}h")
  }

  sensitive = true
}

# TTL Automation
resource "null_resource" "auto_destroy" {
  triggers = {
    expires_at = timeadd(timestamp(), "${var.ttl_hours}h")
  }

  provisioner "local-exec" {
    command = "sleep ${var.ttl_hours * 3600} && terraform destroy -auto-approve"
  }
}
```

**출력 예시** (Ansible Playbook):

```yaml
# Auto-generated by GR IaC Lab System
# CVE: CVE-2025-64709
---
- name: Setup CVE-2025-64709 Lab Environment
  hosts: all
  become: yes

  vars:
    lab_id: "lab-abc123"
    cve_id: "CVE-2025-64709"

- name: Configure Attacker VM
  hosts: attacker_vm
  roles:
    - role: kali_linux_setup
      tools:
        - burpsuite
        - zaproxy
        - python3
        - curl

    - role: lab_guide_desktop
      guide_url: "https://gr-edu.com/guides/cve-2025-64709"

- name: Configure Nginx Proxy
  hosts: nginx_proxy
  roles:
    - role: nginx_reverse_proxy
      backend_host: "{{ hostvars['shop_webapp'].ansible_host }}"
      backend_port: 8080
      ssl_enabled: true

- name: Configure Shop WebApp (VULNERABLE)
  hosts: shop_webapp
  roles:
    - role: spring_boot_app
      app_jar: "/opt/shop-app/shop-vuln-idor.jar"
      java_opts: "-Dspring.profiles.active=vulnerable"

    - role: vuln_idor_inject
      # This role intentionally disables authorization check
      config_file: "/opt/shop-app/application-vulnerable.yml"
      vuln_settings:
        skip_authz_check: true
        log_all_queries: true

    - role: monitoring_agent
      metrics_endpoint: "http://{{ hostvars['monitor'].ansible_host }}:9090"

- name: Configure MySQL Database
  hosts: mysql_db
  roles:
    - role: mysql_server
      mysql_root_password: "{{ vault_mysql_root_password }}"
      mysql_databases:
        - name: shopdb

    - role: mysql_dummy_data
      sql_file: "files/shop_dummy_data.sql"
      # Creates:
      # - users table: 10 users (victim1~victim10, attacker1)
      # - orders table: 50 orders
      # - products table: 20 products

- name: Post-Setup Validation
  hosts: localhost
  tasks:
    - name: Verify all services are running
      uri:
        url: "https://{{ hostvars['nginx_proxy'].public_dns }}/health"
        validate_certs: no
      register: health_check

    - name: Verify vulnerable endpoint exists
      uri:
        url: "https://{{ hostvars['nginx_proxy'].public_dns }}/api/orders/1"
        method: GET
        headers:
          Cookie: "SESSION={{ test_session_cookie }}"
        validate_certs: no
        status_code: 200
      register: vuln_check

    - name: Send lab ready notification
      uri:
        url: "https://gr-edu-api.com/labs/{{ lab_id }}/ready"
        method: POST
        body_format: json
        body:
          status: "ready"
          access_info: "{{ lab_access_info }}"
```

### 4.6 Lab Orchestrator - 환경 생성 (8단계)

**워크플로우**:

```python
class LabOrchestrator:
    async def create_lab(
        self,
        cve_id: str,
        archetype_id: int,
        user_id: int,
        ttl_hours: int = 2
    ) -> LabInstance:
        # 1. 인스턴스 ID 생성
        instance_id = f"lab-{generate_short_id()}"

        # 2. DB에 인스턴스 레코드 생성
        instance = await self.db.create_lab_instance(
            instance_id=instance_id,
            cve_id=cve_id,
            archetype_id=archetype_id,
            user_id=user_id,
            status='creating',
            expires_at=datetime.now() + timedelta(hours=ttl_hours)
        )

        try:
            # 3. IaC 코드 준비
            terraform_code = await self.iac_generator.generate_terraform(...)
            ansible_playbook = await self.iac_generator.generate_ansible(...)

            # 4. Terraform workspace 생성
            workspace = f"lab-{instance_id}"
            await self.terraform.create_workspace(workspace)
            await self.terraform.write_files(workspace, terraform_code)

            # 5. Terraform init
            await self.terraform.init(workspace)

            # 6. Terraform plan (검증)
            plan_result = await self.terraform.plan(workspace)
            await self.log_activity(instance_id, 'terraform_plan', plan_result)

            # 7. Terraform apply
            await self.db.update_status(instance_id, 'provisioning')
            apply_result = await self.terraform.apply(workspace)

            # 8. 출력값 추출
            outputs = await self.terraform.output(workspace)

            # 9. Ansible 인벤토리 생성
            inventory = self.generate_ansible_inventory(outputs)

            # 10. Ansible playbook 실행
            await self.db.update_status(instance_id, 'configuring')
            await self.ansible.run_playbook(
                playbook=ansible_playbook,
                inventory=inventory
            )

            # 11. 검증
            await self.db.update_status(instance_id, 'validating')
            validation_result = await self.validate_lab(instance_id, outputs)

            if not validation_result.success:
                raise LabValidationError(validation_result.errors)

            # 12. 접속 정보 저장
            access_info = {
                'lab_url': outputs['lab_url'],
                'attacker_credentials': outputs['attacker_account'],
                'victim_credentials': outputs['victim_accounts'],
                'guide_url': f"https://gr-edu.com/guides/{cve_id}"
            }

            await self.db.update_lab_instance(
                instance_id=instance_id,
                status='ready',
                ready_at=datetime.now(),
                access_info=access_info,
                terraform_state_path=f"s3://gr-lab-states/{workspace}/terraform.tfstate"
            )

            # 13. TTL 타이머 시작
            await self.schedule_auto_destroy(instance_id, ttl_hours)

            # 14. 사용자 알림
            await self.notification_service.send_lab_ready(
                user_id=user_id,
                instance_id=instance_id,
                access_info=access_info
            )

            return instance

        except Exception as e:
            # 에러 처리
            await self.db.update_status(instance_id, 'error', str(e))

            # Cleanup 시도
            try:
                await self.terraform.destroy(workspace)
            except:
                pass

            raise LabCreationError(f"Failed to create lab: {str(e)}")

    async def destroy_lab(self, instance_id: str):
        instance = await self.db.get_lab_instance(instance_id)

        # 1. 상태 업데이트
        await self.db.update_status(instance_id, 'stopping')

        # 2. Terraform destroy
        workspace = instance.terraform_workspace
        await self.terraform.destroy(workspace)

        # 3. Workspace 삭제
        await self.terraform.delete_workspace(workspace)

        # 4. 상태 업데이트
        await self.db.update_lab_instance(
            instance_id=instance_id,
            status='stopped',
            destroyed_at=datetime.now()
        )

        # 5. 통계 업데이트
        await self.update_statistics(instance_id)
```

---

## 5. 핵심 난이도 분석 및 해결 전략

### 5.1 난이도 높은 구간

#### ⚠️ 3단계: CVE 세세한 해석 (Difficulty: ★★★★★)

**문제**:
- CVE 설명이 애매하거나 불완전한 경우 많음
- PoC가 없거나 벤더 advisory가 부실한 경우
- 복잡한 취약점(로직 버그, Race Condition 등)의 구조화

**해결 전략**:
```yaml
Phase 1 (MVP):
  - 인기 CVE 50개를 수동으로 분석하여 DB에 저장
  - 템플릿 기반 + 일부 LLM 보조

Phase 2 (자동화):
  - LLM fine-tuning: CVE 설명 → 구조화 데이터
  - Human-in-the-loop: AI 분석 결과를 전문가가 검토

Phase 3 (완전 자동화):
  - Multi-source 분석: NVD + Vendor + PoC + 논문 + 블로그
  - Confidence score 기반 품질 관리
```

#### ⚠️ 7단계: IaC 코드 생성 (Difficulty: ★★★★☆)

**문제**:
- Terraform/Ansible 코드의 정확성 보장
- 클라우드별 차이 (AWS vs Azure vs GCP)
- 취약 설정과 정상 설정의 미묘한 차이

**해결 전략**:
```yaml
핵심 원칙: "LLM이 0에서 코드를 짜게 하지 말고, 템플릿 + 변수 주입"

Template Library 구축:
  - Archetype별 기본 템플릿 (10~20개)
  - Atom별 모듈 템플릿 (50~100개)
  - 검증된 템플릿만 사용

LLM 역할:
  - 템플릿 선택
  - 변수 값 결정
  - 조건부 리소스 추가/제거

Validation:
  - terraform validate
  - ansible-lint
  - 비용 추정 (terraform cost)
  - 보안 스캔 (tfsec, checkov)
```

### 5.2 성공 확률 높은 구간

#### ✅ 2, 4단계: 검색 및 매칭 (Difficulty: ★★☆☆☆)

**이유**:
- Rule-based 로직으로 충분히 구현 가능
- GR DB 설계가 잘 되어 있으면 쿼리 하나로 해결

#### ✅ 5, 6단계: 스토리/요소 생성 (Difficulty: ★★★☆☆)

**이유**:
- LLM이 잘하는 영역 (텍스트 생성)
- 정답이 하나가 아니라 "좋은 설명"만 만들면 됨
- 템플릿 + LLM 조합으로 안정적

#### ✅ 8단계: Orchestration (Difficulty: ★★★☆☆)

**이유**:
- DevOps 표준 기술 스택 (Terraform, Ansible, AWS SDK)
- 풍부한 레퍼런스와 라이브러리
- 에러 핸들링 패턴이 잘 정립되어 있음

---

## 6. GR Framework 통합 시너지

### 6.1 기존 자산 활용

**이미 있는 것을 200% 활용**:

```yaml
Layer/Zone 좌표계:
  → IaC 네트워크 토폴로지의 청사진
  → Security Group 규칙 자동 생성

Function Tags (280+):
  → 인프라 Atom 선택의 기준
  → 취약점 유형 분류

CVE-MITRE 매핑:
  → 공격 시나리오 생성
  → MITRE Technique별 실습 환경

Security Policies:
  → 취약 설정 vs 보안 설정 비교
  → Before/After 실습
```

### 6.2 새로운 가치 창출

**GR Framework만 있을 때**:
- 정적인 문서/분류체계
- 개념적 설명

**GR IaC Lab이 추가되면**:
- **동적인 실습 환경**
- **체험 가능한 교육**
- **실전 같은 훈련**

**예시**:
```
Before (GR Framework only):
  "PostgreSQL은 Layer 3, Zone 3에 위치하며,
   TLS 암호화(S3.1), 감사 로깅(M3.1) 정책이 적용됩니다."

After (+ GR IaC Lab):
  "PostgreSQL Layer 3, Zone 3 실습 환경을 생성했습니다.
   지금 바로 SSH 접속하여 TLS 설정을 확인하고,
   감사 로그가 어떻게 기록되는지 직접 보세요.

   실습 1: TLS 미적용 시 Wireshark로 평문 노출 확인
   실습 2: TLS 적용 후 암호화 통신 검증
   실습 3: 감사 로그로 의심스러운 쿼리 탐지"
```

### 6.3 비즈니스 모델

**GR Edu (교육 플랫폼)**:
```yaml
무료:
  - GR Framework 문서 열람
  - 기본 CVE 정보 조회
  - 커뮤니티 실습 가이드

유료 (월 $99):
  - CVE-to-Lab 자동 생성 (월 10회)
  - 실습 환경 2시간 유지
  - 기본 시나리오 (쇼핑몰, 기업)

프리미엄 (월 $299):
  - CVE-to-Lab 무제한
  - 실습 환경 8시간 유지
  - 모든 시나리오 (공장, 금융 등)
  - 팀 협업 기능

기업 (연 $5000+):
  - 프라이빗 클라우드 배포
  - 커스텀 시나리오 개발
  - 사내 CVE 실습 환경 구축
```

---

## 7. 로드맵

### Phase 1: MVP (3개월)

```yaml
Week 1-4: 기반 구축
  - GR DB 스키마 확장 (5개 테이블)
  - 인기 CVE 50개 수동 분석
  - Terraform/Ansible 템플릿 10개

Week 5-8: 파이프라인 구축
  - CVE Service API
  - Scenario Engine (rule-based)
  - IaC Generator (template-based)

Week 9-12: Lab Orchestrator
  - Terraform 실행 엔진
  - AWS 통합
  - TTL 관리

Deliverable:
  - 10개 CVE에 대한 자동 실습 환경 생성
  - 평균 생성 시간 5분
  - 수동 개입 필요
```

### Phase 2: 자동화 (3개월)

```yaml
Week 13-16: AI 통합
  - LLM 기반 CVE 분석
  - 시나리오 스토리 자동 생성
  - 코드 검증 자동화

Week 17-20: 확장
  - CVE 100개로 확대
  - Azure, GCP 지원
  - 시나리오 Archetype 20개

Week 21-24: 품질 개선
  - 사용자 피드백 반영
  - 생성 시간 단축 (3분 목표)
  - 안정성 개선

Deliverable:
  - 100개 CVE 자동 지원
  - Multi-cloud 지원
  - 평균 생성 시간 3분
```

### Phase 3: 상용화 (3개월)

```yaml
Week 25-28: 플랫폼화
  - Web UI 개발
  - 사용자 계정 시스템
  - 결제 시스템 연동

Week 29-32: 고도화
  - 팀 협업 기능
  - 실습 진도 추적
  - 인증서 발급

Week 33-36: 마케팅
  - 베타 테스터 모집 (100명)
  - 콘텐츠 제작 (블로그, 영상)
  - 정식 출시

Deliverable:
  - GR Edu 플랫폼 정식 오픈
  - 500+ CVE 지원
  - 월 사용자 1,000명 목표
```

---

## 8. 결론

### 핵심 성공 요인

1. ✅ **GR Framework 완벽 활용**: 기존 분류체계가 IaC 청사진이 됨
2. ✅ **템플릿 + AI 조합**: 안정성과 유연성의 균형
3. ✅ **명확한 난이도 인식**: 3, 7단계에 리소스 집중
4. ✅ **현실적인 로드맵**: MVP부터 상용화까지 단계적 접근

### 예상 효과

```yaml
교육 효과:
  - 이론 → 실습 전환율: 10% → 80%
  - 학습 완료율: 30% → 70%
  - 실무 적용 능력: 40% → 85%

비즈니스:
  - 유료 전환율: 5%
  - 월 매출 (1년 후): $50,000
  - 기업 고객 (1년 후): 10개사
```

### 최종 평가

**종합 점수**: ⭐⭐⭐⭐⭐ (5/5)

**이 시스템은 실현 가능하고, GR Framework와 완벽하게 통합되며, 큰 비즈니스 가치를 창출할 수 있습니다.**

**다음 단계**:
1. GR DB 스키마 확장 SQL 작성
2. 샘플 CVE (CVE-2025-64709) 전체 파이프라인 PoC
3. MVP 개발 착수

---

**문서 끝**
