field = [[' ']*3 for i in range(3)]

def show():
    print()
    print('  | 0 | 1 | 2 |')
    print('---------------')
    for i, row in enumerate(field):
        row_str = f"{i} | {' | '.join(row)} | "
        print(row_str)
        print('---------------')

def ask():
    while True:

        coord = input('Ваш ход:').split()

        if len(coord) != 2:
            print('Введите две координаты через пробел!')
            continue

        x, y = coord

        if not(x.isdigit()) or not(y.isdigit()):
            print('Введите 2 числа!')
            continue

        x, y = int(x), int(y)

        if 0 <= x <= 2 and 0 <= y <= 2:
            if field[x][y] == ' ':
                return x, y
            else:
                print('Клетка занята!')
        else:
            print('Координаты вне диапазрна!')

def check_win_X():
    list_X = ['X', 'X', 'X']
    list_0 = ['0', '0', '0']
    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[i][j])
        if symbols == list_X:
            print('Выиграли Крестики')
        if symbols == list_0:
            print('Выиграли Нолики')
            return True

    for i in range(3):
        symbols = []
        for j in range(3):
            symbols.append(field[j][i])
        if symbols == list_X:
            print('Выиграли Крестики')
        if symbols == list_0:
            print('Выиграли Нолики')
            return True

    symbols = []
    for i in range(3):
        symbols.append(field[i][i])
    if symbols == list_X:
        print('Выиграли Крестики')
    if symbols == list_0:
        print('Выиграли Нолики')
        return True

    symbols = []
    for i in range(3):
        symbols.append(field[i][2-i])
    if symbols == list_X:
        print('Выиграли Крестики')
    if symbols == list_0:
        print('Выиграли Нолики')
        return True

    return False


num = 0

while True:
    num += 1

    show()

    if num % 2 == 1:
        print('Ходит Крестик')
    else:
        print('Ходит нолик')

    x, y = ask()

    if num % 2 == 1:
        field[x][y] = 'X'
    else:
        field[x][y] = '0'

    if check_win_X():
        break

    if num == 9:
        print('Ничья!')
        break