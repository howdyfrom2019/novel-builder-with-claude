#!/usr/bin/env python3
"""
Novel Builder - 소설/비주얼 노벨 프로젝트 초기화 스크립트

Usage:
    python3 init_novel.py "소설 제목" --path ./내소설 --genre 판타지 --type novel
    python3 init_novel.py "내 VN" --path ./my-vn --genre 로맨스 --type vn
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ {path}")


def init_novel(title: str, output_path: Path, genre: str, novel_type: str):
    base = output_path

    print(f"\n📖 '{title}' 프로젝트 초기화 중...")
    print(f"   장르: {genre} | 타입: {'소설' if novel_type == 'novel' else '비주얼 노벨'}")
    print(f"   경로: {base.resolve()}\n")

    # ── CLAUDE.md (집필 헌법) ──────────────────────────────────────────────
    claude_md_novel = f"""# {title} — 집필 헌법

> 이 파일은 최상위 규칙이다. 모든 에이전트는 집필 전 반드시 읽는다.

## 기본 정보
- **제목**: {title}
- **장르**: {genre}
- **집필 시작**: {datetime.now().strftime('%Y-%m-%d')}

## 문체 규칙
- 시점: [3인칭 전지적 / 1인칭 주인공 — 선택]
- 문체: [간결체 / 서정체 / 구어체 — 선택]
- 화당 분량 목표: [3,000 / 5,000 / 8,000자 — 선택]
- 특이사항: [예: 장면 전환 시 *** 삽입]

## 집필 전 필수 읽기 (순서 엄수)
1. canon/rules/world-rules.md
2. canon/characters/_register.md
3. 이번 화 등장 캐릭터 개별 프로필
4. canon/timeline/master-timeline.md (최근 사건)
5. continuity/promise-tracker.md
6. continuity/knowledge-map.md
7. 직전 2화 원고

## 절대 금지 (위반 시 즉시 재집필)
- 캐릭터 성격 급변 (사건 선행 필수)
- "N화에서~" 메타 참조 삽입
- 사망/퇴장 처리된 캐릭터 재등장
- 알 수 없는 정보를 캐릭터가 아는 것처럼 묘사
- 사건 없는 호칭/어투 변화
- canon/ 파일 무단 변경 (canon-updater 에이전트만 허용)

## 파이프라인 자동 실행 규칙
- "N화 써줘" 명령: writer → continuity-checker → canon-updater → reviewer
- 5화 완성마다: 전체 연속성 감사 추가 실행
"""

    claude_md_vn = f"""# {title} — VN 집필 헌법

> 이 파일은 최상위 규칙이다. 모든 에이전트는 집필 전 반드시 읽는다.

## 기본 정보
- **제목**: {title}
- **장르**: {genre}
- **엔진**: Ren'Py
- **집필 시작**: {datetime.now().strftime('%Y-%m-%d')}

## VN 시나리오 규칙
- 시점: 1인칭 (플레이어 시점 — 주인공 이름 직접 사용 금지)
- 나레이션 = 주인공 내면 독백
- 씬당 대사 목표: 20-40줄

## 집필 전 필수 읽기
1. canon/rules/world-rules.md
2. canon/characters/_register.md + 스프라이트 설정
3. canon/bgm/music-map.md
4. continuity/promise-tracker.md
5. plot/branches/ (현재 아크 분기 설계)

## 절대 금지
- 괄호 안 행동 묘사 (스프라이트 변경으로 표현)
- "주인공은 생각했다" 사용 (나레이션으로 직접 표현)
- 플래그 순서 역행 (설정 전 참조)
- 사망 캐릭터 재등장

## 파이프라인
- "N화 써줘": writer → scene-director → vn-scripter → continuity-checker → canon-updater
"""

    claude_content = claude_md_vn if novel_type == "vn" else claude_md_novel
    write_file(base / "CLAUDE.md", claude_content)

    # ── canon/ ────────────────────────────────────────────────────────────
    write_file(base / "canon" / "characters" / "_register.md", f"""# 캐릭터 등록부

