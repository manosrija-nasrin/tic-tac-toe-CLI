import random
import math


class Player:
    def __init__(self, letter):
        # letter is X or O
        self.letter = letter

    # we want all players to get their next move given a game
    # returns the index corresponding to the move made
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Move (0 to 8): ')
            # now we are going to check if square contains a correct value
            # by casting it to integer, else we're going to say it's invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True     # it's a valid square, yay!
            except ValueError:
                print('Invalid square. Try again!')
        return val      # returns None if square is invalid


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # all squares are empty so randomly choose one
            square = random.choice(game.available_moves())
        else:
            # get square according to minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter    # yourself
        other_player = 'O' if player == 'X' else 'X'   # other player
        # first we check if previous move is winner
        # this is our base case for recursion
        if state.current_winner == other_player:
            # return position and score
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player
                else -1 * (state.num_empty_squares() + 1)
            }
        # if there is empty squares
        elif not state.empty_squares():     # no empty squares
            return {
                'position': None,
                'score': 0
            }
        # algorithm
        if player == max_player:
            best = {
                'position': None,
                'score': -math.inf  # each score should maximize (be larger)
            }
        else:
            best = {
                'position': None,
                'score': math.inf  # each score should minimize
            }
        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game making that move
            # now alternate players
            sim_score = self.minimax(state, other_player)

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move   # position we just moved to

            # step 4: update the dictionaries if necessary
            # i.e. if a score from a possible move beats current best score
            if player == max_player:    # maximize the max player
                if sim_score['score'] > best['score']:
                    best = sim_score    # replace best
            else:   # but minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score    # replace best

        return best
