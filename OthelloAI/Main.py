from Othello_Game import Othello
game = Othello()
singleplayer = False
if singleplayer:
    while game != None:
        game.printout(True)
        game = game.find_best_move(game)
else:
    while game != None:
        game.printout(True)
        if len(game.get_possible_moves(game)) == 0:
            print("No possible moves. Game over.")
            break
        coords = input("x and y")
        coords = coords.split()
        possible_game = game.play(int(coords[1]), int(coords[0])) # Swap x and y since the first input is essentially y
        while possible_game == None:
            coords = input("Invalid move, try again")
            coords = coords.split()
            possible_game = game.play(int(coords[1]), int(coords[0]))
        game = game.play(int(coords[1]), int(coords[0]))
        game.printout(True)
        game = game.find_best_move(game)
