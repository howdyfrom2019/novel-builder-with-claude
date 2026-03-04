# Novel Builder with Claude

> AI 기반 장기 연재 소설 관리 시스템 / AI-Powered Long-Form Serial Novel System

---

## 한국어

### 개요

**Novel Builder**는 Claude(AI)가 소설을 장기 연재할 수 있도록 설계된 구조화 집필 시스템입니다.

AI가 3화쯤에서 캐릭터를 잊거나 세계관을 어기는 문제는 "기억력 부족"이 아니라 **구조 부재** 때문입니다. 이 시스템은 Claude가 집필 전에 반드시 읽어야 할 **Canon(정본) 파일**과 **연속성 추적 파일**을 구조적으로 구성하여, AI가 기억에 의존하지 않고 **참조**만으로 일관된 세계관을 유지하게 합니다.

---

### 어떻게 작동하나요?

#### 핵심 원리: Canon First

```
집필 전 반드시 읽기 → 집필 → 집필 후 반드시 갱신
```

Claude는 매 화 집필 시 다음 순서로 파일을 읽고, 집필 후 연속성 파일을 업데이트합니다:

1. **`CLAUDE.md`** — 집필 헌법. 문체, 시점, 절대 금지 사항, 등장인물 말투 등 모든 규칙이 담긴 최상위 파일
2. **`canon/rules/`** — 세계 규칙. 이 세계에서 절대 어길 수 없는 물리법칙·사회 규칙
3. **`canon/characters/`** — 등장인물 프로필. 성격, 말투, 현재 알고 있는 정보, 관계 등 기록
4. **`plot/arc-master.md`** — 전체 아크 설계. 이번 화가 어느 아크에 해당하는지 확인
5. **`continuity/promise-tracker.md`** — 복선·약속 추적기. 깔아둔 복선이 무엇인지, 이행됐는지 관리
6. **`continuity/knowledge-map.md`** — 정보 비대칭 지도. 누가 무엇을 알고 무엇을 모르는지 기록
7. **직전 화 원고** — 직전 화의 문장과 흐름 파악

집필 완료 후에는 `continuity/` 파일들을 갱신하고, 품질 검증(연속성 체크 13항목)을 실행합니다.

#### 집필 파이프라인

```
[Prep]   canon/ + continuity/ 읽기
    ↓
[Plan]   이번 화 비트시트 작성 (5막 구조)
    ↓
[Write]  본문 집필
    ↓
[Check]  연속성 검증 (13항목)
    ↓
[Update] canon 갱신 + promise-tracker 업데이트
    ↓
[Review] 품질 채점 (목표: 85점+)
```

#### 에이전트 구성

| 에이전트             | 역할                  |
| -------------------- | --------------------- |
| `writer`             | 집필 파이프라인 총괄  |
| `continuity-checker` | 13개 항목 연속성 검증 |
| `canon-updater`      | canon 파일 자동 갱신  |
| `reviewer`           | 품질 채점 (7항목)     |

---

### 프로젝트 구조

```
novel-builder/
├── README.md
├── .claude/
│   └── skills/novel-builder/   ← Novel Builder 스킬 정의
│       ├── SKILL.md
│       ├── scripts/            ← 초기화 스크립트 등
│       └── references/         ← 캐릭터 템플릿, 에이전트 프롬프트 등
│
└── {소설-제목}/                 ← 각 소설은 독립 디렉토리
    ├── CLAUDE.md               ← 집필 헌법 (최우선 규칙)
    ├── stories/                ← 연재 원고
    │   ├── ep-001.md
    │   ├── ep-002.md
    │   └── ...
    ├── canon/                  ← 세계관 정본 (임의 변경 금지)
    │   ├── characters/         ← 등장인물 프로필
    │   ├── locations/          ← 장소 설정
    │   ├── timeline/           ← 시간순 사건 기록
    │   └── rules/              ← 세계 규칙
    ├── continuity/             ← 연속성 추적
    │   ├── promise-tracker.md  ← 복선·약속 이행 관리
    │   ├── knowledge-map.md    ← 캐릭터별 정보 보유 현황
    │   └── relationship-log.md ← 관계 변화 기록
    └── plot/                   ← 플롯 설계
        └── arc-master.md
```

---

### 현재 연재 중인 소설

#### 시간의 잔향 (殘響)

- **장르**: SF 미스터리 / 시간 여행 / 심리 드라마
- **모티프**: 슈타인즈게이트, 체크포인트(네이버 웹툰), 에반게리온, 솔라리스
- **연재 시작**: 2026-03-02
- **현재 화수**: 7화 완성
- **줄거리**: 컴공 학사 출신 이재윤이 AI 취업난을 겪다 NURI(국가양자연구소) 임상연구에 참여하게 되면서, 시간 도약의 '잔향'을 수신하는 존재가 된다. 미래를 알게 된 존재가 잃어버리는 것들에 관한 이야기.

#### 재능의 함정

- 현재 초기 설정 단계

---

### 새 소설 시작하기

