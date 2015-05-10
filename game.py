
import random

BOARD_SIZE = 4

class Board():
    def __init__(self, copy_board=None):
        if copy_board is None:
            self.board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        else:
            self.board = [[copy_board[i][j] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    def countZeros(self):
        return sum([row.count(0) for row in self.board])

    def score(self):
        return sum([sum(row) for row in self.board])

    def addRandomTwo(self):
        num_zeros = self.countZeros()
        add_at_zero = 1 if num_zeros == 1 else random.randint(1, num_zeros)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    add_at_zero -= 1
                    if add_at_zero == 0:
                        self.board[i][j] = 2
                        return

    def printBoard(self):
        for row in self.board:
            print row
        print "\n\n"

class Game():
    def __init__(self):
        board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for i in range(3):
            self.addRandomTwo(board)
        self.allBoards = [board]

    def countZeros(self, board):
        return sum([row.count(0) for row in board])

    def currentScore(self):
        return sum([sum(row) for row in self.allBoards[-1]])

    def addRandomTwo(self, board):
        add_at_zero = 1 if self.countZeros(board) == 1 else random.randint(1, self.countZeros(board))
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    add_at_zero -= 1
                    if add_at_zero == 0:
                        board[i][j] = 2
                        return


    def moveSquareUp(self, board, i, j, collapsed_pos):
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

    def moveUp(self, board):
        # working through all the columns, work downwards, and push values up to their final destination
        old_board = [row[:] for row in board]
        for j in range(BOARD_SIZE):
            collapsed_pos = -1
            for i in range(1, BOARD_SIZE):
                collapsed_pos = self.moveSquareUp(board, i, j, collapsed_pos)
        return board != old_board

    def rotateClockwise(self, board):
        new_board = [[board[i][3 - j] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board[i][j] = new_board[i][j]

    def printBoard(self, board):
        for row in board:
            print row
        print "\n\n"

    def printCurrentBoard(self):
        self.printBoard(self.allBoards[-1])

    def makeMove(self, board, direction):
        # rotate direction times
        for i in range(direction):
            self.rotateClockwise(board)

        # move up
        move_worked = self.moveUp(board)

        # rotate (4 - direction) % 4 times
        for i in range((BOARD_SIZE - direction) % 4):
            self.rotateClockwise(board)

        return move_worked

    def moveIsValid(self, direction):
        board = [row[:] for row in self.allBoards[-1]]
        return self.makeMove(board, direction)

    def takeTurn(self, direction):
        if not self.moveIsValid(direction):
            return False

        board = [row[:] for row in self.allBoards[-1]]
        self.addRandomTwo(board)
        self.makeMove(board, direction)
        self.allBoards.append(board)

        print "I moved direction", direction
        my_game.printCurrentBoard()
        return True


class Player1():
    def move(self, board):
        return


if __name__ == "__main__":
    my_game = Game()

    for main_i in range(400):
        valid_move = my_game.takeTurn((main_i % 4))
        if not valid_move:
            print "YOU SUCK, SCORE ", my_game.currentScore()
            break