| 이름 | 역할 | 첫 등장 | 생사 | 프로필 파일 |
|-----|-----|--------|-----|----------|
| (주인공) | 주인공 | 1화 | 생존 | protagonist.md |

""")

    write_file(base / "canon" / "characters" / "protagonist.md", f"""# 주인공 프로필

## 기본 정보
- **이름**:
- **나이**:
- **성별**:
- **첫 등장**: 1화
- **상태**: 생존

## 외모
- **키/체형**:
- **머리**:
- **눈**:
- **특징**:

## 성격 핵심 3요소 (사건 없이 절대 변하지 않음)
1. **[특성1]**: [설명]
2. **[특성2]**: [설명]
3. **[특성3]**: [설명]

## 말투
- **기본**: 반말/존댓말
- **특징**:

## 목표
- **표면**:
- **숨겨진**:

## 정보 보유 현황
- **아는 것**:
- **모르는 것**:
""")

    write_file(base / "canon" / "locations" / "_map.md", f"""# 세계 지도 & 장소 목록

| 장소명 | 분류 | 첫 등장 | 상세 파일 |
|------|-----|--------|---------|
| (장소1) | - | 1화 | - |

""")

    write_file(base / "canon" / "timeline" / "master-timeline.md", f"""# 마스터 타임라인

> 모든 사건을 시간 순서대로 기록. 집필 후 canon-updater가 갱신.

| 화수 | 시간/날짜 | 사건 | 관련 인물 |
|-----|---------|-----|---------|
| 1화 | D+0 | 이야기 시작 | 주인공 |

""")

    write_file(base / "canon" / "rules" / "world-rules.md", f"""# 세계 규칙 — {title}

## 절대 불변 법칙 (위반 불가)
- [규칙1]: [설명]
- [규칙2]: [설명]

## 장르 특수 규칙 ({genre})
- [장르에 맞는 규칙]:

## 사회/문화 규범
- [계급, 관습, 금기]:

## 정보 통제
- [일반인이 모르는 것]:

""")

    # ── continuity/ ────────────────────────────────────────────────────────
    write_file(base / "continuity" / "promise-tracker.md", """# 약속 & 복선 추적기

## 미이행 (Active)

| ID | 내용 | 심은 화 | 예상 회수 | 긴급도 |
|----|-----|--------|---------|------|
| | | | | |

## 이행 완료 (Resolved)

| ID | 내용 | 심은 화 | 회수 화 |
|----|-----|--------|--------|
| | | | |
""")

    write_file(base / "continuity" / "knowledge-map.md", """# 캐릭터 지식 지도

> 누가 무엇을 알고, 무엇을 모르는가. 정보 비대칭 오류 방지용.

## [주인공]
- **아는 것**:
- **모르는 것**:

""")

    write_file(base / "continuity" / "relationship-log.md", """# 관계 변화 로그

> 변화는 반드시 사건 근거와 함께 기록.

| 화수 | 관계 | 변화 내용 | 근거 사건 |
|-----|-----|---------|---------|
| | | | |
""")

    write_file(base / "continuity" / "character-tracker.md", """# 캐릭터 현재 상태

> 최신 화 기준 상태. canon-updater가 집필 후 갱신.

## [주인공]
- **위치**:
- **감정 상태**:
- **보유 아이템**:
- **부상/상태이상**:
""")

    # ── plot/ ──────────────────────────────────────────────────────────────
    write_file(base / "plot" / "arc-01-outline.md", f"""# 1아크 플롯 개요

## 아크 주제
[이 아크에서 탐구하는 핵심 주제]

## 시작 조건
[1화 시작 상황]

## 핵심 사건 (비트시트)
1. **발단**: [사건]
2. **전개**: [사건]
3. **위기**: [사건]
4. **절정**: [사건]
5. **결말**: [사건]

## 이 아크에서 심을 복선
- F001:
- F002:

## 이 아크에서 회수할 복선
- (없음 — 1아크)

## 예상 화수
1화 ~ ?화
""")

    # ── stories/ ──────────────────────────────────────────────────────────
    write_file(base / "stories" / ".gitkeep", "")

    # ── VN 전용 추가 구조 ─────────────────────────────────────────────────
    if novel_type == "vn":
        write_file(base / "scripts" / ".gitkeep", "")
        write_file(base / "canon" / "sprites" / "_sprite-list.md", """# 스프라이트 목록

