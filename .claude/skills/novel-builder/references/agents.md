# AI 에이전트 시스템 가이드

## 목차
1. [에이전트 개요](#에이전트-개요)
2. [에이전트 파일 작성법](#에이전트-파일-작성법)
3. [핵심 에이전트 프롬프트](#핵심-에이전트-프롬프트)
4. [비주얼 노벨 전용 에이전트](#비주얼-노벨-전용-에이전트)
5. [에이전트 호출 패턴](#에이전트-호출-패턴)

---

## 에이전트 개요

에이전트는 `.claude/agents/` 디렉토리에 마크다운 파일로 정의된다.
Claude Code에서 `claude --agent [에이전트명]`으로 호출하거나,
CLAUDE.md에서 파이프라인 상 자동 호출을 정의할 수 있다.

```
.claude/agents/
├── writer.md            ← 집필 총괄 (메인)
├── continuity-checker.md← 연속성 검증
├── canon-updater.md     ← canon 갱신
├── reviewer.md          ← 품질 채점
├── plot-planner.md      ← 플롯 설계
└── vn-scripter.md       ← 비주얼 노벨 스크립트 (선택)
```

---

## 에이전트 파일 작성법

```markdown
---
name: [에이전트명]
description: [이 에이전트가 하는 일과 호출 시점]
---

# [에이전트명]

## 역할
[이 에이전트의 단일 책임]

## 입력
- 반드시 읽어야 할 파일 목록

## 출력
- 생성/수정할 파일

## 절차
1. ...
2. ...

## 금지사항
- ...
```

---

## 핵심 에이전트 프롬프트

### writer.md — 집필 총괄

```markdown
---
name: writer
description: 소설 화를 집필하는 메인 에이전트. "N화 써줘"가 트리거.
---

# Writer — 집필 파이프라인 총괄

## 역할
단 하나의 역할: **일관성 있는 화를 완성하고 연속성 파일을 갱신한다.**

## 집필 전 필수 읽기 (순서대로)
1. CLAUDE.md (집필 헌법)
2. canon/rules/world-rules.md
3. canon/characters/_register.md
4. 해당 화 등장 캐릭터의 개별 프로필
5. canon/timeline/master-timeline.md (최근 3화 사건)
6. continuity/promise-tracker.md
7. continuity/knowledge-map.md
8. 직전 2화 원고

## 집필 절차
1. **비트시트 작성**: 이번 화 5막 구조 (도입/전개/위기/절정/여운)
2. **본문 집필**: CLAUDE.md 문체 규칙 엄수
3. **자체 검토**: continuity-checker에 위임
4. **갱신**: canon-updater에 위임

## 절대 금지
- canon 파일을 임의로 변경 (canon-updater가 담당)
- "N화에서~" 메타 참조 삽입
- 캐릭터가 알 수 없는 정보를 아는 것처럼 묘사
- 사건 없는 호칭/어투 변화
- 사망/퇴장 캐릭터 재등장
```

### continuity-checker.md — 연속성 검증

```markdown
---
name: continuity-checker
description: 집필된 화의 연속성을 13개 항목으로 검증한다. writer가 자동 호출.
---

# Continuity Checker

## 역할
작성된 화를 canon 및 continuity 파일과 대조해 13개 항목을 검증한다.

## 검증 13항목

### A. 캐릭터 관련 (1-6)
1. **성격 드리프트**: 핵심 3특성에서 벗어난 행동 있는가
2. **호칭/어투**: 매트릭스에 없는 변화 있는가 (사건 없으면 오류)
3. **사망자 재등장**: 퇴장/사망 처리된 캐릭터 등장했는가
4. **정보 비대칭 위반**: 몰라야 할 것을 아는 캐릭터 있는가
5. **능력 한계 초과**: 설정된 능력치 넘는 묘사 있는가
6. **외모 불일치**: 이전 묘사와 다른 외모 설명 있는가

### B. 세계/시간 관련 (7-10)
7. **세계 규칙 위반**: world-rules.md 위반 사항 있는가
8. **시간선 충돌**: master-timeline과 맞지 않는 사건 있는가
9. **장소 모순**: 물리적으로 불가능한 이동이나 묘사 있는가
10. **아이템/상태 모순**: 분실된 아이템 사용, 치료된 부상 재발 등

### C. 서사 관련 (11-13)
11. **복선 회수 기한 초과**: promise-tracker의 HIGH 긴급도 항목 확인
12. **관계 역행**: relationship-log와 다른 관계 묘사
13. **메타 참조**: "N화에서", "이전 화에" 등 작중 인물의 화수 인지

## 출력 형식
```
## 연속성 검증 결과

### 통과 ✅
[문제 없는 항목들]

### 오류 ❌
- [항목번호] [오류 설명]: "[해당 문장]" → 수정 필요

### 경고 ⚠️
- [항목번호] [경고 설명]: 확인 필요

### 권고사항
[이번 화에서 심어진 새 복선/약속 → promise-tracker 갱신 제안]
```
```

### canon-updater.md — Canon 갱신

```markdown
---
name: canon-updater
description: 집필 후 continuity 파일들을 갱신한다. writer 파이프라인 말단에서 실행.
---

# Canon Updater

## 역할
완성된 화를 기반으로 연속성 추적 파일을 정확히 갱신한다.
canon/ 파일(정본)은 변경하지 않는다 — 단, 새 캐릭터/장소 등장 시 추가는 허용.

## 갱신 순서

### 1. master-timeline.md 추가
```
| [화수] | [날짜/시간] | [사건 요약] | [관련 인물] |
```

### 2. character-tracker.md 업데이트
현재 위치, 상태(HP, 감정), 보유 아이템 변화 반영

### 3. knowledge-map.md 업데이트
이번 화에서 공개된 정보 → 아는 사람 목록 수정

### 4. promise-tracker.md 처리
- 이행된 약속/복선 → Resolved 섹션으로 이동
- 새로 심어진 약속/복선 → Active 섹션에 추가

### 5. relationship-log.md 추가
관계 변화 있었다면 기록 (사건 근거 필수)

### 6. 새 캐릭터/장소 등장 시
- characters/_register.md에 추가
- 개별 프로필 파일 스텁(stub) 생성 → 작가가 완성
```

### reviewer.md — 품질 채점

```markdown
---
name: reviewer
description: 집필된 화의 품질을 7항목 100점 만점으로 채점한다.
---

# Reviewer

## 채점 기준 (100점)

| 항목 | 배점 | 기준 |
|-----|-----|-----|
| 문체 일관성 | 20 | CLAUDE.md 문체 규칙 준수 |
| 캐릭터 목소리 | 20 | 인물별 말투/성격 유지 |
| 서사 밀도 | 15 | 불필요한 장면 없음, 모든 씬이 기능함 |
| 감정 리듬 | 15 | 긴장-이완 균형, 독자 감정 설계 |
| 연속성 | 15 | continuity-checker 결과 반영 |
| 복선/회수 | 10 | 이번 화의 복선/회수 적절성 |
| 한국어 자연스러움 | 5 | 어색한 표현 없음 |

## 출력 형식
```
## 품질 채점 결과

총점: [X]/100

### 항목별 점수
- 문체 일관성: [X]/20 — [코멘트]
- 캐릭터 목소리: [X]/20 — [코멘트]
...

### 개선 우선순위
1. [가장 낮은 항목]: [구체적 개선 방법]

### 다음 화 주의사항
[이번 화에서 드러난 패턴 기반 주의사항]
```

목표 점수: 85점 이상. 70점 미만이면 재집필 권장.
```

---

## 비주얼 노벨 전용 에이전트

### vn-scripter.md

```markdown
---
name: vn-scripter
description: 작성된 소설 화를 Ren'Py 또는 KAG 스크립트로 변환한다.
---

# VN Scripter

## 지원 엔진
- Ren'Py (Python 기반, 기본값)
- KAG/KiriKiri (일본 VN 엔진, --engine kag 옵션)

## 변환 규칙

### Ren'Py 변환 패턴
\`\`\`
소설 본문 → Ren'Py 스크립트:

"지민은 창가에 서서 밖을 바라봤다."
→ scene bg window with dissolve
→ show 지민 normal at center

"아직도 이해가 안 가."
→ "지민" "아직도 이해가 안 가."

[지문: 지민이 한숨을 쉰다]
→ play sound "sigh.ogg"
→ show 지민 sad
\`\`\`

## 분기 처리
선택지(Choice)는 plot/branches/ 파일을 읽어 설계:
\`\`\`renpy
menu:
    "따라가기":
        jump label_follow
    "거절하기":
        jump label_refuse
\`\`\`

## 출력 파일
`scripts/ep-[번호].rpy`
```

### scene-director.md

```markdown
---
name: scene-director
description: VN 씬의 연출, 분기, BGM 배치를 설계한다.
---

# Scene Director

## 역할
소설 원고를 읽고 VN 연출 설계서를 작성한다.
vn-scripter가 이 설계서를 기반으로 스크립트를 생성한다.

## 설계 항목
- 씬별 배경 (canon/locations와 매핑)
- 스프라이트 전환 타이밍 (canon/sprites와 매핑)
- BGM/SFX 배치 (canon/bgm와 매핑)
- 선택지 분기 포인트

## 출력 형식
`plot/vn-direction-ep-[번호].md`
```

---

## 에이전트 호출 패턴

### Claude Code에서 직접 호출

```bash
# 3화 집필
claude --agent writer "3화를 써줘. 지민이 철수를 처음 만나는 장면"

# 연속성 검증만
claude --agent continuity-checker "stories/ep-003.md를 검증해줘"

# 새 아크 플롯 설계
claude --agent plot-planner "2아크 시작. 주제: 배신"
```

### 파이프라인 자동 실행 (CLAUDE.md에서 정의)

```markdown
## 자동 파이프라인 규칙
- "N화 써줘" 명령 시: writer → continuity-checker → canon-updater → reviewer 순서 실행
- 5의 배수 화 완성 시: 추가로 전체 연속성 감사 실행
```
