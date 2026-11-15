from defaults import default_quizzes
from inputs import read_number, read_text
from storage import StateStore
from quiz import Quiz


class QuizGame:
    def __init__(self, state_path=None):
        self.quizzes = default_quizzes()
        self.best_score = None
        self.store = StateStore(state_path)
        loaded = self.store.load()
        if loaded is not None:
            self.quizzes, self.best_score = loaded
            print(f'저장 데이터 로드: 퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}')

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
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()

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
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print('새로운 최고 점수입니다!')
        self.save()
        return score


    def save(self):
        return self.store.save(self.quizzes, self.best_score)


    def add_quiz(self):
        print('새 퀴즈 등록')
        question = read_text('문제: ')
        choices = [read_text(f'선택지 {number}: ') for number in range(1, 5)]
        answer = read_number('정답 번호: ', 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print('퀴즈를 추가하고 저장했습니다.')
        else:
            print('퀴즈는 추가됐지만 파일 저장은 실패했습니다.')


    def list_quizzes(self):
        if not self.quizzes:
            print('등록된 퀴즈가 없습니다.')
            return
        print(f'등록 퀴즈: {len(self.quizzes)}개')
        for number, quiz in enumerate(self.quizzes, 1):
            print(f'[{number}] {quiz.question}')


    def show_score(self):
        if self.best_score is None:
            print('아직 완료한 게임이 없습니다.')
        else:
            print(f'최고 점수: {self.best_score}점')

