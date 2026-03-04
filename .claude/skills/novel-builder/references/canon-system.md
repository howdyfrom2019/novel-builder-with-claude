# Canon 관리 시스템 완전 가이드

## 목차
1. [Canon이란](#canon이란)
2. [디렉토리 구조 상세](#디렉토리-구조-상세)
3. [캐논 파일 작성 규칙](#캐논-파일-작성-규칙)
4. [연속성 추적 시스템](#연속성-추적-시스템)
5. [갱신 워크플로우](#갱신-워크플로우)
6. [플랫폼 확장 가이드](#플랫폼-확장-가이드)

---

## Canon이란

블록체인의 Canonical Chain 개념과 동일하다. **무엇이 정본인지 합의된 기록**이 있고, 그 위에서 새 블록(화)이 쌓인다.

- canon/ 파일 = 확정된 사실, 임의 수정 불가
- stories/ 파일 = 새로 쌓이는 블록 (집필 후 canon에 반영)
- AI는 canon을 참조하되 절대 무단 변경하지 않는다

**Canon 우선순위:**
```
CLAUDE.md (최상위) > canon/rules/ > canon/characters/ > canon/locations/ > canon/timeline/
```

---

## 디렉토리 구조 상세

```
canon/
├── characters/
│   ├── protagonist.md        ← 주인공 (필수)
│   ├── [name]-profile.md     ← 등장인물별 파일
│   └── _register.md          ← 전체 캐릭터 등록부 (요약)
├── locations/
│   ├── [place]-detail.md     ← 장소 상세
│   └── _map.md               ← 세계지도/장소 목록
├── timeline/
│   ├── master-timeline.md    ← 전체 시간선
│   └── arc-01-events.md      ← 아크별 세부 사건
└── rules/
    ├── world-rules.md        ← 세계 물리/마법 법칙
    ├── social-rules.md       ← 사회 구조, 계급
    └── special-rules.md      ← 장르 특수 규칙

continuity/
├── promise-tracker.md        ← 약속/복선/플래그 추적
├── knowledge-map.md          ← 캐릭터별 정보 보유 현황
├── relationship-log.md       ← 관계 변화 이력
└── character-tracker.md      ← 현재 캐릭터 상태 (위치, HP 등)
```

---

## 캐논 파일 작성 규칙

### world-rules.md 필수 구조

```markdown
# 세계 규칙

## 절대 불변 법칙 (위반 불가)
- [규칙 1]: [설명] — 예외 없음
- [규칙 2]: [설명] — 예외: [조건]

## 마법/능력 체계
- 발동 조건:
- 한계/대가:
- 금지 사항:

## 사회/문화 규범
- 계급 구조:
- 금기:

## 시간/공간 물리
- [설정 세계의 시간 단위]:
- [특수 물리 법칙]:

## 정보 통제
- [이 세계에서 일반인이 모르는 것]:
```

### _register.md (캐릭터 등록부) 필수 구조

```markdown
# 캐릭터 등록부

| 이름 | 역할 | 등장 화수 | 생사 | 상세 파일 |
|-----|-----|---------|-----|---------|
| 홍길동 | 주인공 | 1화~ | 생존 | protagonist.md |
| 이몽룡 | 악당 | 3화~ | 생존 | mongryong-profile.md |
```

---

## 연속성 추적 시스템

### promise-tracker.md

약속, 복선, 미해결 플래그를 화수와 함께 기록.

```markdown
# 약속 & 복선 추적기

## 미이행 (Active)

| ID | 내용 | 심은 화 | 예상 회수 화 | 긴급도 |
|----|-----|--------|-----------|------|
| P001 | 주인공이 반드시 돌아오겠다 약속 | 3화 | 7화 이전 | HIGH |
| F001 | 붉은 달이 뜨면 복선 | 5화 | 미정 | LOW |

## 이행 완료 (Resolved)

| ID | 내용 | 심은 화 | 회수 화 |
|----|-----|--------|--------|
| P000 | 예시 약속 | 1화 | 2화 |
```

### knowledge-map.md

"누가 무엇을 아는가"를 정확히 기록. 비대칭 정보 오류를 방지.

```markdown
# 캐릭터 지식 지도

## 홍길동 (주인공)
- 아는 것: A의 정체, B의 배신
- 모르는 것: C가 살아있다는 사실, 자신의 진짜 출생

## 이몽룡
- 아는 것: 주인공의 약점
- 모르는 것: D 조직의 실체
```

### relationship-log.md

관계 변화는 반드시 **사건 근거**와 함께 기록.

```markdown
# 관계 변화 로그

| 화수 | 관계 | 변화 내용 | 근거 사건 |
|-----|-----|---------|---------|
| 5화 | 홍↔이 | 적대 → 잠정 휴전 | 공동의 적 등장 |
| 8화 | 홍↔김 | 동료 → 연인 암시 | 위기 상황 고백 |
```

---

## 갱신 워크플로우

### 화 집필 후 필수 갱신 순서

```
1. canon/timeline/master-timeline.md 에 이번 화 사건 추가
2. 등장한 캐릭터의 character-tracker.md 상태 업데이트
3. 새로 공개된 정보 → knowledge-map.md 업데이트
4. 이행된 약속 → promise-tracker.md에서 Resolved로 이동
5. 새 복선/약속 → promise-tracker.md Active에 추가
6. 관계 변화 있으면 → relationship-log.md 기록
```

### AI에게 갱신 지시하는 방법

```
[이번 화 ep-005.md와 continuity/ 파일들을 읽어라]
집필이 끝났으니 다음을 갱신해라:
1. promise-tracker.md - P002 이행됨으로 이동, F003 새로 추가
2. knowledge-map.md - 지민이 철수의 정체를 알게 됨
3. relationship-log.md - 5화 관계 변화 기록
4. master-timeline.md - 오늘 사건 추가
```

---

## 플랫폼 확장 가이드

현재 파일 기반 구조를 플랫폼으로 전환할 때의 매핑:

```
canon/characters/*.md     → DB: characters 테이블
canon/timeline/*.md       → DB: events 테이블 (이벤트 소싱)
continuity/knowledge-map  → DB: character_knowledge 테이블
continuity/promise-tracker→ DB: story_flags 테이블
.claude/agents/*.md       → API: /agents/{type}/invoke
stories/*.md              → Blob Storage + DB metadata

에이전트 시스템:
writer 에이전트        → POST /api/chapters/generate
continuity-checker     → POST /api/chapters/validate
canon-updater          → PATCH /api/canon/update
```

**확장 시 핵심 원칙:**
- Canon은 단일 진실 소스 (Single Source of Truth) 유지
- 에피소드 생성은 항상 canon snapshot을 입력으로 받는다
- 연속성 검증은 생성 파이프라인에서 분리된 서비스로 운영
