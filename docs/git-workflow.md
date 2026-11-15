# 실제 clone / push / pull 실습

## 커밋 단위: 작업을 나누는 기준

한 커밋은 **한 가지 목적을 설명하고 독립적으로 검토·되돌릴 수 있는 작업 단위**로 만든다. 파일 수나 코드 줄 수로 나누지 않는다.

- 메뉴, Quiz 모델, 기본 문제, 플레이, 퀴즈 추가, 목록, 점수, JSON 저장처럼 기능별로 나눈다.
- 같은 기능을 완성하는 코드·관련 테스트는 함께 포함할 수 있다. 서로 관계없는 기능이나 설정 변경은 별도 커밋으로 나눈다.
- 버그 수정은 원인과 해결이 드러나는 단위로 분리한다. 동작을 바꾸지 않는 구조 정리는 Refactor로 구분한다.
- 실행 방법·검증 증거·정책 문서는 목적별 Docs 커밋으로 기록한다. 단순히 커밋 개수를 늘리려고 빈 커밋이나 의미 없는 파일 변경을 만들지 않는다.
- 커밋 전 git diff로 변경 범위를 확인하고 관련 파일만 git add한다. 변경에 맞는 실행 확인이나 테스트 후 커밋한다. 기능 간 의존성이 있으면 앞선 기반 커밋부터 순서대로 기록한다.
- 브랜치 병합은 --no-ff merge로 남겨 실제 기능 작업과 통합 시점을 구분한다.

## 커밋 메시지 형식과 접두사 규칙

제목 형식은 **`접두사: 변경 내용 요약`**이다. 접두사 뒤에 콜론과 공백 한 칸을 넣는다. 요약은 무엇을 구현·수정했는지 구체적으로 쓰며, `수정`, `작업`, `최종`만 쓰는 모호한 제목은 피한다. 한국어·영어 모두 허용하되 한 제목의 표현을 일관되게 유지한다. 제목은 한 줄로 작성하고, 이유나 주의사항이 더 필요하면 빈 줄 뒤 본문에 기록한다.

| 접두사 | 사용 기준 | 이 저장소의 실제 예시 |
|---|---|---|
| `Feat:` | 사용자 기능·동작 추가 | `Feat: register validated questions and immediately persist additions` |
| `Fix:` | 잘못된 동작 수정 | `Fix: save complete state and exit cleanly on EOF or Ctrl+C` |
| `Refactor:` | 기능 의미를 유지하며 코드 책임·구조 개선 | `Refactor: separate QuizGame state and menu responsibilities` |
| `Test:` | 테스트·실행 검증 코드 추가 또는 개선 | `Test: cover CLI persistence invalid input recovery and safe interruption` |
| `Docs:` | README·증거·개발 정책 문서 변경 | `Docs: explain setup JSON schema design validation and Python fundamentals` |
| `Chore:` | 초기화·개발 설정 등 유지관리 | `Chore: initialize isolated mission2 quiz repository` |
| `Merge:` | 기능 브랜치의 명시적 통합 | `Merge: integrate quiz play feature into main` |

이 규칙은 현재 문서에 명시한 작성·검토 기준이며 commit-msg 훅 등으로 강제하지는 않는다. 실제 기능별 커밋과 병합은 [Git 그래프](git-graph.md), 원격 최신 이력은 [GitHub 커밋 목록](https://github.com/haiba-00/mission2-quiz/commits/main/)에서 확인할 수 있다.

## 실제 복제·동기화 명령과 출력

```text
> git clone https://github.com/haiba-00/mission2-quiz.git mission2-clone
Cloning into '<CLONE_DIRECTORY>'...
> git add README.md
> git commit -m "Docs: verify change from cloned checkout"
[main 710ad26] Docs: verify change from cloned checkout
 1 file changed, 2 insertions(+)
> git push
To https://github.com/haiba-00/mission2-quiz.git
   f4549d9..710ad26  main -> main
> git pull --ff-only
From https://github.com/haiba-00/mission2-quiz
   f4549d9..710ad26  main       -> origin/main
Updating f4549d9..710ad26
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
> README clone verification line
복제·동기화 실습: 별도 clone 작업 폴더에서 이 문장을 추가하고 원본에서 pull로 반영했다.
```
