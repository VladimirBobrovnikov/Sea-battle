from random import choice
from MyErrors import *


class Dot:
    def __init__(self, x, y, value='O', hid=False):
        self.x = x
        self.y = y
        self.value = value
        self.hid = hid

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Ship:
    def __init__(self, size, dot, direction):
        self.size = size
        self.dot = dot
        self.direction = direction
        self.number_of_life = size
        self.list_dots = []

    def dots(self):
        self.list_dots = []
        for i in range(self.size):
            if self.direction == 'horizontally':
                dot_now = Dot(self.dot.x, self.dot.y + i)
            else:
                dot_now = Dot(self.dot.x + i, self.dot.y)
            if 0 <= dot_now.x <= 5 and 0 <= dot_now.y <= 5:
                self.list_dots.append(dot_now)
            else:
                raise BoardOutException
        for dot in self.list_dots:
            dot.value = '■'
        return self.list_dots


class Board:
    # self_board Двумерный список, в котором хранятся состояния каждой из клеток
    # hid это bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага)
    # или нет (для своей доски).
    def __init__(self, hid, cls_, list_of_ships_places=None, list_ships_on_the_board_as_obj=None):
        self.self_board = [[Dot(i, j, hid=hid) for j in range(6)] for i in range(6)]
        if list_ships_on_the_board_as_obj:
            self.list_ships_on_the_board_as_obj = list_ships_on_the_board_as_obj
        else:
            self.list_ships_on_the_board_as_obj = []
        if list_of_ships_places:
            self.list_of_ships_places = list_of_ships_places
        else:
            self.list_of_ships_places = []
        self.hid = hid
        self.cls_ = cls_
        self.number_of_lives_ships = 7
        self.free_area = None
        self.clean_free_area()
        self.free_shots_point = self.free_area

    def clean_free_area(self):
        self.free_area = set()
        for i in range(6):
            for j in range(6):
                self.free_area.add(str(i) + str(j))

    def add_ship(self):  # который ставит корабль на доску (если ставить не получается, выбрасываем исключения)
        while True:
            print('Расстановка кораблей\n')
            list_variable_ship = [3, 2, 2, 1, 1, 1, 1]
            self.list_ships_on_the_board_as_obj = []
            self.clean_free_area()
            try:
                for i in range(7):
                    if len(self.free_area) < len(list_variable_ship) - i:
                        raise BoardOverFull
                    else:
                        while True:
                            try:
                                if self.cls_ is User:
                                    ship_place, ships_now = Game.placer_board(list_variable_ship[i])
                                elif self.cls_ is AI:
                                    ship_place, ships_now = Game.random_board(list_variable_ship[i], self.free_area)
                                for dot in ship_place:
                                    if str(dot.x) + str(dot.y) not in self.free_area:
                                        raise ErrorPlaced
                            except ErrorPlaced:
                                print('Корабли косаются друг друга\n'
                                      'Расположите корабль занова\n')
                            else:
                                self.list_of_ships_places.append(ship_place)
                                for dot in ship_place:
                                    self.self_board[dot.x][dot.y] = dot
                                    for i_ in range(dot.x - (1 if dot.x > 0 else 0), dot.x + (2 if dot.x < 6 else 1)):
                                        for j in range(dot.y - (1 if dot.y > 0 else 0), dot.y + (2 if dot.y < 6 else 1)):
                                            self.free_area.discard(str(i_) + str(j))
                                self.list_ships_on_the_board_as_obj.append(ships_now)
                                break
            except BoardOverFull:
                print('\nПри данной расстановке невозможно расположить все корабли\n'
                      'Требуется произвести рсстановку заново\n')
                self.self_board = [[Dot(i, j) for j in range(6)] for i in range(6)]
                continue
            else:
                if self.cls_ is User:
                    print('Игрок Player расставил корабли')
                elif self.cls_ is AI:
                    print('Игрок Bot расставил корабли')
                break

    def show_board(self):
        print('    ', end='')
        for i in range(6):
            print(str(i + 1), end=' ')
        print()
        number_line = 1
        for line in self.self_board:
            print(number_line, ' |', end='')
            for dot in line:
                print(dot.value, end='')
                print('|', end='')
            print()
            number_line += 1

    def shot(self, dot_shot):
        # делает выстрел по доске (если есть попытка выстрелить за пределы
        # и в использованную точку, нужно выбрасывать исключения)
        try:
            if str(dot_shot.x) + str(dot_shot.y) not in self.free_shots_point:
                raise RepietDot
            elif self.self_board[dot_shot.x][dot_shot.y].value == '■':
                print('Попадание')
                for ship in self.list_ships_on_the_board_as_obj:
                    for dot in ship.list_dots:
                        if dot == dot_shot:
                            ship.number_of_life -= 1
                            dot.value = '\033[35m{}\033[0m'.format('X')
                            dot.hid = True
                            self.free_shots_point.discard(str(dot_shot.x) + str(dot_shot.y))
                            if ship.number_of_life == 0:
                                for dot_ in ship.list_dots:
                                    dot_.value = '\033[31m{}\033[0m'.format('X')
                                self.number_of_lives_ships -= 1
                                print('Корабль уничтожен')
                                if self.number_of_lives_ships == 0:
                                    Game.LOOSER = self.cls_
                                    return False
                            return True
            elif self.self_board[dot_shot.x][dot_shot.y].value == 'O':
                print('Мимо')
                self.free_shots_point.discard(str(dot_shot.x) + str(dot_shot.y))
                self.self_board[dot_shot.x][dot_shot.y].value = '\033[31m{}\033[0m'.format('T')
                self.self_board[dot_shot.x][dot_shot.y].hid = True
        except RepietDot:
            print('Стрельба в эту точку уже произведена')
            return True


