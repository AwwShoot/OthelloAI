from Othello_Game import Othello
test = Othello()

# Initial Random Play
print("Initial Board: ")
test.printout(True)

print("Playing 3,3: ")
test = test.play(3, 2)
test.printout(True)

# Find the next best move
bestMove = test.find_best_move(test)
print("Estimated Best Move: ")
bestMove.printout(True)

print("Playing 2,4")
#test.printout()
test = test.play(2, 4)
test.printout(True)

# Find the next best move
bestMove = test.find_best_move(test)
print("Estimated Best Move: ")
bestMove.printout(True)

print("Playing 2,5")
test = test.play(2, 5)
test.printout(True)

# Find the next best move
bestMove = test.find_best_move(test)
print("Estimated Best Move: ")
bestMove.printout(True)



if test: #Illegal move will return none
    test.printout(True)
else:
    print("Ding!") #everything works :)