class Table:

    def __init__(self, size, first_player, second_player, next_step='X'):
        self.size, self.next_step = size, next_step
        self.first_player, self.second_player = first_player, second_player
        self.table = [[' ', ' ', ' '] for _ in range(size)]
        self.count_x = self.count_o = 0
        self.state = 'Game not finished'

    def set_new_table(self):
        self.table = [[' ', ' ', ' '] for _ in range(self.size)]

    def update_table(self, coordinate_x, coordinate_y):
        self.table[coordinate_x][coordinate_y] = self.next_step
        self.state = self._get_state()
        if self.next_step == 'X':
            self.count_x += 1
            self.next_step = 'O'
        else:
            self.count_o += 1
            self.next_step = 'X'

    def _get_state(self):
        if any((any(len(set(self.table[i])) == 1 and self.table[i][0] == self.next_step for i in range(self.size)),
                any(len(set(self.table[j][i] for j in range(self.size))) == 1 and self.table[0][i] == self.next_step for
                    i in range(self.size)),
                len(set(self.table[i][i] for i in range(self.size))) == 1 and self.table[0][0] == self.next_step,
                len(set(self.table[i][self.size - 1 - i] for i in range(self.size))) == 1 and self.table[0][
                    self.size - 1] == self.next_step)):
            return f'{self.next_step} wins'
        if self.count_x + self.count_o + 1 == self.size * self.size:
            return 'Draw'
        return 'Game not finished'
