from config.types_config import WindowSettings, ButtonSettings,Scenario,ButtonStyle,CharacterSettings,TargetSettings
import json
#make a loader, reads from json and outputs objects corresponding to that window, fro example the "main menu" reads and outputs and object with everything



def load_scenario(name: str, path: str = "config/config.json") -> Scenario:
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
        t["spawn_area"] = tuple(t["spawn_area"])
        targets = TargetSettings(**t)

    return Scenario(title=name, window=window, buttons=tuple(buttons),
                    physics=data.get("physics", {}), hud=data.get("hud", {}),
                    character=character, targets=targets)


def all_scenarios(path:str = "config/config.json")->tuple[str,...]:
    with open(path) as f:
        data = json.load(f)
    return tuple(data.keys())