
import random

BOARD_SIZE = 4

class Board():
    def __init__(self):
        self.allBoards = []
        self.board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for i in range(3):
            self.addRandomTwo()

    def countZeros(self):
        return sum([row.count(0) for row in self.board])

    def addRandomTwo(self):
        add_at_zero = random.randint(1, self.countZeros())
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    add_at_zero -= 1
                    if add_at_zero == 0:
                        self.board[i][j] = 2
                        return


    def moveSquareUp(self, i, j, collapsed_pos):
        current_value = self.board[i][j]
        if current_value != 0:
            valid_pos = None
            for trial_pos in reversed(range(0, i)):
                if trial_pos >= collapsed_pos:
                    if self.board[trial_pos][j] == 0:
                        valid_pos = trial_pos
                    else:
                        if self.board[trial_pos][j] == current_value:
                            self.board[trial_pos][j] += self.board[i][j]
                            self.board[i][j] = 0
                            return trial_pos
                        else:
                            break
            if valid_pos is not None:
                self.board[valid_pos][j] = self.board[i][j]
                self.board[i][j] = 0
        return collapsed_pos

    def moveUp(self):
        print "Moving UP!!"
        for j in range(BOARD_SIZE):
            collapsed_pos = 0
            for i in range(1, BOARD_SIZE):
                # go left from i, until you hit the wall, or you find someone to squish into
                collapsed_pos = self.moveSquareUp(i, j, collapsed_pos)



    def printBoard(self):
        for row in self.board:
            print row
        print "\n\n"


if __name__ == "__main__":
    board = Board()
    board.printBoard()

    board.moveUp()
    board.printBoard()
