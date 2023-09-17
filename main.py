#Shamiah Bass, Brandon Hyppolite, Laura Waldron
#CAP4360 Fall 2023 Project 1
#Print a brief message explaining how the program works
#Display the board
#User plays as X while computer plays as O
#Play until someone wins
#Decide to play another round or quit

import math


class Person():
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            print('')
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
class Computer():
    def __init__(self, letter):
        #letter is x or o
        self.letter = letter

    def get_move(self, game):
        # get a random valid spot for our next move
        square = self.MiniMax(game, self.letter)['position'] # Call MinMax to find the best move
        return square
    #make a miniMax function here
    #Use the minimax algorithm to keep track of the game and the player
    def MiniMax(self, state, player, a=-math.inf, b=math.inf):
        maximum=self.letter
        other='X' if player== 'O' else 'O' #What is the player? The other is the opposite letter
        #return the position of the letter and the score
        if state.winner==other: #If the other person won, add one to their score
            return {'position': None, 'score': 1*(state.empty_squares()+1) if other == maximum else -1}
        elif not state.empty_squares():
            return{'position': None, 'score': 0}
        #Now let's save the best score for the alpha and beta
        if player== maximum:
            best={'position': None, 'score':-math.inf} #the maximized score
        else:
            best={'position': None, 'score': math.inf} #the minimized score
        #Find the best move using the recursive nature of minimax
        for test in state.available_moves():
            state.make_move(test, player) #make a move using this testing variable
            simulate = self.MiniMax(state, player, a, b)
            #Reset this spot to empty
            state.board[test] = ''
            state.winner = None
            simulate['position'] = test #set the position
            #Now let's find the best score
            if((simulate['score'] >best['score']) and (player==maximum)) or ((simulate['score']<best['score']) and (player !=maximum)):
                best=simulate #set the best score to the simulated score
                #use alpha-beta pruning
                if best['score']>=a:
                    a=best['score']
                elif best['score']>b:
                    b=best['score']
            if a>=b:
                break
        return best


class TicTacToe:
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
     print("It's a tie!")

if __name__ == '__main__':
    print("Welcome to the TicTacToe game!\n We will play a game between the user and the computer. Let's get started!")
    x_player = Person('X') #Here is our x player
    o_player = Computer('O') #Here is our o player
    t = TicTacToe()
    while True:
        playerInput= input("Would you like to play again? Enter 'Y' if yes, or 'N' if no")
        if(playerInput== 'N' or playerInput== 'n'):
            print("Thanks for playing our game!")
            break
        else:
            play(t, x_player, o_player, print_game=True)