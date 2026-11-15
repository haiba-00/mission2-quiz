import json
import os
from pathlib import Path
from quiz import Quiz


class StateStore:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else Path(__file__).resolve().parent / 'state.json'

    def load(self):
        try:
            with self.path.open(encoding='utf-8') as stream:
                data = json.load(stream)
            if not isinstance(data, dict) or not isinstance(data.get('quizzes'), list):
                raise ValueError('잘못된 state 스키마')
            quizzes = [Quiz.from_dict(item) for item in data['quizzes']]
            best = data.get('best_score')
            if best is not None and (type(best) is not int or not 0 <= best <= 100):
                raise ValueError('잘못된 최고 점수')
            return quizzes, best
        except FileNotFoundError:
            print('저장 파일이 없어 기본 퀴즈를 사용합니다.')
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            print(f'저장 파일을 읽을 수 없어 기본 데이터로 복구합니다: {type(error).__name__}')
        return None

    def save(self, quizzes, best_score):
        temporary = self.path.with_name(self.path.name + '.tmp')
        try:
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
