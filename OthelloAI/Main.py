from Othello_Game import Othello
game = Othello()

while game != None:
    game.printout(True)
    game = game.find_best_move(game)
