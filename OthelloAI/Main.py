from Othello_Game import Othello
test = Othello()
test.printout()
test = test.play(3, 2)
test.printout()
test = test.play(2, 4)
test.printout(True)
test = test.play(6, 6)
if test: #Illegal move will return none
    test.printout(True)
else:
    print("Ding!") #everything works :)