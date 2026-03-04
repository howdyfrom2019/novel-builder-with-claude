---
name: novel-builder
description: |
  AI 기반 한국어 소설 및 비주얼 노벨 빌더 시스템. Canon(정본) 관리 구조를 통해 캐릭터 일관성, 세계관 연속성을 보장하며 장기 연재를 지원한다.

  Use when user wants to:
  - 새 소설/비주얼 노벨 프로젝트 시작 (init, 시작, 새 소설, 새 프로젝트)
  - 캐릭터 시트 작성 또는 관리 (캐릭터, character, 인물)
  - 새 화(에피소드) 집필 (N화 써줘, 다음 화, 새 에피소드)
  - 세계관/설정 문서 작성 (세계관, 설정, worldbuilding, canon)
  - 연속성 점검 (연속성, 캐릭터 일관성, 정합성, continuity)
  - 비주얼 노벨 시나리오 작성 (비주얼 노벨, visual novel, VN, 시나리오)
  - 소설 프로젝트 구조 설계 또는 확장
---

# Novel Builder — AI 소설 빌더 시스템

## 핵심 철학: Canon First

AI가 소설을 3화에서 무너뜨리는 이유는 기억력 부족이 아니라 **구조 부재**다.
Canon(정본) 파일을 집필 전에 읽히면 AI는 기억하려 애쓰지 않고 **참조**한다.

```
your-story/
├── CLAUDE.md              ← 집필 헌법 (모든 규칙 최상위)
├── stories/               ← 연재 원고 (chapters/)
│   └── ep-001.md
├── canon/                 ← 세계관 정본 (절대 임의 변경 금지)
│   ├── characters/        ← 캐릭터 프로필
│   ├── locations/         ← 장소 설정
│   ├── timeline/          ← 시간순 사건 기록
│   └── rules/             ← 세계 규칙 (마법, 사회, 물리 등)
├── continuity/            ← 연속성 추적
│   ├── promise-tracker.md ← 약속·복선 이행 관리
│   ├── knowledge-map.md   ← 캐릭터별 정보 보유 현황
│   └── relationship-log.md← 관계 변화 기록
├── plot/                  ← 플롯 설계
│   └── arc-01-outline.md
└── .claude/agents/        ← AI 에이전트 정의
```

---

## 빠른 시작

### 1. 새 프로젝트 초기화

```bash
python3 scripts/init_novel.py "소설제목" --path ./내소설 --genre 판타지 --type novel
# visual novel의 경우: --type vn
```

### 2. 설정 파일 작성 순서

1. `canon/rules/world-rules.md` — 세계 규칙 먼저
2. `canon/characters/` — 주인공 + 주요 인물 프로필
3. `canon/locations/` — 핵심 장소 설정
4. `CLAUDE.md` — 집필 헌법 완성 (문체, 시점, 금지사항)

### 3. 화 집필 명령어

```
[프로젝트의 CLAUDE.md와 canon/ 파일들을 먼저 읽어라]
1화를 써줘. ep-001.md로 저장하고, continuity/ 파일들을 갱신해라.
```

---

## Canon 파일 작성 가이드

### 캐릭터 시트 (canon/characters/)

→ 상세 템플릿: `references/character-template.md` 참조

핵심 필수 항목:
- 이름, 나이, 외모 (시각적 일관성)
- 성격 (3가지 핵심 특성 + 변화 불가 조건)
- 말투/어투 매트릭스 (누구에게 어떻게 말하는가)
- 정보 보유 현황 (무엇을 알고, 무엇을 모르는가)

### 세계 규칙 (canon/rules/)

→ 상세 가이드: `references/canon-system.md` 참조

규칙은 **위반 불가 항목**을 명시해야 한다:
```markdown
## 절대 규칙
- 마법은 대가(代價) 없이 사용 불가
- 죽은 자는 되살릴 수 없다 (단, X 조건 예외)
```

---

## 에이전트 시스템

→ 전체 에이전트 프롬프트: `references/agents.md` 참조

핵심 에이전트 구성:

| 에이전트 | 역할 | 자동 호출 시점 |
|---------|------|-------------|
| `writer` | 집필 파이프라인 총괄 | 사용자 요청 |
| `continuity-checker` | 13개 항목 연속성 검증 | 집필 후 |
| `canon-updater` | canon 파일 자동 갱신 | 집필 후 |
| `reviewer` | 품질 채점 (7항목) | 집필 후 |

비주얼 노벨 전용:

| 에이전트 | 역할 |
|---------|------|
| `vn-scripter` | KAG/Ren'Py 스크립트 변환 |
| `scene-director` | 연출/분기 설계 |

---

## 집필 파이프라인

```
[Prep]   canon/ + continuity/ 읽기
    ↓
[Plan]   이번 화 비트시트 작성 (5막 구조)
    ↓
[Write]  본문 집필
    ↓
[Check]  continuity-checker 실행 (13항목)
    ↓
[Update] canon 갱신 + promise-tracker 업데이트
    ↓
[Review] 품질 채점 (목표: 85점+)
```

---

## 비주얼 노벨 특화

→ 상세 가이드: `references/visual-novel.md` 참조

VN은 소설과 다른 추가 구조가 필요하다:
- `canon/sprites/` — 캐릭터 스프라이트 상태 정의
- `canon/bgm/` — 씬별 BGM 매핑
- `scripts/` — KAG 또는 Ren'Py 스크립트 파일
- 분기(Branch) 설계: `plot/branches/`

---

## 연속성 검증 체크리스트

5화마다 또는 아크 전환 시 반드시 실행:

```
[continuity/ 파일 전체와 이번 화를 읽어라]
다음 13항목을 체크하고 문제를 보고해라:
1. 캐릭터 성격 드리프트
2. 호칭/어투 변화 (사건 없는 변화 = 오류)
3. 죽거나 퇴장한 인물 재등장
4. 약속/복선 기한 초과
5. 장소 물리적 모순
6. 시간선 충돌
7. 캐릭터 정보 비대칭 위반 (몰라야 할 것을 아는 경우)
8. 세계 규칙 위반
9. 외모 묘사 불일치
10. 능력치/스탯 모순
11. 관계 설정 역행
12. 메타 참조 ("N화에서"처럼 작중 인물이 화수를 인지)
13. 시점 혼란
```

---

## 플랫폼 확장 고려사항

이 구조는 플랫폼으로 확장을 염두에 두고 설계됐다:
- 각 소설 프로젝트 = 독립 디렉토리 (격리)
- canon/은 데이터베이스 테이블로 마이그레이션 가능
- 에이전트 = 마이크로서비스로 분리 가능
- continuity/ 파일 = 이벤트 소싱 패턴으로 전환 가능

→ 확장 설계 가이드: `references/canon-system.md#platform` 참조