class Player:
    def __init__(self, my_board, not_my_board):
        self.my_board = my_board
        self.not_my_board = not_my_board

    def move(self, free_area_shots):
        # метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел
        # по вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся повторить ход.
        # Метод должен возвращать True, если этому игроку нужен повторный ход
        # (например, если он выстрелом подбил корабль).
        while True:
            print('Производится стрельба\n')
            dot_shot = self.ask_coord(free_area_shots)
            try:
                if self.not_my_board.shot(dot_shot):
                    return True
            except BoardOutException:
                print('Координаты вне игрового поля')
                continue
            else:
                break


class User(Player):
    def __init__(self, my_board, not_my_board):
        super().__init__(my_board, not_my_board)

    @staticmethod
    def ask_coord(free_area):

        print(f'Укажите координаты:')
        while True:
            try:
                x = int(input('Введите номер строки\n'))
                if x > 6 or x < 1:
                    raise BoardOutException
                y = int(input('Введите номер столбца\n'))
                if y > 6 or y < 1:
                    raise BoardOutException
            except BoardOutException:
                print('Координаты вне игрового поля')
                continue
            except ValueError:
                print('Некорректный ввод данных')
                continue
            else:
                dot_shot = Dot(x - 1, y - 1)
                return dot_shot

    @staticmethod
    def ask_direction(size):
        while True:
            try:
                if size != 1:
                    vertically_or_horizontally = input('размещение по горизонтали? (y/n)\n')
                else:
                    vertically_or_horizontally = 'y'
                if vertically_or_horizontally == 'y':
                    return 'horizontally'
                elif vertically_or_horizontally == 'n':
                    return 'vertically'
                else:
                    raise NotCorrectInput
            except NotCorrectInput:
                print('Для определения направления расположения корабля\n'
                      'укажите "y", если хотите расположить корабль по горизонтали\n'
                      'укажите "n", если хотите расположить корабль по вертикали\n')
                continue


