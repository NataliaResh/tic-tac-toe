import random

from Table import Table

GAME_TABLE_SIZE = 3


def print_table(table: Table):
    print('---------')
    for i in range(table.size):
        print('|', end=' ')
        for j in range(table.size):
            print(table.table[i][j], end=' ')
        print('|')
    print('---------')


def _get_user_coordinates(game_table: Table):
    while True:
        try:
            coordinate_x, coordinate_y = map(int, input('Enter the coordinates: ').split())
            if not (1 <= coordinate_x <= 3 and 1 <= coordinate_y <= 3):
                print('Coordinates should be from 1 to 3!')
                continue
            if game_table.table[coordinate_x - 1][coordinate_y - 1] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            return coordinate_x - 1, coordinate_y - 1
        except ValueError:
            print('You should enter numbers!')


def _get_level_easy_coordinates(table: Table):
    while True:
        coordinate_x, coordinate_y = random.randint(1, 3), random.randint(1, 3)
        if not (1 <= coordinate_x <= 3 and 1 <= coordinate_y <= 3):
            continue
        if table.table[coordinate_x - 1][coordinate_y - 1] != ' ':
            continue
        return coordinate_x - 1, coordinate_y - 1


def _get_step_to_win(game_table, step):
    for i in range(GAME_TABLE_SIZE):
        if game_table.table[i].count(step) == 2 and game_table.table[i].count(' ') == 1:
            return i, game_table.table[i].index(' ')

    for j in range(GAME_TABLE_SIZE):
        column = [game_table.table[i][j] for i in range(GAME_TABLE_SIZE)]
        if column.count(step) == 2 and column.count(' ') == 1:
            return column.index(' '), j

    diagonal = [game_table.table[i][i] for i in range(GAME_TABLE_SIZE)]
    if diagonal.count(step) == 2 and diagonal.count(' ') == 1:
        return diagonal.index(' '), diagonal.index(' ')

    diagonal = [game_table.table[i][GAME_TABLE_SIZE - i - 1] for i in range(GAME_TABLE_SIZE)]
    if diagonal.count(step) == 2 and diagonal.count(' ') == 1:
        return diagonal.index(' '), GAME_TABLE_SIZE - diagonal.index(' ') - 1

    return None, None


def _get_level_medium_coordinates(game_table):
    step = game_table.next_step
    x, y = _get_step_to_win(game_table, step)
    if not (x is None or y is None):
        return x, y

    if step == 'X':
        step = 'O'
    else:
        step = 'X'
    x, y = _get_step_to_win(game_table, step)
    if not (x is None or y is None):
        return x, y

    return _get_level_easy_coordinates(game_table)


def empty_indexes(board):
    return list(filter(lambda x: x != 'X' and x != 'O', board))


def winning(board, player):
    return (board[0] == board[1] == board[2] == player) or \
           (board[3] == board[4] == board[5] == player) or \
           (board[6] == board[7] == board[8] == player) or \
           (board[0] == board[3] == board[6] == player) or \
           (board[1] == board[4] == board[7] == player) or \
           (board[2] == board[5] == board[8] == player) or \
           (board[0] == board[4] == board[8] == player) or \
           (board[2] == board[4] == board[6] == player)


def minimax(new_board, player, step):
    board = new_board.copy()
    avail_slots = empty_indexes(board)
    if step == 'X':
        second_step = 'O'
    else:
        second_step = 'X'
    if winning(board, second_step):
        return {'score': -10}
    if winning(board, step):
        return {'score': 10}
    if len(avail_slots) == 0:
        return {'score': 0}

    if player == 'X':
        second_player = 'O'
    else:
        second_player = 'X'
    moves = []

    for i in avail_slots:
        board[i] = player
        move = {'index': i, 'score': minimax(board, second_player, step)['score']}
        board[i] = i
        moves.append(move)

    best_move = 0
    if player == step:
        best_score = -10000
        for i in range(len(moves)):
            if best_score < moves[i]['score']:
                best_score = moves[i]['score']
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if best_score > moves[i]['score']:
                best_score = moves[i]['score']
                best_move = i

    return moves[best_move]


def _number_to_coordinate(number):
    number += 1
    remainder = number % 3
    if remainder == 0:
        remainder = 3

    return (number - remainder) // 3, remainder - 1


def _table_to_array(table):
    array = []
    count = 0
    for i in range(GAME_TABLE_SIZE):
        for j in range(GAME_TABLE_SIZE):
            if table[i][j] == ' ':
                array.append(count)
            else:
                array.append(table[i][j])
            count += 1
    return array


def _step_user(game_table):
    x, y = _get_user_coordinates(game_table)
    game_table.update_table(x, y)
    print_table(game_table)


def _step_easy(game_table):
    print('Making move level "easy"')
    x, y = _get_level_easy_coordinates(game_table)
    game_table.update_table(x, y)
    print_table(game_table)


def _step_medium(game_table):
    print('Making move level "medium"')
    x, y = _get_level_medium_coordinates(game_table)
    game_table.update_table(x, y)
    print_table(game_table)


def _step_hard(game_table):
    print('Making move level "hard"')
    array = _table_to_array(game_table.table)
    x, y = _number_to_coordinate(minimax(array, game_table.next_step, game_table.next_step)['index'])
    game_table.update_table(x, y)
    print_table(game_table)


_PLAYER_TO_FUNCTION = {
    'user': _step_user,
    'easy': _step_easy,
    'medium': _step_medium,
    'hard': _step_hard,
}


def get_command():
    while True:
        try:
            user_input = input('Input command: ')
            if user_input == 'exit':
                command, first_player, second_player = user_input, '', ''
            else:
                command, first_player, second_player = user_input.split()
                assert command == 'start' and first_player in _PLAYER_TO_FUNCTION and second_player in _PLAYER_TO_FUNCTION
            return command, first_player, second_player
        except ValueError:
            print('Bad parameters!')
        except AssertionError:
            print('Bad parameters!')


def _is_game_over(game_table):
    if game_table.state != 'Game not finished':
        print(game_table.state)
        print()
        return True
    return False


def game(game_table):
    while True:
        _PLAYER_TO_FUNCTION[game_table.first_player](game_table)
        if _is_game_over(game_table):
            break
        _PLAYER_TO_FUNCTION[game_table.second_player](game_table)
        if _is_game_over(game_table):
            break
