from config.types_config import WindowSettings, ButtonSettings,Scenario,ButtonStyle,CharacterSettings,TargetSettings
import json
#loader, reads the json config file and gives ready to use objects.
#The Scenario object contains all info needed to instanciate all objects of a given scenario(main menu is also a scenario)
#This only creates settings (data), never graphics objects, because creating those opens windows and draws
#Scenario cointains only the information needed to create everything in the form of objects defined in types_config
#the implementation of classes as well as the phisical behavior is (for now) in graphical_logic/classes ,,, Ex ther button class



def load_scenario(name: str, path: str = "config/config.json") -> Scenario:
    """get scenario settings from config"""
    with open(path) as f:
        data: dict = json.load(f)[name]

    window = WindowSettings(**data["window"])
    default_style: dict = data.get("button_style", {})

    buttons: list[ButtonSettings] = []
    for button in data.get("buttons", []):
        style = ButtonStyle(**{**default_style, **button.get("style", {})})
        fields: dict = {key: value for key, value in button.items() if key != "style"}
        fields["center"] = tuple(fields["center"])
        buttons.append(ButtonSettings(**fields, style=style))

    character = None
    if "character" in data:
        c = dict(data["character"])
        c["position"] = tuple(c["position"])
        character = CharacterSettings(**c)

    targets = None
    if "targets" in data:
        t = dict(data["targets"])
        if t.get("spawn_area") is not None:
            t["spawn_area"] = tuple(t["spawn_area"])
        targets = TargetSettings(**t)

    trajectory_area = None
    if "trajectory_area" in data:
        trajectory_area = tuple(data["trajectory_area"])

    return Scenario(title=name, window=window, buttons=tuple(buttons),
                    physics=data.get("physics", {}), hud=data.get("hud", {}),
                    character=character, targets=targets, trajectory_area=trajectory_area)



#only used for orchestrator to get all existent scenarios
def all_scenarios(path:str = "config/config.json")->tuple[str,...]:
    """get names of all scenarios in config"""
    with open(path) as f:
        data = json.load(f)
    return tuple(data.keys())