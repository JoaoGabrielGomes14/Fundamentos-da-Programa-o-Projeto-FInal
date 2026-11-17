from graphics import GraphWin
from config.types_config import ButtonSettings


from graphics import Point, Polygon, Text
from config.types_config import ButtonSettings


class Button:
    def __init__(self, win, settings: ButtonSettings):
        self.settings = settings
        self.id = settings.id

        # center and half sizes, used for drawing and for click checks
        self.x, self.y = settings.center
        self.half_w = settings.width / 2
        self.half_h = settings.heigth / 2

        # the shape
        self.shape = Polygon(*self._corners())
        self.shape.setFill("lightgray")
        self.shape.draw(win)

        # the text
        self.text = Text(Point(self.x, self.y), settings.label)
        self.text.draw(win)

        self.activate()
        self.deselect()

    def _corners(self):
        x, y, w, h = self.x, self.y, self.half_w, self.half_h
        if self.settings.shape == "diamond":
            return [Point(x, y + h), Point(x + w, y), Point(x, y - h), Point(x - w, y)]
        if self.settings.shape == "rect":
            return [Point(x - w, y - h), Point(x + w, y - h), Point(x + w, y + h), Point(x - w, y + h)]
        raise ValueError(f"unknown button shape: {self.settings.shape}")

    def clicked(self, p):
        """True if the button is active and the point p is inside it."""
        if not self.active or p is None:
            return False
        dx = abs(p.getX() - self.x)
        dy = abs(p.getY() - self.y)
        if self.settings.shape == "diamond":
            return dx / self.half_w + dy / self.half_h <= 1
        return dx <= self.half_w and dy <= self.half_h

    # on/off: an inactive button ignores clicks
    def activate(self):
        self.active = True
        self.text.setTextColor("black")
        self.shape.setWidth(2)

    def deactivate(self):
        self.active = False
        self.text.setTextColor("darkgray")
        self.shape.setWidth(1)

    # selected: highlights the chosen option
    def select(self):
        self.text.setTextColor("red")
        self.text.setSize(20)

    def deselect(self):
        self.text.setTextColor("black" if self.active else "darkgray")
        self.text.setSize(12)

    def undraw(self):
        self.shape.undraw()
        self.text.undraw()