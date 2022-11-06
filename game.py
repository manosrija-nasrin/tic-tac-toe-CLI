from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer

import time


class TicTacToe:
    def __init__(self):
        # we will use a single list to rep 3x3 bpard
        self.board = [' ' for _ in range(9)]
        self.current_winner = None  # keep track of winner!

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)]
                        for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # return list of available squares
        # enumerate(['x', 'o', 'x'] -> [(1, 'x'), (2, 'o'), (3, 'x)])
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def winner(self, square, letter):
        # return True if letter is a winner after making a move in square
        # or False otherwise

        # winner if same letter in three cells in a row, column or diagonal
        # check rows first
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all(s == letter for s in row):
            return True

        # check columns
        col_ind = square % 3
        col = [self.board[col_ind + i*3] for i in range(3)]
        if all(s == letter for s in col):
            return True

        # check diagonals
        # only if the square is an even number
        # possible combinations in [0, 2, 4, 6, 8]
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0, 4, 8]]   # left diagonal
            if all(s == letter for s in diag1):
                return True
            diag2 = [self.board[i] for i in [2, 4, 6]]   # right diagonal
            if all(s == letter for s in diag2):
                return True

        # if all of these fail
        return False

    def make_move(self, square, letter):
        # if square is empty, assign letter to square and return True
        # else return False
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False


def play(game: TicTacToe, x_player: HumanPlayer, o_player: RandomComputerPlayer, print_game=True):
    # returns winner of the game (letter) or None for a tie
    if print_game:
        game.print_board_nums()

    letter = 'X'  # starting letter
    while game.empty_squares():
        if letter == 'X':
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)
        # check if move is valid
        if game.make_move(square, letter):
            if print_game:
                print(letter + f'makes a move to square {square}')
                game.print_board()
                print('')  # a blank line
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter   # if there is a winner, returns letter and exits
            letter = 'O' if letter == 'X' else 'X'  # switches player
        if print_game:
            time.sleep(1)   # tiny break

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    x_wins = 0
    o_wins = 0
    ties = 0
    for _ in range(50):
        x_player = RandomComputerPlayer('X')
        o_player = GeniusComputerPlayer('O')
        tic_tac_toe = TicTacToe()
        result = play(tic_tac_toe, x_player, o_player, False)
        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1
    print(
        f"After 50 iterations, we see {x_wins} X wins, {o_wins} O wins and {ties} ties.")
