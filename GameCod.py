import random


class Ship:

    def __init__(self, size, x, y, direction):
        self.__size = size
        self.__x = x
        self.__y = y
        self.__direction = direction
        self.placed = []

    restricted_area_player = set()
    restricted_area_bot = set()
    free_area_bot = set()
    free_area_player = set()

    def picker(self, player_or_bot):
        horizontally = self.__size if self.__direction == 'horizontally' else 1
        vertically = self.__size if self.__direction == 'vertically' else 1
        x = self.__x - 1
        y = self.__y - 1
        for i in range(x - (1 if x > 0 else 0), x + vertically + (1 if (x + vertically) < PlayingField.MAX_SIZE else 0)):
            for j in range(y - (1 if y > 0 else 0), y + horizontally + (1 if (y + horizontally) < PlayingField.MAX_SIZE else 0)):
                if player_or_bot == 'player':
                    Ship.restricted_area_player.add(str(i) + str(j))
                else:
                    Ship.restricted_area_bot.add(str(i) + str(j))
        if self.__direction == 'vertically':
            for i in range(x, x + self.__size):
                if player_or_bot == 'player':
                    player_field.massiv[i][y] = '■'
                else:
                    bot_field.massiv[i][y] = '■'
                temp_data = (i, y)
                self.placed.append(temp_data)
        else:
            for j in range(y, y + self.__size):
                if player_or_bot == 'player':
                    player_field.massiv[x][j] = '■'
                else:
                    bot_field.massiv[x][j] = '■'
                temp_data = (x, j)
                self.placed.append(temp_data)
        del self.__size
        del self.__x
        del self.__y
        del self.__direction
        Ship.free_area_bot = Ship.free_area_bot.difference(Ship.restricted_area_bot)
        Ship.free_area_player = Ship.free_area_player.difference(Ship.restricted_area_player)

    @staticmethod
    def del_used():
        del Ship.free_area_bot
        del Ship.restricted_area_bot
        del Ship.free_area_player
        del Ship.restricted_area_player


class PlayingField:

    def __init__(self):
        self.empty = 'O'
        self.whole = '■'
        self.crash = 'X'
        self.miss = 'T'
        self.shots = set()
        self.massiv = [
            [self.empty for j in range(6)] for i in range(6)
        ]

    MAX_SIZE = 6

  # 2 объекта - поля игрока и компа


def check_value_coord(x, y):
    if x > PlayingField.MAX_SIZE or x < 1:
        return ValueError
    if y > PlayingField.MAX_SIZE or y < 1:
        return ValueError


def show_playing_field():
    print()
    print('    Поле игрока ', 'Поле Бота', sep=PlayingField.MAX_SIZE * ' ')
    print('    ', end='')
    for i in range(PlayingField.MAX_SIZE):
        print(str(i + 1), end=' ')
    print('      ', end='')
    for i in range(PlayingField.MAX_SIZE):
        print(str(i + 1), end=' ')
    print()
    for number_line in range(6):
        print(number_line + 1, ' |', end='')
        print('|'.join(map(str, player_field.massiv[number_line])), '|', sep='', end='  ')
        print(number_line + 1, ' |', end='')
        # print('|'.join(map(str, bot_field.massiv[number_line])), '|', sep='', end='')

        for i in range(PlayingField.MAX_SIZE):
            if (str(number_line) + str(i)) in bot_field.shots:
                print(bot_field.massiv[number_line][i], '|', sep='', end='')
            else:
                print('O', '|', sep='', end='')
        print()
        number_line += 1


def step_player():
    global number_of_steps_player
    print('Выстрел игрока Player\n')
    while True:
        while True:
            try:
                x = int(input('Введите номер строки\n'))
                y = int(input('Введите номер столбца\n'))
                check_value_coord(x, y)
            except ValueError:
                print(text_error1)
                continue
            else:
                break
        try:
            if (str(x - 1) + str(y - 1)) in bot_field.shots:
                raise ValueError('Выстрел по этим координатам уже произведен')
            else:
                bot_field.shots.add((str(x - 1) + str(y - 1)))
                number_of_steps_player += 1
                if bot_field.massiv[x - 1][y - 1] == bot_field.empty:
                    bot_field.massiv[x - 1][y - 1] = bot_field.miss
                elif bot_field.massiv[x - 1][y - 1] == bot_field.whole:
                    bot_field.massiv[x - 1][y - 1] = bot_field.crash
                    show_playing_field()
                    print('Попадание\n'
                          'Продолжайте стрельбу')
                    if number_of_steps_player == PlayingField.MAX_SIZE**2:
                        break
                    continue
        except ValueError:
            print('Выстрел по этим координатам уже произведен\n')
            continue
        else:
            show_playing_field()
            break


def step_bot():
    global number_of_steps_bot
    print('Выстрел игрока Бот\n')
    while True:
        x = random.randrange(0, PlayingField.MAX_SIZE - 1, 1)
        y = random.randrange(0, PlayingField.MAX_SIZE - 1, 1)
        try:
            if (str(x) + str(y)) in player_field.shots:
                raise ValueError('Выстрел по этим координатам уже произведен')
            else:
                player_field.shots.add((str(x - 1) + str(y - 1)))
                number_of_steps_bot += 1
                if player_field.massiv[x - 1][y - 1] == bot_field.empty:
                    player_field.massiv[x - 1][y - 1] = bot_field.miss
                elif player_field.massiv[x - 1][y - 1] == bot_field.whole:
                    player_field.massiv[x - 1][y - 1] = bot_field.crash
                    print('Попадание')
                    if number_of_steps_bot == PlayingField.MAX_SIZE**2:
                        break
                    continue
        except ValueError:
            continue
        else:
            show_playing_field()
            break


