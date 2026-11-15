from quiz import Quiz


def default_quizzes():
    return [
        Quiz('Python에서 정수를 나타내는 자료형은?', ['str', 'int', 'list', 'dict'], 2),
        Quiz('Git에서 현재 변경을 이력으로 기록하는 명령은?', ['commit', 'clone', 'pull', 'status'], 1),
        Quiz('Docker에서 호스트 포트와 컨테이너 포트를 연결하는 옵션은?', ['--name', '-v', '-p', '--rm'], 3),
        Quiz('JSON에서 키와 값으로 구성된 객체에 대응하는 Python 자료형은?', ['bool', 'str', 'list', 'dict'], 4),
        Quiz('파일을 UTF-8로 읽을 때 open에 지정하는 인자는?', ['encoding', 'answer', 'branch', 'port'], 1),
    ]
