from GUI.widgets import Button
from core.game_state import GameState
from core.game_pieces import *


class Controller(object):

    def __init__(self):
        self.selected_gems = None
        self.selected_card = None  # tuple of row, col coords
        self.is_drawing = True  # True is drawing gems, False is buying cards

        self.button = Button(1100, 750, 1180, 780, 
                             fill="brown", text="Confirm")
        self.exception_text = ""

    def get_gem(self, x, y):
        # returns gem that's been clicked on
        r = 50
        if abs(x - 720) < (r + 20):  # x range
            for (i, gem) in enumerate(Gem):
                if abs(y - (150 + 110 * i)) < r:  # y range
                    return gem
        return None

    def add_gem(self, gem: Gem):
        self.is_drawing = True
        self.selected_card = None
        if self.selected_gems is None:
            self.selected_gems = Bundle()
        self.selected_gems.add(gem)

    def get_card(self, x, y):
        # returns card that's been clicked on
        w = 125
        h = 200
        for i in range(3):
            for j in range(4):
                if 0 < (x - (100 + j * 135)) < w and 0 < (y - (100 + (2 - i) * 210)) < h:
                    return i, j
        return None

    def add_card(self, card):
        self.is_drawing = False
        self.selected_gems = None
        self.selected_card = card

    def confirmed(self, x, y):
        return self.button.is_clicked(x, y)

    def take_turn(self, game_state: GameState):
        # tries to take the turn
        try: 
            if self.is_drawing:
                game_state.draw_gems(self.selected_gems)
                self.selected_gems = None
            else:
                (i, j) = self.selected_card
                card = game_state.display[i * 4 + j]
                game_state.buy_card(card)
                self.selected_card = None
            self.exception_text = ""
        except Exception as exc:
            self.exception_text = str(exc)
            self.selected_card = None
            self.selected_gems = None

    def draw(self, canvas):
        if self.selected_card is not None or self.selected_gems is not None:
            self.button.draw(canvas)
        if self.selected_gems is not None:
            r = 50
            for (i, gem) in enumerate(Gem):
                if self.selected_gems.amount(gem) > 0:
                    canvas.create_rectangle(700 - r, 150 + 110 * i - r,
                                            740 + r, 150 + 110 * i + r,
                                            fill=None, 
                                            width=3*self.selected_gems.amount(gem))
        elif self.selected_card is not None:
            i, j = self.selected_card
            w, h = 125, 200
            canvas.create_rectangle(100 + j * 135, 100 + (2 - i) * 210,
                                    100 + j * 135 + w, 100 + (2 - i) * 210 + h,
                                    fill=None, width=3)
        
        canvas.create_text(1050, 750, anchor="ne", text=self.exception_text, 
                           font="Arial 20 bold", fill="red")
