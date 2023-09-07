#CAP4630
#Project 1
#Laura Waldron
#8/29/23

#1. Print a brief message explaining the purpose
#2. Display a TicTacToe board
#3. Prompt the user to play X
#4. Play O as the computer's move
#5. Repeat these two steps until winner or tie
#6. Ask if they want to replay the game
#Kylie's video, 35:55

import math
import random

#a class for the player
class Player:
    def __init__(self, choice):
        #choice is either X or O
        self.choice=choice
    #all players need to get their next move
    def next_move(self, game):
        pass

#a class for the computer
class Computer:
    def __init__(self,choice):
        #use the previous class to implement
        super().__init__(choice)
    def next_move(self,game):
        square = random.choice(game.available_moves())
        return square
class HPlayer(Player):
    def __init__(self,choice):
        super().__init__(choice)
    def next_move(self, game):
        valid_square = False
        val= None
        while not valid_square:
            square = input(self.letter + '\'s Turn, Input move 0-9:')
            #is this a correct way?
            #is is an integer? if not, invalid
            #spot not available, invalid
            try:
                val=int(square)
                if val not in game.avaliable_moves():
                    raise ValueError
                valid_square=True #successful
            except ValueError:
                print('I am sorry, this is not a good square to use.')
        return val


#a class to play a tictactoe game
class TicTacToe:
    def __init__(self):
        self.board=[' ' for _ in range(9)] #three by three board
        self.current_winner=None
    def print_board(self):
        #method to print the rows of the board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('|' + '|'.join(row) + '|')
    @staticmethod
    def print_board_nums():
        #0/1/2, what number corresponds to what box?
        number_board=[[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('|' + '|'.join(row) + '|')
    def available_moves(self):
        #return the set of empty numbers
        moves=[]
        for(i, spot) in enumerate(self.board):
            #['x','x','o']-->[(0,'x'), (1,'x'), (2,'x')]
            if spot==' ':
                moves.append(i)
        return moves
    def empty_squares(self):
        return ' ' in self.board
    def num_empty_squares(self):
        return self.board.count(' ')
    def move(self, square, letter):
        #make a valid move, assigning the square to x or o
        #return True.
        if self.board[square] == ' ':
            self.board[square]= letter
            if self.winner(self, letter):
                self.current_winner=letter
            return True
        else:
            return False
    def winner(self, square, letter):
        #win if three in a row!
        #rows
        r_index=square//3
        row=self.board[r_index*3: (r_index+1)*3]
        if all([spot==letter for spot in row]):
            return True
        #columns
        c_index=square%3
        column=[self.board[c_index+i*3] for i in range(3)]
        if all([spot==letter for spot in column]):
            return True
        #diagonals
        #even square numbers win diagonal
        if square%2==0:
            diag1=[self.board[i] for i in [0, 4,8]] #left to right
            if all([spot==letter for spot in diag1]):
                return True
            diag2=[self.board[i] for i in [2,4,6]] #right to left
            if all([spot==letter for spot in diag2]):
                return True
        #return false if no row, column, or diagonal matches
        return False

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()
    letter='X' #starting letter
    #iterate while empty squares
    #return the winner to break the loop
    while game.empty_squares():
        if letter =='O':
            square=o_player.get_move(game)
        else:
            square=x_player.get_move(game)
        #make a move
        if game.move(square, letter):
            if print_game:
                print(letter + f'moves to square {square}')
                game.print_board()
                print('') #empty line
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            #change to the other letter
            if letter == 'X':
                letter='O'
            else:
                letter= 'X'
            if print_game:
                print('It\'s a tie!!')
if __name__ == '__main__':
    x_player=Player('X')
    o_player=Computer('O')
    t=TicTacToe()
    play=(t, x_player, o_player, print_game=True)