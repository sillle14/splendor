# Updated Animation Starter Code
import random

from core.game_state import GameState
from tkinter import *
from GUI.widgets import *
from GUI.game_pieces import *
from GUI.controller import *
import copy

sys.path.append('..')


####################################
# customize these functions
####################################

def init(data, names):
    # load data.xyz as appropriate
    update_game(data, GameState(names))
    data.controller = Controller()


def update_game(data, game_state):
    data.game = game_state


def mouse_pressed(event, data):
    # use event.x and event.y

    # clicked on gems
    gem = data.controller.get_gem(event.x, event.y)
    if gem is not None:
        data.controller.add_gem(gem)
    
    # clicked on cards
    card = data.controller.get_card(event.x, event.y)
    if card is not None:
        data.controller.add_card(card)
    
    # confirm
    if data.controller.confirmed(event.x, event.y):
        data.controller.take_turn(data.game)  # modifies data.game


def key_pressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "n":
        newstates = data.game.get_possible_moves()[0]
        random.shuffle(newstates)
        newstate = newstates[0]
        update_game(data, newstate)
        print(data.game)
    if event.keysym == " ":
        data.controller.take_turn(data.game)  # modifies data.game


def timer_fired(data):
    pass


def redraw_all(canvas, data):
    # draw cards
    for i in range(3):
        for j in range(4):
            draw_card(canvas, data.game.display[i * 4 + j],
                      100 + j * 135, 100 + (2 - i) * 210)
    # draw display gems
    for (i, gem) in enumerate(Gem):
        for j in range(data.game.gems.amount(gem)):
            draw_gem(canvas, gem, 700 + j * 10, 150 + 110 * i)
    # draw players
    for (i, player) in enumerate(data.game.players):
        draw_player(canvas, player, 800, i * 200)
    # draw other
    canvas.create_text(0 + 20, 0 + 20, text="Splendor",
                       anchor="nw", font="Arial 40 bold")
    canvas.create_text(0 + 20, data.height - 20, 
                       text="Turn: " + str(data.game.turns), anchor="sw",
                       font="Arial 40  bold")
    
    # draw controller
    data.controller.draw(canvas)


####################################
# use the run function as-is
####################################

def run(names):
    width = 1200
    height = 800

    def redraw_all_wrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='beige', width=0)
        redraw_all(canvas, data)
        canvas.update()

    def mouse_pressed_wrapper(event, canvas, data):
        mouse_pressed(event, data)
        redraw_all_wrapper(canvas, data)

    def key_pressed_wrapper(event, canvas, data):
        key_pressed(event, data)
        redraw_all_wrapper(canvas, data)

    def timer_fired_wrapper(canvas, data):
        timer_fired(data)
        redraw_all_wrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timer_fired_wrapper, canvas, data)

    # Set up data and call init
    class Struct(object):
        pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100  # milliseconds
    root = Tk()
    root.resizable(width=False, height=False)  # prevents resizing window
    init(data, names)

    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event: mouse_pressed_wrapper(event, canvas, data))
    root.bind("<Key>", lambda event: key_pressed_wrapper(event, canvas, data))
    timer_fired_wrapper(canvas, data)

    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(800, 800)