## [캐릭터명]
| 코드 | 표정 | 사용 조건 |
|-----|-----|---------|
| normal | 기본 | 일상 |
| happy | 웃음 | 긍정 |
| sad | 슬픔 | 이별/상실 |
| angry | 분노 | 갈등 |
| surprised | 놀람 | 반전 |
""")

        write_file(base / "canon" / "bgm" / "music-map.md", """# BGM & SE 맵

## BGM
| 코드 | 파일명 | 분위기 | 주 사용 씬 |
|-----|-------|------|---------|
| bgm_daily | daily.ogg | 일상 | 평온한 씬 |
| bgm_tension | tension.ogg | 긴박 | 갈등 씬 |
| bgm_sad | sad.ogg | 슬픔 | 이별 씬 |
| bgm_romance | romance.ogg | 설렘 | 로맨틱 씬 |

## SE
| 코드 | 파일명 | 용도 |
|-----|-------|-----|
| se_door | door.ogg | 문 |
| se_phone | phone.ogg | 전화 |
""")

        write_file(base / "plot" / "branches" / "arc-01-branches.md", """# 1아크 분기 설계

## 분기 트리
```
EP-? 선택지: "[선택지 내용]"
├── A → FLAG: xxx = True → EP-? 루트A
└── B → FLAG: xxx = False → EP-? 루트B
```

## 플래그 목록
| 플래그명 | 타입 | 초기값 | 설정 시점 | 참조 시점 |
|--------|-----|------|---------|---------|
| | | | | |

## 루트별 결말
| 루트 | 조건 | 결말 에피소드 |
|-----|-----|-----------|
| | | |
""")

    # ── .claude/agents/ ───────────────────────────────────────────────────
    agents_dir = base / ".claude" / "agents"

    write_file(agents_dir / "writer.md", f"""---
name: writer
description: {title}의 화를 집필하는 메인 에이전트. "N화 써줘" 명령에 트리거.
---

# Writer

## 집필 전 필수 읽기 (순서 엄수)
1. CLAUDE.md
2. canon/rules/world-rules.md
3. canon/characters/_register.md
4. 이번 화 등장 캐릭터 프로필
5. canon/timeline/master-timeline.md (최근 3화)
6. continuity/promise-tracker.md
7. continuity/knowledge-map.md
8. 직전 2화 원고 (있다면)

## 절차
1. 이번 화 5막 비트시트 작성 (도입/전개/위기/절정/여운)
2. 본문 집필 (CLAUDE.md 문체 규칙 엄수)
3. continuity-checker 호출
4. canon-updater 호출
5. reviewer 호출

## 절대 금지
- canon 파일 무단 변경
- 메타 참조 ("N화에서~")
- 사망자 재등장
- 정보 비대칭 위반
""")

    write_file(agents_dir / "continuity-checker.md", f"""---
name: continuity-checker
description: {title}의 화를 13개 항목으로 연속성 검증. writer가 자동 호출.
---

# Continuity Checker

## 검증 파일
- canon/characters/ (등장 캐릭터 프로필)
- canon/rules/world-rules.md
- canon/timeline/master-timeline.md
- continuity/ (전체)

## 13개 검증 항목
1. 성격 드리프트
2. 호칭/어투 무단 변화
3. 사망자 재등장
4. 정보 비대칭 위반
5. 능력 한계 초과
6. 외모 불일치
7. 세계 규칙 위반
8. 시간선 충돌
9. 장소 모순
10. 아이템/상태 모순
11. 복선 회수 기한 초과 (promise-tracker HIGH 항목)
12. 관계 역행
13. 메타 참조

## 출력
```
## 연속성 검증

통과 ✅ / 오류 ❌ / 경고 ⚠️
[항목별 결과]
```
""")

    write_file(agents_dir / "canon-updater.md", f"""---
name: canon-updater
description: {title} 집필 후 continuity 파일 갱신. canon 정본은 변경하지 않음.
---

