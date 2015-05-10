
import random

BOARD_SIZE = 4

class Board():
    def __init__(self, copy_board=None):
        if copy_board is None:
            self.board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        else:
            self.board = [row[:] for row in copy_board.board]

    def count_zeros(self):
        return sum([row.count(0) for row in self.board])

    def score(self):
        return sum([sum(row) for row in self.board])

    def add_random_two(self):
        num_zeros = self.count_zeros()
        add_at_zero = 1 if num_zeros == 1 else random.randint(1, num_zeros)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    add_at_zero -= 1
                    if add_at_zero == 0:
                        self.board[i][j] = 2
                        return

    def rotate_clockwise(self):
        new_board = [[self.board[i][3 - j] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.board = [row[:] for row in new_board]

    def move_square_up(self, i, j, collapsed_pos):
        board = self.board
        current_value = board[i][j]
        if current_value != 0:
            valid_pos = None
            for trial_pos in reversed(range(0, i)):
                if trial_pos >= collapsed_pos:
                    if board[trial_pos][j] == 0:
                        valid_pos = trial_pos
                    else:
                        if board[trial_pos][j] == current_value:
                            board[trial_pos][j] += board[i][j]
                            board[i][j] = 0
                            return trial_pos
                        else:
                            break
            if valid_pos is not None:
                board[valid_pos][j] = board[i][j]
                board[i][j] = 0
        return collapsed_pos

    def move_up(self):
        # working through all the columns, work downwards, and push values up to their final destination
        old_board = [row[:] for row in self.board]
        for j in range(BOARD_SIZE):
            collapsed_pos = -1
            for i in range(1, BOARD_SIZE):
                collapsed_pos = self.move_square_up(i, j, collapsed_pos)
        return self.board != old_board

    # Instead of making moves in all directions, we rotate the board and rotate back to simulate.
    def make_move(self, direction):
        for i in range(direction):
            self.rotate_clockwise()
        move_worked = self.move_up()
        for i in range((BOARD_SIZE - direction) % 4):
            self.rotate_clockwise()
        return move_worked

    def print_board(self):
        for row in self.board:
            print row
        print "\n\n"

class Game():
    def __init__(self):
        board = Board()
        for i in range(3):
            board.add_random_two()
        self.allBoards = [board]

    def current_score(self):
        return self.allBoards[-1].score()

    def print_current_board(self):
        self.allBoards[-1].print_board()

    def is_move_valid(self, direction):
        current_board_copy = Board(self.allBoards[-1])
        return current_board_copy.make_move(direction)

    def take_turn(self, direction):
        if not self.is_move_valid(direction):
            return False

        board = Board(self.allBoards[-1])
        board.add_random_two()
        board.make_move(direction)
        self.allBoards.append(board)

        print "I moved direction", direction
        my_game.print_current_board()
        return True

    def current_board(self):
        return self.allBoards[-1]


class Player1():
    def move(self, game):
        current_score = game.current_board().score()
        return (current_score / 2) % 4


if __name__ == "__main__":
    my_game = Game()
    player = Player1()

    while True:
        valid_move = my_game.take_turn(player.move(my_game))
        if not valid_move:
            print "Invalid move - Game over!"
            print "Score: ", my_game.current_score()
            break

