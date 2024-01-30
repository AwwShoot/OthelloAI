# This file and class is dedicated to handling the game Othello, its rules, and its board
class Othello:
    # I know I could write that programmatically and make it shorter
    # But this means a new board can be easily copy/pasted/modified for testing heuristics
    # 1 is black pieces, which go first, 2 is white pieces.
    board = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,2,1,0,0,0],
             [0,0,0,1,2,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]
    player = 1 #1 for black 2 for white
    turn = 1 # number of elapsed turns for ply
    def __init__(self, board, player, turn):
        self.board = board
        self.player = player
        self.turn = turn
    def clone(self):
        return Othello(self.board.copy(), self.player, self.turn)
    def play(self, x, y): #returns a new Othello object representing the new game state
        if self.board[x][y] != 0:
            print("Cannot place there, another piece already occupies the space.")
            return #return None if it's an illegal board state
        new_state = self.clone()
        new_state.board[x][y] = new_state.player
        # check lines for tiles to flip

        new_state.player = (new_state.player%2) + 1#Alternate the player