# Canon Updater

## 갱신 순서
1. canon/timeline/master-timeline.md — 이번 화 사건 추가
2. continuity/character-tracker.md — 상태 업데이트
3. continuity/knowledge-map.md — 공개된 정보 반영
4. continuity/promise-tracker.md — 이행/신규 처리
5. continuity/relationship-log.md — 관계 변화 기록
6. 신규 캐릭터/장소 → _register.md 추가 + 스텁 생성
""")

    write_file(agents_dir / "reviewer.md", f"""---
name: reviewer
description: {title} 집필 화를 100점 기준 7항목 채점. 85점 미만 재집필 권장.
---

# Reviewer

## 채점 항목 (100점)
- 문체 일관성: /20
- 캐릭터 목소리: /20
- 서사 밀도: /15
- 감정 리듬: /15
- 연속성: /15
- 복선/회수: /10
- 한국어 자연스러움: /5

## 출력
```
총점: X/100
항목별: [...]
개선 우선순위: [...]
```
""")

    if novel_type == "vn":
        write_file(agents_dir / "vn-scripter.md", f"""---
name: vn-scripter
description: {title}의 화 원고를 Ren'Py 스크립트로 변환.
---

# VN Scripter

## 변환 규칙
- 나레이션 → `"나레이션 텍스트"`
- 대사 → `"캐릭터명" "대사"`
- 장소 변화 → `scene bg_[코드] with [전환효과]`
- 감정 변화 → `show [캐릭터] [표정코드]`
- BGM → canon/bgm/music-map.md 참조

## 출력
`scripts/ep-[번호].rpy`
""")

        write_file(agents_dir / "scene-director.md", f"""---
name: scene-director
description: {title} 화의 연출, 분기, BGM 배치 설계서 작성.
---

# Scene Director

## 설계 항목
- 씬별 배경 (canon/locations 매핑)
- 스프라이트 전환 타이밍 (canon/sprites 매핑)
- BGM/SE 배치 (canon/bgm 매핑)
- 선택지 분기 포인트 (plot/branches 참조)

## 출력
`plot/vn-direction-ep-[번호].md`
""")

    print(f"\n✅ '{title}' 프로젝트가 성공적으로 생성됐습니다!")
    print(f"\n📋 다음 단계:")
    print(f"  1. CLAUDE.md — 문체·시점·목표 분량 채우기")
    print(f"  2. canon/rules/world-rules.md — 세계 규칙 작성")
    print(f"  3. canon/characters/protagonist.md — 주인공 프로필 완성")
    print(f"  4. plot/arc-01-outline.md — 1아크 플롯 설계")
    print(f"\n✍️  준비 완료 후 Claude Code에서:")
    print(f'  "1화를 써줘. [핵심 씬 설명]"')
    if novel_type == "vn":
        print(f"\n🎮 VN 전용 추가 설정:")
        print(f"  - canon/sprites/ — 캐릭터별 스프라이트 상태 정의")
        print(f"  - canon/bgm/music-map.md — BGM 파일 목록 채우기")
        print(f"  - plot/branches/ — 분기 설계")


def main():
    parser = argparse.ArgumentParser(
        description="소설/비주얼 노벨 프로젝트 초기화"
    )
    parser.add_argument("title", help="소설 제목")
    parser.add_argument("--path", default=".", help="생성할 디렉토리 경로")
    parser.add_argument("--genre", default="판타지", help="장르 (예: 판타지, 로맨스, SF)")
    parser.add_argument(
        "--type",
        choices=["novel", "vn"],
        default="novel",
        help="프로젝트 타입 (novel: 소설, vn: 비주얼 노벨)",
    )

    args = parser.parse_args()

    # 제목을 기반으로 디렉토리명 생성
    title_slug = args.title.replace(" ", "-").lower()
    if args.path == ".":
        output_path = Path(f"./{title_slug}")
    else:
        output_path = Path(args.path)

    init_novel(
        title=args.title,
        output_path=output_path,
        genre=args.genre,
        novel_type=args.type,
    )


if __name__ == "__main__":
    main()
