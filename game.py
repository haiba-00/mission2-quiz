from defaults import default_quizzes
from inputs import read_number


class QuizGame:
    def __init__(self):
        self.quizzes = default_quizzes()
        self.best_score = None

    def show_menu(self):
        print('\n작업실 퀴즈\n1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료')
        return read_number('선택: ', 1, 5)

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == 5:
                print('종료합니다.')
                return
            print('선택한 기능을 준비하고 있습니다.')
