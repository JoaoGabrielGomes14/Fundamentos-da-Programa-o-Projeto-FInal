from graphics import GraphWin, Point, Polygon, Text,Image,Line,Circle
from config.types_config import ButtonSettings, ButtonStyle,CharacterSettings,TargetSettings
import random
#this is where we define the behavior of things needed. we pass the settings and this is the finished , drawn version of these objects,
#implement here all needed logic for each thing. for example a button needs to be able to know when was clicked or how to disapear



class Button:
    def __init__(self, win: GraphWin, settings: ButtonSettings) -> None:
        self.settings: ButtonSettings = settings    #this will load the settings and style
        self.style: ButtonStyle = settings.style
        self.id: str = settings.id
        self.active: bool = True #to check if the button can be pressed or not
        self.selected: bool = False #see if this is the one the user clicked

        self.x: float = settings.center[0]
        self.y: float = settings.center[1]
        self.half_w: float = settings.width / 2  #used to calculate the corners 
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
        """takes in a point checks to see if its inside the area of the button"""
        if not self.active or p is None:
            return False
        dx = abs(p.getX() - self.x)
        dy = abs(p.getY() - self.y)
        if self.settings.shape == "diamond":
            return dx / self.half_w + dy / self.half_h <= 1
        return dx <= self.half_w and dy <= self.half_h


    def activate(self) -> None:
        """if the button can be pressed or not, used for when it must reach a state before being available,see comment for info"""
        #this is used in the main menu, not press start unless an option is selected
        self.active = True
        self._refresh()


    def deactivate(self) -> None:
        self.active = False
        self._refresh()


    def select(self) -> None:
        """is the "chosen" option,changes look"""
        self.selected = True
        self._refresh()


    def deselect(self) -> None:
        self.selected = False
        self._refresh()


    def undraw(self) -> None:
        self.shape.undraw()
        self.text.undraw()


#right now this is a drawn stickman, if were gonna use an image then change this
class Character():
    HEAD_RADIUS: float = 0.12
    HIP_HEIGHT: float = 0.4
    SHOULDER_HEIGHT: float = 0.7   #picking a shape of the character, like said in types config we might want to make it custom but for now should do
    HAND_HEIGHT: float = 0.6
    LEG_SPREAD: float = 0.2
    ARM_REACH: float = 0.25

    def __init__(self, win: GraphWin, settings: CharacterSettings) -> None:
        self.settings: CharacterSettings = settings
        self.x: float = settings.position[0]
        self.y: float = settings.position[1]
        h: float = settings.height
        self.win: GraphWin = win


        head_r = h * self.HEAD_RADIUS
        neck = Point(self.x, self.y + h - 2 * head_r)
        hip = Point(self.x, self.y + h * self.HIP_HEIGHT)
        shoulder = Point(self.x, self.y + h * self.SHOULDER_HEIGHT)

        self.parts: list[Circle | Line] = [
            Circle(Point(self.x, self.y + h - head_r), head_r),
            Line(neck, hip),
            Line(hip, Point(self.x - h * self.LEG_SPREAD, self.y)),
            Line(hip, Point(self.x + h * self.LEG_SPREAD, self.y)),
            Line(shoulder, Point(*self.hand())),
            Line(shoulder, Point(self.x - h * self.ARM_REACH, self.y + h * self.HAND_HEIGHT)),
        ]
        self.draw()

    def draw(self)->None:
        for part in self.parts:
            part.setOutline(self.settings.color)
            part.setWidth(2)
            part.draw(self.win)

    def hand(self) -> tuple[float, float]:
        h = self.settings.height
        return self.x + h * self.ARM_REACH, self.y + h * self.HAND_HEIGHT

    def undraw(self) -> None:
        for part in self.parts:
            part.undraw()


    def move(self,point:Point)->None:
        dx = point.getX() - self.x
        dy = point.getY() - self.y
        for part in self.parts:
            part.move(dx, dy)
        self.x = point.getX()
        self.y = point.getY()


class Target():
    def __init__(self, win: GraphWin, settings: TargetSettings, path: list[Point] | None = None) -> None:
        self.win: GraphWin = win
        self.settings: TargetSettings = settings
        self.path: list[Point] | None = path   #None = stays still (scenario 1), a list of points makes it follows the path (scenario 2 and 3)
        self.index: int = 0
        self.center: Point = Point(0, 0)
        self.body: Circle | Image | None = None
        self.visible: bool = False
        self.timer: float = 0.0
        self.respawn()

    def respawn(self) -> None:
        """choses a random spot in spawn area and reapear there"""
        self.hide()
        if self.path:
            self.index = 0
            self.center = self.path[0].clone()
        else:
            if self.settings.spawn_area is None:
                raise ValueError("a target without a path needs a spawn_area in the config so that it doesnt go spawing in bad places")
            x1, y1, x2, y2 = self.settings.spawn_area
            self.center = Point(random.uniform(x1, x2), random.uniform(y1, y2))

        if self.settings.image is not None:
            self.body = Image(self.center.clone(), self.settings.image)
        else:
            self.body = Circle(self.center.clone(), self.settings.radius)
            self.body.setFill(self.settings.fill)

        self.body.draw(self.win)
        self.visible = True
        self.timer = 0.0

    def set_path(self, path: list[Point] | None) -> None:
        """the path the drone is going to take (scenario 2,3)"""
        self.path = path
        self.respawn()

    def step(self) -> None:
        """move to the next point in path"""
        if not self.path or self.body is None:
            return
        self.index = (self.index + self.settings.speed) % len(self.path)
        new = self.path[self.index]
        self.body.move(new.getX() - self.center.getX(), new.getY() - self.center.getY())
        self.center = new.clone()

    def hide(self) -> None:
        if self.body is not None:
            self.body.undraw()
        self.visible = False

    def hit_by(self, x: float, y: float) -> bool:
        if not self.visible:
            return False
        dx = x - self.center.getX()
        dy = y - self.center.getY()
        return dx * dx + dy * dy <= self.settings.radius ** 2

    def tick(self, dt: float) -> None:
        """for the target to disapear, (if it has a limited lifetime)"""
        if self.settings.lifetime is None:
            return
        self.timer += dt
        if self.timer >= self.settings.lifetime:
            self.respawn()

    def undraw(self) -> None:
        self.hide()