def chek_the_victory(person):
    if person == 'player':
        for ship in list_of_ships_bot:
            for coord in ship.placed:
                if bot_field.massiv[coord[0]][coord[1]] != 'X':
                    return None
    else:
        for ship in list_of_ships_player:
            for coord in ship.placed:
                if player_field.massiv[coord[0]][coord[1]] != 'X':
                    return None
    return person


def cord_input(size_ship, player_or_bot):
    if player_or_bot == 'player':
        show_playing_field()
        print(f'\nРазмещение корабля размером {size_ship} клетки\n'
              f'Для расположения укажите координаты:\n')
    while True:
        try:
            if player_or_bot == 'player':
                x = int(input('Введите номер строки\n'))
                y = int(input('Введите номер столбца\n'))
                check_value_coord(x, y)
            else:
                b = random.choice(list(Ship.free_area_bot))
                x, y = int(b[0]) + 1, int(b[1]) + 1
            if player_or_bot == 'player':
                if str(x - 1) + str(y - 1) in Ship.restricted_area_player:
                    raise ValueError('\nВ этой клетке нельзя расположить корабль\n')
            else:
                if str(x - 1) + str(y - 1) in Ship.restricted_area_bot:
                    raise ValueError('\nВ этой клетке нельзя расположить корабль\n')
            if player_or_bot == 'player' and size_ship != 1:
                vertically_or_horizontally = input('размещение по горизонтали? (y/n)\n')
            else:
                vertically_or_horizontally = random.choice(['y', 'n'])
            if vertically_or_horizontally != 'y':
                if vertically_or_horizontally != 'n':
                    raise ValueError('Некорректный ввод данных')
                else:
                    a = 'vertically'
                    if (x + size_ship - 1) > PlayingField.MAX_SIZE:
                        raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
                    for i in range(x, x + size_ship):
                        if player_or_bot == 'player':
                            if str(i - 1) + str(y - 1) in Ship.restricted_area_player:
                                raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
                        else:
                            if str(i - 1) + str(y - 1) in Ship.restricted_area_bot:
                                raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
            else:
                a = 'horizontally'
                if (y + size_ship - 1) > PlayingField.MAX_SIZE:
                    raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
                for i in range(y, y + size_ship):
                    if player_or_bot == 'player':
                        if str(x - 1) + str(i - 1) in Ship.restricted_area_player:
                            raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
                    else:
                        if str(x - 1) + str(i - 1) in Ship.restricted_area_bot:
                            raise ValueError('\nВ этих координатах нельзя расположить корабль\n')
        except ValueError:
            if player_or_bot == 'player':
                print(text_error1)
                print('Коробли не должны косаться друг друга')
        else:
            return x, y, a


def set_up():
    global bot_field, player_field, list_of_ships_player, list_of_ships_bot
    list_variable_ship = [3, 2, 2, 1, 1, 1, 1]
    print('\nБот расставляет корабли')
    while True:
        bot_field = PlayingField()
        list_of_ships_bot = []
        Ship.restricted_area_bot = set()
        for i in range(PlayingField.MAX_SIZE):
            for j in range(PlayingField.MAX_SIZE):
                Ship.free_area_bot.add(str(i) + str(j))
        try:
            for i in range(7):
                if len(Ship.free_area_bot) < len(list_variable_ship) - i:
                    raise IndexError('ПРОВЕРИТЬ ТИП ОШИБКИ при неправильном заполнении поля')
                else:
                    # Ship(size, *(x, y, direction))
                    ships_now = Ship(list_variable_ship[i], *cord_input(list_variable_ship[i], 'bot'))
                    ships_now.picker('bot')
                    list_of_ships_bot.append(ships_now)
        except IndexError:
            print('Бот переставляет корабли\n')
            continue
        else:
            print('Игрок Бот расставил корабли')
            break
    print('Player расставляет корабли')
    while True:
        player_field = PlayingField()
        list_of_ships_player = []
        Ship.availible_area_player = set()
        Ship.restricted_area_player = set()
        for i in range(PlayingField.MAX_SIZE):
            for j in range(PlayingField.MAX_SIZE):
                Ship.availible_area_player.add(str(i) + str(j))
        try:
            for i in range(7):
                if len(Ship.availible_area_player) < len(list_variable_ship) - i:
                    raise IndexError('ПРОВЕРИТЬ ТИП ОШИБКИ при неправильном заполнении поля')
                else:
                    # Ship(size, *(x, y, direction))
                    ships_now = Ship(list_variable_ship[i], *cord_input(list_variable_ship[i], 'player'))
                    ships_now.picker('player')
                    list_of_ships_player.append(ships_now)
        except IndexError:
            print('\nПри данной расстановке невозможно расположить все корабли\n'
                  'Требуется произвести рсстановку заново\n')
            continue
        else:
            print('Игрок Player расставил корабли')
            break
    return bot_field, player_field, list_of_ships_player, list_of_ships_bot


text_error1 = 'Некорректный ввод данных.\n' \
              'Значение координат должно быть в диапазоне от 1 до 6\n'

bot_field, player_field, list_of_ships_player, list_of_ships_bot = set_up()
Ship.del_used()
number_of_steps_player = 0
number_of_steps_bot = 0

first_step = random.choice(['Player', 'Bot'])
print(f'Сегодня первым ходит {first_step}')
if first_step == 'Player':
    step_player()
while True:
    step_bot()
    victory = chek_the_victory('bot')
    if victory:
        break
    step_player()
    victory = chek_the_victory('player')
    if victory:
        break
print(f'Победил игрок {victory}')
