def read_number(prompt, low, high):
    """공백, 빈 값, 숫자가 아닌 값, 범위 밖 입력을 처리한다."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print('숫자를 입력하세요. 빈 입력은 사용할 수 없습니다.')
            continue
        if low <= value <= high:
            return value
        print(f'{low}~{high} 사이의 숫자를 입력하세요.')


def read_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print('빈 내용은 등록할 수 없습니다.')
