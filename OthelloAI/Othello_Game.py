# This file and class is dedicated to handling the game Othello, its rules, and its board
class Othello:
    # I know I could write that programmatically and make it shorter
    # But this means a new board can be easily copy/pasted/modified for testing heuristics
    # 1 is black pieces, which go first, 2 is white pieces.
    board = [[0, 0, 0, 0, 0, 0, 0, 0],  # 0
             [0, 0, 0, 0, 0, 0, 0, 0],  # 1
             [0, 0, 0, 0, 0, 0, 0, 0],  # 2
             [0, 0, 0, 2, 1, 0, 0, 0],  # 3
             [0, 0, 0, 1, 2, 0, 0, 0],  # 4
             [0, 0, 0, 0, 0, 0, 0, 0],  # 5
             [0, 0, 0, 0, 0, 0, 0, 0],  # 6
             [0, 0, 0, 0, 0, 0, 0, 0]]  # 7
    player = 1  # 1 for black 2 for white
    turn = 0  # number of elapsed turns for ply
    depth = 4

    # Heuristic tracking values
    board_value = 0  # All heuristic values contribute to this, which will act as the true "value" of this board state
    total_white = 0
    total_black = 0
    permanent_black = 0
    permanent_white = 0
    possible_moves = 0
    corners_white = 0
    corners_black = 0

    def __init__(self, board=board, player=player, turn=turn):
        self.board = board
        self.player = player
        self.turn = turn

    def clone(self):  # shallow clone

        return Othello([x.copy() for x in self.board.copy()], self.player, self.turn)

    def play(self, x, y):  # returns a new Othello object representing the new game state
        if self.board[x][y] != 0:
            print("Cannot place there, another piece already occupies the space.")
            return  # return None if it's an illegal board state
        new_state = self.clone()
        new_state.turn += 1
        new_state.board[x][y] = new_state.player  # row major order lets things be more readable
        # check lines for tiles to flip
        total_flips = 0
        opponent = (new_state.player % 2) + 1  # easy way to flip player val

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
            # new_state.set_heuristics()
            return new_state
        else:  # A move that causes no flips is illegal.
            return None

    def flip(self, x, y, x_dir, y_dir):
        opponent = (self.player % 2) + 1
        possible_flips = 0
        position = [x, y]
        position[0] += x_dir  # Move the checker along
        position[1] += y_dir
        while -1 < position[0] < 8 and -1 < position[1] < 8:  # Stay in bounds
            if self.board[position[0]][position[1]] == opponent:
                possible_flips += 1
                position[0] += x_dir
                position[1] += y_dir
            elif self.board[position[0]][position[1]] == 0:
                return 0
            else:  # Found an ally, modify the board.
                position[0] -= x_dir
                position[1] -= y_dir  # Move back
                while position[0] != x or position[1] != y:
                    self.board[position[0]][position[1]] = self.player
                    position[0] -= x_dir
                    position[1] -= y_dir
                return possible_flips
        return 0  # Hit a bound before an allied piece

    def printout(self, verbose=False):
        string_components = []  # Joining a list of strings is faster than several concats on larger strings
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
            self.set_heuristics()
            string_components.append(f"\nTurn number: {self.turn}\n")
            string_components.append(f"Player {self.player} to move\n")
            string_components.append(f"White has {self.total_white} pieces\n")
            string_components.append(f"Black has {self.total_black} pieces\n")
            string_components.append(f"board value is {self.board_value}")
        print("".join(string_components))

    def set_heuristics(self):  # sets heuristic values of the board.
        self.board_value = 0
        self.total_black = 0
        self.total_white = 0
        self.permanent_white = 0
        self.permanent_black = 0
        self.corners_black = 0
        self.corners_white = 0

        # Count extra for pieces that can't be changed anymore
        # A piece can't be changed if on at least one side of the X, Y, AND diagonal axis all pieces are its color.
        for x in range(8):
            for y in range(8):  # pick a point
                value = self.board[x][y]
                if value == 1:
                    self.total_black += 1
                    if (x == 7 and y == 7) or (x == 1 and y == 7) or (x == 1 and y == 1) or (x == 7 and y == 7):
                        self.corners_black += 1  # Corners are worth a LOT
                elif value == 2:
                    self.total_white += 1
                    if (x == 7 and y == 7) or (x == 1 and y == 7) or (x == 1 and y == 1) or (x == 7 and y == 7):
                        self.corners_white += 1  # Corners are worth a LOT
                else:
                    continue  # No need to calculate a blank tile
                # Check the X axis
                x_before = True
                x_after = True
                for check_x in range(8):
                    if self.board[check_x][y] != value:
                        if check_x < x:
                            x_before = False
                        else:
                            x_after = False

                # Check the Y axis
                y_before = True
                y_after = True
                for check_y in range(8):
                    if self.board[x][check_y] != value:
                        if check_y < y:
                            y_before = False
                        else:
                            y_after = False

                # Check if the diagonal axis in a lazy, but clever way.
                xy_before = True
                xy_after = True
                check_xy = 0
                while x - check_xy > -1 and y - check_xy > -1:
                    if self.board[x - check_xy][y - check_xy] != value:
                        xy_before = False
                        break
                    check_xy += 1
                check_xy = 0
                while x + check_xy < 8 and y + check_xy < 8:
                    if self.board[x + check_xy][y + check_xy] != value:
                        xy_after = False
                        break
                    check_xy += 1
                # If at least one side on all axis are blocked, then count the tile for extra
                if (x_before or x_after) and (y_before or y_after) and (xy_before or xy_after):
                    if value == 1:
                        self.permanent_black += 1
                    else:
                        self.permanent_white += 1

        # Board state is currently measured as value for player about to play
        self.possible_moves = len(self.get_possible_moves(self))
        if self.player == 1:
            if self.possible_moves == 0 and self.total_black < self.total_white:
                self.board_value += -1000  # DON'T pick a move that ends the game unless you win
            else:
                self.board_value = (self.total_black + 10 * self.permanent_black
                                    + self.corners_black * 100
                                    - self.total_white - 10 * self.permanent_white
                                    - self.corners_white * 100
                                    + 5 * self.possible_moves)
                if self.possible_moves == 0 and self.total_black > self.total_white:
                    self.board_value += 1000
        else:
            if self.possible_moves == 0 and self.total_white < self.total_black:
                self.board_value += -1000  # The don't be a loser clause
            else:
                self.board_value = (self.total_white + 10 * self.permanent_white
                                    + self.corners_white * 100
                                    - self.total_black - 10 * self.permanent_black
                                    - self.corners_black * 100
                                    + 5 * self.possible_moves)
                if self.possible_moves == 0 and self.total_white > self.total_black:
                    self.board_value += 1000

    # Returns true iff the given coordinate has a tile immediately adjacent or diagonal to it
    def potentially_playable_tile(self, state, x, y):
        valid = False
        for i in range(3):
            for j in range(3):
                point_x = x - 1 + i
                point_y = y - 1 + j
                if -1 < point_x < 8 and -1 < point_y < 8:
                    if state.board[point_x][point_y] != 0:
                        if i == j and j == 1:
                            return False  # Target tile is taken.
                        else:
                            valid = True  # At least one potential tile to flip makes it valid
        return valid

    # Dig through the tiles looking for ones not white or black    
    def get_possible_moves(self, state):
        moves = []
        for x in range(8):
            for y in range(8):
                if self.potentially_playable_tile(state, x,
                                                  y):  # Slight optimization so we don't check EVERY empty tile
                    new_state = state.play(x, y)
                    if new_state:
                        moves.append(new_state)
        return moves

        # MinMax With Alpha-Beta Pruning

    # Will always use an odd-numbered ply that looks for the best future board for the player calling this
    # Find the lowest value returned to ply = 1 (I.E. what the enemy will pick at the end of our prediction)
    # Pass it up to ply > 1
    # At ply > 1, pass down this pruning value. If a min value lower than that is found in a different decision path
    # Stop calculating that branch, pruning it.
    # If a higher minimum can be found, set the pruning value to that.
    def minimax(self, state, depth, maximizing_player, prune=float('-inf')):
        if depth == 0 or self.get_possible_moves(state) == 0:
            state.set_heuristics()
            return state.board_value  # Only time board value is asked for so why calc it any other time

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(state):
                evaluation = self.minimax(move, depth - 1, False, max_eval)
                max_eval = max(max_eval, evaluation)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(state):
                evaluation = self.minimax(move, depth - 1, True, prune)
                min_eval = min(min_eval, evaluation)
                if min_eval < prune:
                    return min_eval  # Cut off calculation early if opponent will do worse than your worst option elsewhere
            return min_eval

    # We check possible moves and use MinMax to find the best one  
    def find_best_move(self, state):
        best_eval = float('-inf')
        best_move = None
        for move in self.get_possible_moves(state):
            evaluation = self.minimax(move, self.depth, False)
            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
        return best_move

        # Game end Condition