import time
from random import randint

def generate_game_space():                                          # функция генерации игрового поля
    game_space = [[0 for _ in range(5)] for _ in range(5)]
    return game_space

def unit_value():                                                   # функция оценки ячейки
    return randint(1, 100)

def find_best_move(game_space, current_player):
    units_value = []
    max_value = 0
    x, y = None, None
    for row in range(len(game_space)):
        for column in range(len(game_space[row])):
            if game_space[row][column] == 0:
                units_value.append((unit_value(), (row, column)))
    for unit in units_value:
        value, cords = unit
        if value > max_value:
            max_value = value
            x, y = cords

    return x, y, max_value

def main():
    game_space = generate_game_space()
    players = [1, 2]
    current_player_index = 0                                        # 0 - первый игрок (1), 1 - второй игрок (2)
    max_moves = 10                                                  # максимальное количество ходов у каждого игрока
    moves_count = 0
    
    while moves_count < max_moves:
        x, y, _ = find_best_move(game_space, players[current_player_index])
        if x is not None:
            game_space[x][y] = players[current_player_index]

        current_player_index = (current_player_index + 1) % len(players)    # смена игрока
        moves_count += 1

    for row in game_space:
        for column in row:
            print(column, end = ' ')
        print()

start = time.time()
main()
end = time.time()

print(f'Время работы программы: {end - start}')