```bash
# Novel Builder 스킬 참조
# .claude/skills/novel-builder/scripts/ 의 초기화 스크립트 사용

python3 .claude/skills/novel-builder/scripts/init_novel.py "소설제목" --path ./내소설 --genre 판타지
```

---

## English

### Overview

**Novel Builder** is a structured writing system that enables Claude (AI) to write and maintain long-form serial novels with consistency.

The reason AI tends to "forget" characters or break world-building rules around chapter 3 isn't a memory problem — it's a **structure problem**. This system solves that by providing Claude with a set of **Canon (authoritative source) files** and **continuity tracking files** that must be read before each writing session. Instead of relying on memory, Claude _references_ structured documentation to maintain a coherent, consistent world across any number of episodes.

---

### How It Works

#### Core Principle: Canon First

```
Read before writing → Write → Update after writing
```

Before writing each episode, Claude reads the following files in order. After writing, it updates the continuity files:

1. **`CLAUDE.md`** — The Writing Constitution. The top-level file containing all rules: prose style, POV restrictions, absolute prohibitions, and character voice guidelines.
2. **`canon/rules/`** — World Rules. Physical and social laws of this world that can never be violated.
3. **`canon/characters/`** — Character profiles including personality, speech patterns, current knowledge state, and relationships.
4. **`plot/arc-master.md`** — Full arc design plan, to understand where the current episode fits.
5. **`continuity/promise-tracker.md`** — Foreshadowing and promise tracker. Manages what has been seeded vs. resolved.
6. **`continuity/knowledge-map.md`** — Information asymmetry map. Records who knows what and who doesn't.
7. **Previous episode manuscript** — To ensure seamless flow and consistent tone.

After writing, continuity files are updated and a quality check (13-point continuity verification) is performed.

#### Writing Pipeline

```
[Prep]   Read canon/ + continuity/
    ↓
[Plan]   Write beat sheet for this episode (5-act structure)
    ↓
[Write]  Draft the episode
    ↓
[Check]  Continuity verification (13 checkpoints)
    ↓
[Update] Update canon files + promise-tracker
    ↓
[Review] Quality scoring (target: 85+ / 100)
```

#### Agent System

| Agent                | Role                                         |
| -------------------- | -------------------------------------------- |
| `writer`             | Orchestrates the full writing pipeline       |
| `continuity-checker` | Verifies 13 continuity checkpoints           |
| `canon-updater`      | Automatically updates canon files post-write |
| `reviewer`           | Quality scoring across 7 dimensions          |

---

### Project Structure

```
novel-builder/
├── README.md
├── .claude/
│   └── skills/novel-builder/   ← Novel Builder skill definition
│       ├── SKILL.md
│       ├── scripts/            ← Initialization scripts
│       └── references/         ← Character templates, agent prompts, etc.
│
└── {novel-title}/              ← Each novel is an isolated directory
    ├── CLAUDE.md               ← Writing constitution (top priority)
    ├── stories/                ← Published episodes
    │   ├── ep-001.md
    │   ├── ep-002.md
    │   └── ...
    ├── canon/                  ← Authoritative world-building (do not modify arbitrarily)
    │   ├── characters/         ← Character profiles
    │   ├── locations/          ← Location settings
    │   ├── timeline/           ← Chronological event log
    │   └── rules/              ← World rules
    ├── continuity/             ← Continuity tracking
    │   ├── promise-tracker.md  ← Foreshadowing and promise management
    │   ├── knowledge-map.md    ← Character knowledge state map
    │   └── relationship-log.md ← Relationship change log
    └── plot/                   ← Plot design
        └── arc-master.md
```

---

### Active Novels

#### 시간의 잔향 (_Echoes of Time_)

- **Genre**: SF Mystery / Time Travel / Psychological Drama
- **Inspired by**: Steins;Gate, Checkpoint (Naver Webtoon), Evangelion, Solaris
- **Started**: 2026-03-02
- **Episodes Published**: 7
- **Logline**: Lee Jae-yun, a computer science graduate struggling with AI-era unemployment, becomes entangled with NURI (National Quantum Research Institute) through a clinical trial — and finds himself receiving "echoes" of time leaps from alternate timelines. A story about what a person loses when they come to know the future.

#### 재능의 함정 (_The Talent Trap_)

- Currently in initial setup stage.

---

### Starting a New Novel

```bash
# Uses the Novel Builder skill
python3 .claude/skills/novel-builder/scripts/init_novel.py "My Novel" --path ./my-novel --genre fantasy
```

Then ask Claude:

```
Read [novel]/CLAUDE.md and all canon/ files first.
Write episode 1. Save to stories/ep-001.md and update continuity/ files.
```

---

### Design Philosophy

The key insight behind this system: **AI doesn't need better memory. It needs better architecture.**

By treating each novel as a self-contained knowledge base — with strict rules, character state tracking, and enforced reading order — Claude can maintain a living, consistent world across dozens of episodes without needing to hold the entire story in context at once.

This structure is also designed with future platform extensibility in mind:

- Each novel = isolated directory (portable)
- `canon/` files → migratable to a database
- Agents → separable into microservices
- `continuity/` files → convertible to event-sourcing patterns
