import math
import random
import time
 
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

class AIComputerPlayer(Player):
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
    

class TiCTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # we will use a single list to rep 3x3 board
        self.current_winner = None # keep track of winner!

    def print_board(self):
        # this is just getting the rows
        # [print(self.board[i*3:(i+1)*3]) for i in range(3)]
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')


    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        # if valid move, then make the move (assign square to letter)
        # then return true. if invalid, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # winner if 3 in a row anywhere.. we have to check all of these!
        # first let's check the row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        
        # check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # check diagonals
        # but only if the square is an even number (0, 2, 4, 6, 8)
        # these are the only moves possible to win a diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        # if all of these fail
        return False

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X' # starting letter
    # iterate while the game still has empty squares
    # (we don't have to worry about winner because we'll just return that
    # which breaks the loop)
    while game.empty_squares():
        # get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        # let's define a function to make a move!
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter
            
            # after we made our move, we need to alternate letters
            letter = 'O' if letter == 'X' else 'X' # switches player
        
        # take a break
        time.sleep(0.8)

    if print_game:
            print("It's a tie!")

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = AIComputerPlayer('O')
    t = TiCTacToe()
    playAgain = True
    while playAgain:
        play(t, x_player, o_player, print_game=True)
        time.sleep(1)
        playAgain = input("Do you want to play again? (y/n): ").lower() == 'y'
        t = TiCTacToe()
    print("Thanks for playing!")