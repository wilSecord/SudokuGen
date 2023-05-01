import random
import numpy as np

class cell:
    def __init__(self, r, c):
        self.options = [i for i in range(1, 10)]
        self.value = 0
        self.n_row = r
        self.n_column = c
        self.group = []
        self.row = []
        self.column = []

    def __repr__(self):
        return str(self.value)


    def collapse(self):
        choice = random.choice(self.options)

        for item in self.group:
            item.remove_choice(choice)
        for item in self.row:
            item.remove_choice(choice)
        for item in self.column:
            item.remove_choice(choice)
      
        self.value = choice


    def remove_choice(self, choice):
        if choice in self.options:
            self.options.remove(choice)

    def option_count(self):
        return len(self.options)


    def add_group(self, c):
        if c not in self.group:
            self.group.append(c)

        if self not in c.group:
            c.group.append(self)

    def add_row(self, c):
        if c not in self.row:
            self.row.append(c)

        if self not in c.row:
            c.row.append(self)


    def add_column(self, c):
        if c not in self.column:
            self.column.append(c)

        if self not in c.column:
            c.column.append(self)


def make_board():
    board = np.empty((9, 9), dtype=cell)
    for i in range(9):
        for j in range(9):
            board[i][j] = cell(i, j)

    for i in range(9):
        for item in board[i]:
            for other in board[i]:
                item.add_row(other)
    
    for i in range(9):
        for j in range(9):
            for k in range(9):
                board[i][j].add_column(board[k][j])
    

    for gi in range(3):
        for gj in range(3):
            for i in range(3):
                for j in range(3):
                    for ci in range(3):
                        for cj in range(3):
                            board[ci + 3 * gi][cj + 3 * gj].add_group(board[i + 3 * gi][j + 3 * gj])

    flat_board = board.flatten()
    un_collapsed = [item for item in flat_board] 
    while un_collapsed:
        flat_board = board.flatten()
        min_entropy = random.choice(un_collapsed)
        for item in flat_board:
            if item.option_count() < min_entropy.option_count():
                if item.value == 0:
                    min_entropy = item
        try:
            min_entropy.collapse()
        except:
            break
        un_collapsed.remove(min_entropy)

    return board
    

if __name__ == "__main__":
    board = make_board()
    while 0 in board.flatten():
        board = make_board()
    print(board)
