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
            if choice == 1:
                self.play()
            else:
                print('선택한 기능을 준비하고 있습니다.')

    def play(self):
        if not self.quizzes:
            print('퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
            return
        correct = 0
        for number, quiz in enumerate(self.quizzes, 1):
            print(f'\n[문제 {number}/{len(self.quizzes)}]')
            quiz.display()
            answer = read_number('정답 번호: ', 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print('정답입니다!')
            else:
                print(f'오답입니다. 정답: {quiz.answer}')
        score = round(correct / len(self.quizzes) * 100)
        print(f'결과: {len(self.quizzes)}문제 중 {correct}문제 정답 ({score}점)')
        return score

