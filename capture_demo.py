"""Run the real CLI in an isolated copy and save actual subprocess output."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

root = Path(__file__).resolve().parent
demo = root / 'work' / ('demo-' + uuid.uuid4().hex)
demo.mkdir(parents=True, exist_ok=True)
for name in ['main.py', 'game.py', 'quiz.py', 'defaults.py', 'inputs.py', 'storage.py']:
    shutil.copyfile(root / name, demo / name)
state = demo / 'state.json'
if state.exists():
    state.replace(demo / 'previous-state.json')
sections = []
def run(title, entered):
    result = subprocess.run([sys.executable, '-X', 'utf8', str(demo / 'main.py')],
                            input=entered, text=True, encoding='utf-8', capture_output=True,
                            env={**os.environ, 'PYTHONUTF8': '1'}, cwd=root, timeout=15)
    assert result.returncode == 0, result.stderr
    sections.append(f'## {title}\n\n명령: `python -X utf8 main.py`\n\n입력 순서:\n```text\n{entered}\n```\n실제 stdout:\n```text\n{result.stdout}\n```\n종료 코드: {result.returncode}\n')
    return result.stdout

out = run('첫 실행 및 입력 검증', '\nabc\n9\n 4 \n5\n')
assert '아직 완료한 게임이 없습니다' in out
out = run('퀴즈 등록', '2\n\n재시작 후 데이터가 남는 저장 방식은?\nJSON 파일\n지역 변수\nprint\n주석\n0\nabc\n 1 \n5\n')
assert '퀴즈를 추가하고 저장' in out
out = run('목록 조회', '3\n5\n')
assert '등록 퀴즈: 6개' in out
out = run('플레이 및 최고점수', '1\n2\n1\n3\n4\n1\n1\n4\n5\n')
assert '100점' in out
out = run('재시작 후 퀴즈와 최고점수 유지', '3\n4\n5\n')
assert '최고 점수: 100점' in out and '등록 퀴즈: 6개' in out
out = run('EOF 안전 종료', '')
assert '안전하게 종료' in out
state.write_text('{broken', encoding='utf-8')
out = run('손상된 JSON 복구', '3\n5\n')
assert '정상 .bak 데이터로 자동 복구' in out
assert len(json.loads(state.read_text(encoding='utf-8'))['quizzes']) == 6
(root / 'docs' / 'cli-evidence.md').write_text('# 실제 CLI 실행 증거\n\n분리된 work/demo 복사본을 실행했다. 루트 state.json 경로 규칙도 동일하다.\n\n' + '\n'.join(sections), encoding='utf-8')
print('PASS: 7 actual CLI scenarios; all exit codes 0; persistence assertions passed.')
