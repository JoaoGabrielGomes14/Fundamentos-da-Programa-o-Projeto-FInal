from graphics import GraphWin
from dataclasses import dataclass,field
#settings of objects, then passed as atributes to corresponding classes in graphica_logic/classes



@dataclass(frozen=True,slots=True,kw_only=True)
class WindowSettings():
    width: int
    height: int
    title: str
    background: str ##we can do like "White" or put the color by hex, like "#8d4fa4"
    x_min : float
    y_min : float
    world_width : float | None = None   #size in world units, None = same as pixels
    world_height : float | None = None

    @property
    def x_max(self):
        return self.x_min + (self.world_width if self.world_width is not None else self.width)


    @property
    def y_max(self):
        return self.y_min + (self.world_height if self.world_height is not None else self.height)
    

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
    inactive_text_color: str = "darkgray" #a button has three looks: normal, inactive (cant be clicked) and selected (the chosen option)
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
    style : ButtonStyle = field(default_factory=ButtonStyle) #one new instance per button, right now this is not needed because  buttonstyle is immutable but its the safe way


@dataclass(frozen=True, slots=True, kw_only=True)
class CharacterSettings():
    position: tuple[float, float] #we might need to make it so that it has more complex stuff like an atribute "arms" or "legs" 
    height: float
    color: str = "black"



#maybe change name, this isnt really a target anymore tbh, its a target in scenario 1 but more like a "drone" in 2 , we could make a different class but this is so simiar(just added a move method and do checks)(not worth doing inhereatance, just extra complexity for no reason (my opinion)for only two as well )
@dataclass(frozen=True, slots=True, kw_only=True)
class TargetSettings():
    radius: float
    count: int = 1
    lifetime: float | None = None   #this is so it can despaawn like said in the assignemtn, None = never respawns by time (scenario 2)
    spawn_area: tuple[float, float, float, float] | None = None #where a target without a path can appear, so it wont spawn in front of the buttons or character
    speed: int = 1   #how many points of the path it moves per frame, only used when it follows a path
    fill: str = "blue"
    image: str | None = None #we will probably check for one or the other, it doesnt make a lot of sense to have both in one target, either image or color


@dataclass(frozen=True,slots=True,kw_only=True)
class Scenario():
    title:str #the name of the scenario
    window: WindowSettings
    buttons: tuple[ButtonSettings,...]
    physics: dict = field(default_factory=dict)  #rules of physics that might be important for the scenario
    hud: dict = field(default_factory=dict)
    character: CharacterSettings | None = None
    targets: TargetSettings | None = None  #for exampple menu will not get these,
    trajectory_area: tuple[float, float, float, float] | None = None