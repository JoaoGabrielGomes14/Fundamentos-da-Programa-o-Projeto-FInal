from graphics import GraphWin
from dataclasses import dataclass,field
#save types used throughout the program


@dataclass(frozen=True,slots=True,kw_only=True)
class WindowSettings():
    width: int
    height: int
    title: str
    background: str ##we can do like "White" or put the color by hex, i think its the name, like 8d4fa4
    x_min : float
    y_min : float
    dimension_size_x : float | None = None
    dimension_size_y : float | None = None

    @property
    def x_max(self):
        return self.x_min + (self.dimension_size_x if self.dimension_size_x is not None else self.width)


    @property
    def y_max(self):
        return self.y_min + (self.dimension_size_y if self.dimension_size_y is not None else self.height)
    

    def make_window(self)->GraphWin:
        window = GraphWin(
            title=self.title,
            width=self.width,
            height=self.height,
            autoflush=False
        )
        window.setBackground(self.background)
        window.setCoords(self.x_min,self.y_min,self.x_max,self.y_max)
        return window

    #perguntar se podemos usar method master.geometry do tkinter para mover a janela
@dataclass(frozen=True,slots=True,kw_only=True)
class ButtonStyle():
    fill: str = "lightgray"
    outline: str = "black"
    font: str = "helvetica"            
    text_color: str = "black"
    text_size: int = 12                
    border_width: int = 2
    inactive_text_color: str = "darkgray"
    inactive_border_width: int = 1
    selected_text_color: str = "red"
    selected_text_size: int = 20


@dataclass(frozen=True,slots=True,kw_only=True)
class ButtonSettings():
    id:str
    center: tuple[int,int]
    shape:str
    label:str
    width:float
    heigth:float
    style : ButtonStyle = field(default_factory=ButtonStyle)


@dataclass(frozen=True,slots=True,kw_only=True)
class Scenario():
    title:str #the name of the scenario
    window: WindowSettings
    buttons: tuple[ButtonSettings,...]
    physics: dict | None = None  #rules of physics that might be important for the scenario
    character: CharacterSettings | None = None
    targets: TargetSettings | None = None  #for exampple menu will not get these,


@dataclass(frozen=True, slots=True, kw_only=True)
class CharacterSettings():
    position: tuple[float, float]
    height: float
    color: str = "black"


@dataclass(frozen=True, slots=True, kw_only=True)
class TargetSettings():
    count: int
    radius: float
    lifetime: float
    spawn_area: tuple[float, float, float, float]
    fill: str = "blue"
    image: str | None = None