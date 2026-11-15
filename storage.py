import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from quiz import Quiz


class StateStore:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else Path(__file__).resolve().parent / 'state.json'

    def _read(self, path):
            with path.open(encoding='utf-8') as stream:
                data = json.load(stream)
            if not isinstance(data, dict) or not isinstance(data.get('quizzes'), list):
                raise ValueError('잘못된 state 스키마')
            quizzes = [Quiz.from_dict(item) for item in data['quizzes']]
            best = data.get('best_score')
            if best is not None and (type(best) is not int or not 0 <= best <= 100):
                raise ValueError('잘못된 최고 점수')
            return quizzes, best

    def load(self):
        try:
            return self._read(self.path)
        except FileNotFoundError:
            print('저장 파일이 없습니다. 정상 백업을 확인합니다.')
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            print(f'저장 파일을 읽을 수 없어 복구를 시도합니다: {type(error).__name__}')
            try:
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                damaged = self.path.with_name(self.path.name + f'.corrupt-{stamp}')
                shutil.copy2(self.path, damaged)
                print(f'손상 원본 보존: {damaged.name}')
            except OSError:
                print('손상 파일 백업 실패: 원본 파일은 변경하지 않았습니다.')
        backup = self.path.with_name(self.path.name + '.bak')
        try:
            recovered = self._read(backup)
            print('정상 .bak 데이터로 자동 복구했습니다. 다음 저장 시 state.json을 복원합니다.')
            return recovered
        except (OSError, UnicodeError, ValueError, KeyError, TypeError):
            pass
        print('유효한 백업이 없어 기본 퀴즈를 사용합니다.')
        return None

    def save(self, quizzes, best_score):
        temporary = self.path.with_name(self.path.name + '.tmp')
        backup = self.path.with_name(self.path.name + '.bak')
        try:
            if self.path.exists():
                try:
                    self._read(self.path)
                except (OSError, UnicodeError, ValueError, KeyError, TypeError):
                    pass  # 손상된 현재 파일로 정상 백업을 덮어쓰지 않는다.
                else:
                    shutil.copy2(self.path, backup)
            with temporary.open('w', encoding='utf-8') as stream:
                json.dump({'quizzes': [q.to_dict() for q in quizzes], 'best_score': best_score},
                          stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            temporary.replace(self.path)
            return True
        except (OSError, UnicodeError) as error:
            print(f'저장하지 못했습니다. 메모리의 데이터는 유지됩니다: {type(error).__name__}')
            return False
