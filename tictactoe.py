# write your code here

from Table import Table
from functions import get_command, print_table, game, GAME_TABLE_SIZE

if __name__ == '__main__':
    command, first_player, second_player = get_command()
    while command != 'exit':
        game_table = Table(GAME_TABLE_SIZE, first_player, second_player)
        print_table(game_table)
        game(game_table)
        command, first_player, second_player = get_command()
