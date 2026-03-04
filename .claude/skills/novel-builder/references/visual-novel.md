# 비주얼 노벨 특화 가이드

## 목차
1. [VN과 소설의 구조적 차이](#vn과-소설의-구조적-차이)
2. [VN 프로젝트 구조](#vn-프로젝트-구조)
3. [시나리오 작성법](#시나리오-작성법)
4. [분기 설계 시스템](#분기-설계-시스템)
5. [Ren'Py 스크립트 패턴](#renpy-스크립트-패턴)
6. [연출 요소 관리](#연출-요소-관리)

---

## VN과 소설의 구조적 차이

| 요소 | 소설 | 비주얼 노벨 |
|-----|-----|-----------|
| 서술 시점 | 3인칭/1인칭 | 주로 1인칭 (플레이어 시점) |
| 지문 | 산문으로 통합 | 배경/스프라이트 지시로 분리 |
| 대화 | 인물별 행 구분 | speaker/text 분리 |
| 분기 | 없음 | 선택지 → 루트 분기 |
| 연출 | 문체로 표현 | BGM, SE, CG, 이펙트 |
| 시간 제어 | 없음 | 텍스트 속도, 페이드, 대기 |

---

## VN 프로젝트 구조

```
your-vn/
├── CLAUDE.md              ← VN 전용 집필 헌법
├── scripts/               ← Ren'Py 스크립트 파일
│   ├── ep-001.rpy
│   └── ep-002.rpy
├── canon/
│   ├── characters/        ← (소설과 동일 + 스프라이트 설정 추가)
│   ├── locations/         ← (소설과 동일 + 배경 이미지 매핑 추가)
│   ├── sprites/           ← 캐릭터 스프라이트 상태 정의
│   │   ├── [이름]-sprites.md
│   ├── bgm/               ← BGM/SE 매핑
│   │   └── music-map.md
│   ├── rules/
│   └── timeline/
├── continuity/            ← (소설과 동일)
├── plot/
│   ├── arc-01-outline.md
│   └── branches/          ← 분기 설계 문서
│       └── arc-01-branches.md
└── .claude/agents/
    ├── writer.md
    ├── vn-scripter.md
    ├── scene-director.md
    └── continuity-checker.md
```

---

## 시나리오 작성법

### VN용 CLAUDE.md 추가 규칙

```markdown
## VN 시나리오 규칙

### 시점
- 1인칭 주인공 시점 (주인공 이름을 직접 사용 금지 — 플레이어 투영)
- 나레이션 = 주인공의 내면 독백

### 지문 분리 원칙
소설의 지문을 VN 스크립트로 변환할 때:
- 배경 변화 → scene 명령
- 캐릭터 등장/퇴장 → show/hide 명령
- 감정 변화 → 스프라이트 표정 코드 변경
- 소리 → play music/sound 명령

### 텍스트 분량
- 씬당 대사: 20-40줄 (너무 길면 CG 전환 또는 선택지 삽입)
- 나레이션 블록: 최대 3-4문장 연속

### 금지
- 괄호 안 행동 묘사 대신 스프라이트 변경으로 표현
- "주인공은 생각했다" 사용 금지 (나레이션으로 직접 표현)
```

---

## 분기 설계 시스템

### branches/ 파일 구조

`plot/branches/arc-01-branches.md`:

```markdown
# 1아크 분기 설계

## 분기 트리

```
EP-003 선택지: "고백할까?"
├── YES → FLAG: confessed = True
│   └── EP-005: 연인 루트 시작
│       └── EP-008: 해피엔딩 A
└── NO  → FLAG: confessed = False
    └── EP-005: 우정 루트 유지
        └── EP-008: 노멀엔딩
```

## 플래그 목록

| 플래그명 | 타입 | 초기값 | 설정 시점 | 참조 시점 |
|--------|-----|------|---------|---------|
| confessed | bool | False | EP-003 | EP-005, EP-008 |
| trust_철수 | int (0-10) | 5 | EP-002~006 | EP-009 |

## 루트별 결말

| 루트 | 조건 | 결말 에피소드 |
|-----|-----|-----------|
| 해피엔딩 A | confessed=True AND trust_철수≥7 | EP-012 |
| 노멀엔딩 | confessed=False | EP-012-N |
| 배드엔딩 | trust_철수≤3 | EP-010-BAD |
```

### 분기 일관성 주의사항

continuity-checker에 VN 전용 항목 추가:
- 플래그 상태가 분기 이전/이후 씬과 일치하는가
- 선택지가 있는 씬에서 양쪽 루트 모두 캐릭터 일관성 유지되는가
- 엔딩 루트별로 약속/복선이 각각 회수되었는가

---

## Ren'Py 스크립트 패턴

### 기본 씬 구조

```renpy
label ep_001:
    scene bg_school_rooftop with fade
    play music "bgm_daily.ogg" fadein 1.0

    "방과 후의 옥상은 언제나 조용했다."

    show 지민 normal at center with dissolve
    "지민" "또 여기 있었네."

    show 지민 happy
    "지민" "오늘은 일찍 왔잖아."

    hide 지민 with dissolve
    "그 말이 마음에 걸렸다."

    jump ep_001_choice

label ep_001_choice:
    menu:
        "같이 있어도 돼?":
            $ trust_지민 += 1
            jump ep_001_a
        "그냥 혼자 있고 싶어서.":
            jump ep_001_b
```

### 감정 전달 패턴

```renpy
# 긴장감 연출
stop music fadeout 2.0
play sound "heartbeat.ogg" loop
show 지민 serious
"지민" "사실... 말해야 할 게 있어."
pause 1.5
show 지민 sad
"지민" "미안해."

# 반전 연출
with flash
scene bg_truth_revealed
play music "bgm_revelation.ogg"
"그 순간, 모든 것이 이해됐다."
```

### 플래그 기반 분기

```renpy
# 플래그 확인 분기
if confessed and trust_지민 >= 7:
    jump ending_happy_a
elif confessed:
    jump ending_normal_b
else:
    jump ending_normal_c
```

---

## 연출 요소 관리

### music-map.md 구조

```markdown
# BGM & SE 매핑

## BGM 목록

| 코드 | 파일명 | 분위기 | 주 사용 씬 |
|-----|-------|------|---------|
| bgm_daily | daily_life.ogg | 평온, 일상 | 학교, 일상 대화 |
| bgm_tension | tension_01.ogg | 긴박감 | 갈등, 추격 |
| bgm_sad | rain_and_memory.ogg | 슬픔 | 이별, 상실 |
| bgm_romance | soft_piano.ogg | 설렘 | 로맨틱 씬 |
| bgm_revelation | truth.ogg | 반전 | 비밀 공개 |

## SE 목록

| 코드 | 파일명 | 사용 상황 |
|-----|-------|---------|
| se_door | door_open.ogg | 문 열림/닫힘 |
| se_phone | phone_ring.ogg | 전화 수신 |
| se_heartbeat | heartbeat.ogg | 긴장/두근거림 |

## 씬 연출 규칙
- BGM 전환은 반드시 fadeout → fadein (갑작스러운 전환 금지)
- 감정 절정 씬에서는 SE만 사용하고 BGM 중단 허용
- 반전 씬: flash 이펙트 + bgm_revelation 즉시 시작
```

### VN 연출 연속성 체크리스트

집필 후 추가 확인 항목:
1. BGM이 씬 분위기와 일치하는가
2. 스프라이트 표정이 대사 감정과 맞는가
3. 분기 선택지 이후 양쪽 루트 모두 자연스럽게 이어지는가
4. 플래그 설정/참조가 올바른 순서인가
5. CG/배경 전환이 장소 설정과 일치하는가