class AI(Player):
    def __init__(self, my_board, not_my_board):
        super().__init__(my_board, not_my_board)

    @staticmethod
    def ask_coord(free_area):
        b = choice(list(free_area))
        x, y = int(b[0]), int(b[1])
        dot_shot = Dot(x, y)
        return dot_shot

    @staticmethod
    def ask_direction():
        vertically_or_horizontally = choice(['y', 'n'])
        if vertically_or_horizontally == 'y':
            return 'horizontally'
        else:
            return 'vertically'


class Game:
    def __init__(self):
        self.board_user = Board(False, User)
        self.board_ai = Board(True, AI)
        self.user = User(self.board_user, self.board_ai)
        self.ai = AI(self.board_ai, self.board_user)

    LOOSER = None

    @staticmethod
    def placer_board(size):
        while True:
            new_game.board_user.show_board()
            print(f'Установка коробля размером {size}')
            ships_now = Ship(size, User.ask_coord(new_game.board_user.free_area), User.ask_direction(size))
            try:
                ship_place = ships_now.dots()
            except BoardOutException:
                print('Размер корабля выходит за границы поля\n'
                      'Разместите корабль в других координатах')
                continue
            else:
                return ship_place, ships_now

    @staticmethod
    def random_board(size, free_area):
        while True:
            # Ship(size, dot_start, direction)
            print(f'Установка коробля размером {size}')
            ships_now = Ship(size, AI.ask_coord(free_area), AI.ask_direction())
            try:
                ship_place = ships_now.dots()
            except BoardOutException:
                # Размер корабля выходит за границы поля
                # Разместите корабль в других координатах
                continue
            else:
                return ship_place, ships_now

    def show_game_board(self):
        print()
        print('    Поле игрока ', 'Поле Бота', sep=6 * ' ')
        print('    ', end='')
        for i in range(6):
            print(str(i + 1), end=' ')
        print('      ', end='')
        for i in range(6):
            print(str(i + 1), end=' ')
        print()
        for number_line in range(6):
            print(number_line + 1, ' |', end='')
            for dot in self.board_user.self_board[number_line]:
                print(dot.value, end='')
                print('|', end='')
            print('  ', end='')
            print(number_line + 1, ' |', end='')
            for dot in self.board_ai.self_board[number_line]:
                if dot.hid:
                    print(dot.value, end='')
                else:
                    print('O', end='')
                print('|', end='')
            print()

    def greet(self):
        print("""
    Добро пожаловать в игру "Морской бой"
Игра заключается в имитации баталии двух флотилий.
Бой заключается в пошаговой стрельбе по полю противника.
Расположение кораблей противника заранее неизвестно, вам
предстоит проверять присутсвие кораблей в координатах поля стрельбой.
В случае попадания вам предоставляется возможность повторного выстрела
При промахе ход переходит противнику.
Перед игрой вам предстоит расставить свои корабли на игровом поле\n
Формат ввода координат:\nНомер строки:\n"Цифра от 1 до 6"\nНомер столбца:\n"Цифра от 1 до 6"
размещение по горизонтали? (y/n)\nБуква латинского алфавита: "y" если Да или "n" если Нет\n
Удачной игры!
         """)

    def loop(self):
        # метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode
        # для игроков и делаем проверку, сколько живых кораблей осталось на досках, чтобы
        # определить победу.
        while True:
            if not Game.LOOSER:
                new_game.show_game_board()
                while self.user.move(self.board_user.free_shots_point):
                    new_game.show_game_board()
            if not Game.LOOSER:
                while self.ai.move(self.board_ai.free_shots_point):
                    pass
            elif Game.LOOSER is AI:
                print('Победил игрок User')
                self.exit_game()
                break
            else:
                print('Победил игрок Bot')
                self.exit_game()
                break

    def start(self):
        self.greet()
        self.board_user.add_ship()
        self.board_ai.add_ship()
        self.loop()

    def exit_game(self):
        del self.board_user
        del self.board_ai
        del self.user
        del self.ai
        Game.LOOSER = None


while True:
    new_game = Game()
    new_game.start()
    if input('Вы желаете сыграть еще раз? (y/n)') != 'y':
        break
