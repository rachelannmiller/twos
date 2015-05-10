
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

    # Instead of making moves in all directions, we rotate the board and rotate back to simulate.
    def make_move(self, direction):
        for i in range(direction):
            self.rotate_clockwise()

        # move up
        move_worked = self.move_up()

        # rotate (4 - direction) % 4 times
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

    def move_square_up(self, board, i, j, collapsed_pos):
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

    def move_up(self, board):
        # working through all the columns, work downwards, and push values up to their final destination
        old_board = [row[:] for row in board]
        for j in range(BOARD_SIZE):
            collapsed_pos = -1
            for i in range(1, BOARD_SIZE):
                collapsed_pos = self.move_square_up(board, i, j, collapsed_pos)
        return board != old_board

    def rotate_clockwise(self, board):
        new_board = [[board[i][3 - j] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board[i][j] = new_board[i][j]

    def print_current_board(self):
        self.allBoards[-1].print_board()

    def make_move(self, board, direction):
        # rotate direction times
        for i in range(direction):
            self.rotate_clockwise(board)

        # move up
        move_worked = self.move_up(board)

        # rotate (4 - direction) % 4 times
        for i in range((BOARD_SIZE - direction) % 4):
            self.rotate_clockwise(board)

        return move_worked

    def is_move_valid(self, direction):
        board = Board(self.allBoards[-1])
        return self.make_move(board.board, direction)

    def take_turn(self, direction):
        if not self.is_move_valid(direction):
            return False

        board = Board(self.allBoards[-1])
        board.add_random_two()
        self.make_move(board.board, direction)
        self.allBoards.append(board)

        print "I moved direction", direction
        my_game.print_current_board()
        return True


class Player1():
    def move(self, board):
        return


if __name__ == "__main__":
    my_game = Game()

    for main_i in range(400):
        valid_move = my_game.take_turn((main_i % 4))
        if not valid_move:
            print "YOU SUCK, SCORE ", my_game.current_score()
            break

