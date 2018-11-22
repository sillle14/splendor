# Basic widgets for tkinter

class Button(object) : 

    def __init__(self, x0, y0, x1, y1, **kwargs):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1 
        self.y1 = y1
        if "text" in kwargs:
            self.text = kwargs["text"]
        else:
            self.text = None
        if "fill" in kwargs:
            self.fill = kwargs["fill"]
        else:
            self.fill = "white"

    def draw(self, canvas):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1,fill=self.fill)
        canvas.create_text((self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2, text=self.text)

    def isClicked(self, x, y):
        return self.x0 < x < self.x1 and self.y0 < y < self.y1
    
