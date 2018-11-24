from core.game_pieces import *

COLORMAP = {Gem.WHITE: "#b9f2ff", Gem.RED: "#e0115f", Gem.GREEN: "#50c878", Gem.BLUE: "#0f52ba", Gem.BLACK: "#696969"}


def draw_card(canvas, card, x, y):
    w = 125
    h = 200
    canvas.create_rectangle(x, y, x+w, y+h, fill=COLORMAP[card.gem])
    for (i, gem) in enumerate(card.cost.gems):
        # Gem cost in bottom
        canvas.create_oval(x + w/5*i, y + h - w/5,
                           x + w/5*(i+1), y + h,
                           fill=COLORMAP[gem])
        canvas.create_text(x + w/5*i + w/10, y + h - w/10,
                           text=str(card.cost.amount(gem)))
        # Gem gained
        # Points gained
        canvas.create_text(x + w/6, y + w/6, text=card.points,
                           font="Arial 20 bold")


def draw_gem(canvas, gem, x, y):
    r = 50
    canvas.create_oval(x-r, y-r, x+r, y+r, fill=COLORMAP[gem])


def draw_player(canvas, player, x, y):
    w = 400
    h = 200
    m = 5
    canvas.create_rectangle(x+m, y+m, x + w-m, y + h-m, fill="salmon1")
    # name
    if player.my_turn:
        canvas.create_text(x + 15, y + 15, text="**"+player.name+"**",
                           anchor="nw", font="Arial 30 bold")
    else:
        canvas.create_text(x + 15, y + 15, text=player.name,
                           anchor="nw", font="Arial 30 bold")
    # points
    canvas.create_text(x + w - 15, y + 15, text=str(player.points), 
                       anchor="ne", font="Arial 30 bold")
    # gems
    for (i, gem) in enumerate(Gem):
        for j in range(player.gems.amount(gem)):
            canvas.create_oval(x + w/4 + i * w/8, y + h/3 + j*5, 
                               x + w/4 + (i+1) * w/8, y + h/3 + w/8 + j*5,
                               fill=COLORMAP[gem])
    # cards
    for (i, gem) in enumerate(Gem):
        for j in range(player.tableau.amount(gem)):
            canvas.create_rectangle(x + w/4 + i * w/8, y + h*2/3 + j*5, 
                                    x + w/4 + (i+1) * w/8, y + h*2/3 + w/8 + j*5,
                                    fill=COLORMAP[gem])
