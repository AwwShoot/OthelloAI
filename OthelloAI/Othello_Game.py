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
        total_flips = 0
        opponent =  (new_state.player%2) + 1 #easy way to flip player val

        # Check below
        possible_flips = 0
        position = [x, y]
        while position[1] < 8 and new_state.board[position[0]][position[1] + 1] == opponent:
            possible_flips += 1
            position[1] += 1
        if position[1] != 8: # found an allied tile before the edge
            total_flips += possible_flips
            for i in range(y, position[1]): #Flip the pieces
                new_state.board[x][i] = new_state.player

        # Check below and to the right
        possible_flips = 0
        position = [x, y]
        while position[1] < 8 and position[0] < 8 and new_state.board[position[0]+ 1][position[1] + 1] == opponent:
            possible_flips += 1
            position[1] += 1
            position[0] += 1
        if position[1] < 8 and position[0] < 8:  # found an allied tile before the edge
            total_flips += possible_flips
            for i, j in range(x, position[0]), range(y, position[1]): #Flip the pieces
                new_state.board[i][j] = new_state.player

        # Check to the right
        possible_flips = 0
        position = [x, y]
        while position[0] < 8 and new_state.board[position[0] + 1][position[1] ] == opponent:
            possible_flips += 1
            position[0] += 1
        if position[0] < 8:  # found an allied tile before the edge
            total_flips += possible_flips
            for i in range(x, position[0]):  # Flip the pieces
                new_state.board[i][y] = new_state.player

        # Check above and to the right
        possible_flips = 0
        position = [x, y]
        while position[1] > -1 and position[0] < 8 and new_state.board[position[0] + 1][position[1] - 1] == opponent :
            possible_flips += 1
            position[1] -= 1
            position[0] += 1
        if position[1] > -1 and position[0] < 8:  # found an allied tile before the edge
            total_flips += possible_flips
            for i, j in range(x, position[0]), range(position[1], y):  # Flip the pieces
                new_state.board[i][j] = new_state.player

        # Check above
        possible_flips = 0
        position = [x, y]
        while position[1] > -1 and new_state.board[position[0]][position[1] - 1] == opponent:
            possible_flips += 1
            position[1] -= 1
        if position[1] > -1:  # found an allied tile before the edge
            total_flips += possible_flips
            for i in range(position[1], y):  # Flip the pieces
                new_state.board[x][i] = new_state.player

        # Check above and to the left
        possible_flips = 0
        position = [x, y]
        while position[1] > -1 and position[0] > -1 and new_state.board[position[0] - 1][position[1] - 1] == opponent:
            possible_flips += 1
            position[1] -= 1
            position[0] -= 1
        if position[1] > -1 and position[0] > -1:  # found an allied tile before the edge
            total_flips += possible_flips
            for i, j in range(position[0], x), range(position[1], y):  # Flip the pieces
                new_state.board[i][j] = new_state.player

        # Check to the left
        possible_flips = 0
        position = [x, y]
        while position[0] > -1 and new_state.board[position[0]][position[1] - 1] == opponent:
            possible_flips += 1
            position[0] -= 1
        if position[0] > -1:  # found an allied tile before the edge
            total_flips += possible_flips
            for i in range(position[0], x):  # Flip the pieces
                new_state.board[i][y] = new_state.player

        # Check below and to the left
        possible_flips = 0
        position = [x, y]
        while position[1] < 8 and position[0] > -1 and new_state.board[position[0] - 1][position[1] + 1] == opponent:
            possible_flips += 1
            position[1] += 1
            position[0] -= 1
        if position[1] < 8 and position[0] > -1:  # found an allied tile before the edge
            total_flips += possible_flips
            for i, j in range(position[0], x), range(y, position[1]):  # Flip the pieces
                new_state.board[i][j] = new_state.player

        new_state.player = opponent #Alternate the player

