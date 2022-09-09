from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot: {(self.x, self.y)}'


class Ship:
    def __init__(self, bow, lenght, orient):
        self.bow = bow
        self.length = lenght
        self.orient = orient
        self.lives = lenght

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            curr_x = self.bow.x
            curr_y = self.bow.y

            if self.orient == 0:
                curr_x += i

            elif self.orient == 1:
                curr_y += i

            ship_dots.append(Dot(curr_x, curr_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hide=False, size=10):
        self.hide = hide
        self.size = size

        self.count = 0

        self.field = [['0'] * size for _ in range(size)]

        self.busy = []

        self.ships = []

    def __str__(self):
        res = ""
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|'
        for i, row in enumerate(self.field):
            if i < 9:
                res += f'\n{i + 1} | ' + ' | '.join(row) + ' | '
            else:
                res += f'\n{i + 1}| ' + ' | '.join(row) + ' | '

        if self.hide:
            res = res.replace("■", "0")

        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):

        near = [(0, 0), (-1, 0), (1, 0),
                (0, -1), (0, 1), (-1, 1),
                (1, 1), (1, -1), (-1, -1)]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipExeption()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutExeption
        if d in self.busy:
            raise BoardUsedExeption

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExeption as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 9), randint(0, 9))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            coord = input('Введите координаты:').split()

            if len(coord) != 2:
                print('Введите 2 координаты!')
                continue

            x, y = coord

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите 2 числа!')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = False

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1]
        board = Board(size=self.size)
        attemps = 0
        for l in lens:
            while True:
                attemps += 1
                if attemps > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipExeption:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def print_board(self):
        print('Доска пользователя')
        print('-' * 20)
        print(self.us.board)
        print('Доска компьютера')
        print('-' * 20)
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.print_board()
            if num % 2 == 0:
                print('Ход игрока')
                repeat = self.us.move()
            else:
                print('Ход компьютера')
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_board()
                print('+' * 20)
                print('Игрок победил!')
                break

            if self.us.board.defeat():
                self.print_board()
                print('+' * 20)
                print('Компьютер победил!')
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


class BoardExeption(Exception):
    pass


class BoardOutExeption(BoardExeption):
    def __str__(self):
        return 'Вы выстрелили за доску!'


class BoardUsedExeption(BoardExeption):
    def __str__(self):
        return "Вы уже стреляли в эту точку!"


class BoardWrongShipExeption(BoardExeption):
    pass


g = Game()
g.start()