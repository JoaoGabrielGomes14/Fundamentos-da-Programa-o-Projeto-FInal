from graphics import GraphWin, Point, Polygon, Text
from config.types_config import ButtonSettings, ButtonStyle


class Button:
    def __init__(self, win: GraphWin, settings: ButtonSettings) -> None:
        self.settings: ButtonSettings = settings    #this will load the settings and style
        self.style: ButtonStyle = settings.style
        self.id: str = settings.id
        self.active: bool = True #to check if the button can be pressed or not
        self.selected: bool = False #see if this is the one the user clicked

        self.x: float = settings.center[0]
        self.y: float = settings.center[1]
        self.half_w: float = settings.width / 2  #we have the center so the witdht/2 gives us the border of the shape. for calculating self.selected
        self.half_h: float = settings.heigth / 2

        self.shape: Polygon = Polygon(*self._corners()) #this gets drawn by graphics
        self.shape.setFill(self.style.fill)
        self.shape.setOutline(self.style.outline)
        self.shape.draw(win)

        self.text: Text = Text(Point(self.x, self.y), settings.label)
        self.text.setFace(self.style.font)
        self.text.draw(win)

        self._refresh()

    def _corners(self) -> list[Point]:  # this shape is to tell graphics what to draw
        x, y, w, h = self.x, self.y, self.half_w, self.half_h
        if self.settings.shape == "diamond":
            return [Point(x, y + h), Point(x + w, y), Point(x, y - h), Point(x - w, y)]
        if self.settings.shape == "rect":
            return [Point(x - w, y - h), Point(x + w, y - h), Point(x + w, y + h), Point(x - w, y + h)]
        raise ValueError(f"unknown button shape: {self.settings.shape}")

    def _refresh(self) -> None:
        """update the style, thisis so that if the button is selected it changes its size or color"""
        s = self.style
        if self.selected:
            self.text.setTextColor(s.selected_text_color)
            self.text.setSize(s.selected_text_size)
        elif self.active:
            self.text.setTextColor(s.text_color)
            self.text.setSize(s.text_size)
        else:
            self.text.setTextColor(s.inactive_text_color)
            self.text.setSize(s.text_size)
        self.shape.setWidth(s.border_width if self.active else s.inactive_border_width)

    def clicked(self, p: Point | None) -> bool: # this is the math to check if its inside or not
        if not self.active or p is None:
            return False
        dx = abs(p.getX() - self.x)
        dy = abs(p.getY() - self.y)
        if self.settings.shape == "diamond":
            return dx / self.half_w + dy / self.half_h <= 1
        return dx <= self.half_w and dy <= self.half_h

    def activate(self) -> None:
        self.active = True
        self._refresh()

    def deactivate(self) -> None:
        self.active = False
        self._refresh()

    def select(self) -> None:
        self.selected = True
        self._refresh()

    def deselect(self) -> None:
        self.selected = False
        self._refresh()

    def undraw(self) -> None:
        self.shape.undraw()
        self.text.undraw()