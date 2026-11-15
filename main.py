from game import QuizGame


def main():
    game = None
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print('\n입력이 중단되어 안전하게 종료합니다.')
    finally:
        if game is not None:
            if game.save():
                print('현재 데이터를 저장했습니다.')


if __name__ == '__main__':
    main()
