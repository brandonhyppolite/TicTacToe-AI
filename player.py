import math
import random
 
class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square
    
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # we're going to check that this is a correct value by trying to cast
            # it to an integer, and if it's not, then we say its invalid
            # if that spot is not available on the board, we also say its invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if these are successful, then yay!
            except ValueError:
                print('Invalid square. Try again.')

        return val
    
class GeniusComputerPlayer(Player):
    def __init__(self, letter): # we want to keep track of this
        super().__init__(letter) # super() lets us access the parent class

    def get_move(self, game): # we want to pass in the game to make the recursion work
        if len(game.available_moves()) == 9: # if it's the first move
            square = random.choice(game.available_moves()) # randomly choose one
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position'] # we'll implement this later
        return square # return the position for whoever's turn it is
    
    def minimax(self, state, player):
        max_player = self.letter # yourself!
        other_player = 'O' if player == 'X' else 'X' # the other player...

        # first, we want to check if the previous move is a winner
        if state.current_winner == other_player: 
            # we should return position AND score because we need to keep track of the score
            # for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                                state.num_empty_squares() + 1)} # this is the score b/c it's the last one
        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0} # no score because it's a tie
        
        if player == max_player: # maximize our player
            best = {'position': None, 'score': -math.inf} # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf}  

        for possible_move in state.available_moves(): # look at all possible moves
            # step 1: make a move, try that spot
            state.make_move(possible_move, player) # make the move for the player we're iterating on
            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # now, we alternate players
            # step 3: undo the move
            state.board[possible_move] = ' ' # reset the board
            state.current_winner = None # reset the winner because we don't know yet
            sim_score['position'] = possible_move # otherwise this will get messed up from the recursion

            # step 4: update the dictionaries if necessary
            if player == max_player: # X is max player
                if sim_score['score'] > best['score']: # we want the largest score
                    best = sim_score   
            else: # but minimize the other player's score
                if sim_score['score'] < best['score']:
                    best = sim_score  

        return best # return the dictionary
    