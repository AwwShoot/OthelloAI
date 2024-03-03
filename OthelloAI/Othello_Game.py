# This file and class is dedicated to handling the game Othello, its rules, and its board
class Othello:
    # I know I could write that programmatically and make it shorter
    # But this means a new board can be easily copy/pasted/modified for testing heuristics
    # 1 is black pieces, which go first, 2 is white pieces.
    board = [[0,0,0,0,0,0,0,0], #0
             [0,0,0,0,0,0,0,0], #1
             [0,0,0,0,0,0,0,0], #2
             [0,0,0,2,1,0,0,0], #3
             [0,0,0,1,2,0,0,0], #4
             [0,0,0,0,0,0,0,0], #5
             [0,0,0,0,0,0,0,0], #6
             [0,0,0,0,0,0,0,0]] #7
    player = 1 #1 for black 2 for white
    turn = 0 # number of elapsed turns for ply

    # Heuristic tracking values
    board_value = 0 # All heuristic values contribute to this, which will act as the true "value" of this board state
    total_white = 0
    total_black = 0

    def __init__(self, board = board, player = player, turn = turn):
        self.board = board
        self.player = player
        self.turn = turn
    def clone(self): # shallow clone

        return Othello([x.copy() for x in self.board.copy()], self.player, self.turn)
    def play(self, x, y): #returns a new Othello object representing the new game state
        if self.board[x][y] != 0:
            print("Cannot place there, another piece already occupies the space.")
            return #return None if it's an illegal board state
        new_state = self.clone()
        new_state.turn += 1
        new_state.board[x][y] = new_state.player# row major order lets things be more readable
        # check lines for tiles to flip
        total_flips = 0
        opponent =  (new_state.player%2) + 1 #easy way to flip player val

        # Check below
        total_flips += new_state.flip(x, y, 0, 1)

        # Check below and to the right
        total_flips += new_state.flip(x, y, 1, 1)

        # Check to the right
        total_flips += new_state.flip(x, y, 1, 0)

        # Check above and to the right
        total_flips += new_state.flip(x, y, 1, -1)

        # Check above
        total_flips += new_state.flip(x, y, 0, -1)

        # Check above and to the left
        total_flips += new_state.flip(x, y, -1, -1)

        # Check to the left
        total_flips += new_state.flip(x, y, -1, 0)

        # Check below and to the left
        total_flips += new_state.flip(x, y, -1, 1)

        new_state.player = opponent  # Alternate the player
        if total_flips > 0:
            new_state.set_heuristics()
            return new_state
        else: #A move that causes no flips is illegal.
            return None


    def flip(self, x, y, x_dir, y_dir):
        opponent =  (self.player%2) + 1
        possible_flips = 0
        position = [x, y]
        position[0] += x_dir# Move the checker along
        position[1] += y_dir 
        while -1 < position[0] < 8 and -1 < position[1] < 8: # Stay in bounds
            if self.board[position[0]][position[1]] == opponent:
                possible_flips += 1
                position[0] += x_dir
                position[1] += y_dir
            elif self.board[position[0]][position[1]] == 0:
                return 0
            else: # Found an ally, modify the board. 
                position[0] -= x_dir
                position[1] -= y_dir # Move back
                while position[0] != x or position[1] != y:
                    self.board[position[0]][position[1]] = self.player
                    position[0] -= x_dir
                    position[1] -= y_dir
                return possible_flips
        return 0# Hit a bound before an allied piece
        
    def printout(self, verbose=False):
        string_components = [] #Joining a list of strings is faster than several concats on larger strings
        for row in self.board:
            for tile in row:
                tile_str = ''
                match tile:
                    case 0:
                        tile_str = '- '
                    case 1:
                        tile_str = 'X '
                    case 2:
                        tile_str = '0 '
                string_components.append(tile_str)
            string_components.append("\n")
        # Display heuristics as well if verbose
        if verbose:
            string_components.append(f"\nTurn number: {self.turn}\n")
            string_components.append(f"Player {self.player} to move\n")
            string_components.append(f"White has {self.total_white} pieces\n")
            string_components.append(f"Black has {self.total_black} pieces")
        print("".join(string_components))


    def set_heuristics(self): # sets heuristic values of the board.

        for row in self.board:
            for tile in row:
                if tile == 1:
                    self.total_black += 1
                elif tile == 2:
                    self.total_white += 1

        if self.player == 1:
            self.board_value = self.total_black - self.total_white
        else:
            self.board_value = self.total_white - self.total_black
        
    def get_possible_moves(self, state):
        moves = []
        for x in range(8):
            for y in range(8):
                if state.board[x][y] == 0:
                    new_state = state.play(x, y)
                    if new_state:
                        moves.append(new_state)
        return moves 
     
        
    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or self.is_game_over(state):
            return state.board_value

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(state):
                eval = self.minimax(move, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(state):
                eval = self.minimax(move, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
      
    def find_best_move(self, state):
        best_eval = float('-inf')
        best_move = None
        for move in self.get_possible_moves(state):
            eval = self.minimax(move, self.depth, False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move      
        
    def is_game_over(self, state):
        
        return len(self.get_possible_moves(state)) == 0