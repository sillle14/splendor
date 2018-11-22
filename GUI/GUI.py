# Updated Animation Starter Code
import sys
sys.path.append('..')
from core.game_state import GameState
from tkinter import *
from GUI.widgets import *
from GUI.game_pieces import *

import random

####################################
# customize these functions
####################################

def init(data, names):
    # load data.xyz as appropriate
    updateGame(data, GameState(names))


def updateGame(data, game_state):
    data.game = game_state


def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "n":
        newstates = data.game.get_possible_moves()[0]
        random.shuffle(newstates)
        newstate = newstates[0]
        updateGame(data, newstate)
        print(data.game)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw cards
    for i in range(3):
        for j in range(4):
            drawCard(canvas, data.game.display[i*4+j],100+  j*135,100 + (2-i)*210)
    # draw display gems
    for (i, gem) in enumerate(Gem):
        for j in range(data.game.gems.amount(gem)):
            drawGem(canvas, gem, 700 + j*10, 150 + 110*i)
    # draw players
    for (i, player) in enumerate(data.game.players):
        drawPlayer(canvas, player, 800, i * 200)
    # draw other
    canvas.create_text(0 + 20, 0 + 20, text="Splendor", anchor="nw", font="Arial 40 bold")
    canvas.create_text(0 + 20, data.height - 20, text="Turn: "+str(data.game.turns), anchor="sw", font="Arial 40  bold")
    

####################################
# use the run function as-is
####################################

def run(names):
    width = 1200
    height = 800
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='beige', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data, names)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(800, 800)