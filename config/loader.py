from config.types_config import WindowSettings, ButtonSettings,Scenario,ButtonStyle
import json
#make a loader, reads from json and outputs objects corresponding to that window, fro example the "main menu" reads and outputs and object with everything



def load_scenario(name: str, path: str = "config/config.json") -> Scenario:
    with open(path) as f:
        data: dict = json.load(f)[name]

    window = WindowSettings(**data["window"])
    default_style: dict = data.get("button_style", {})

    buttons: list[ButtonSettings] = []
    for button in data["buttons"]:
        style = ButtonStyle(**{**default_style, **button.get("style", {})})
        fields: dict = {key: value for key, value in button.items() if key != "style"}
        fields["center"] = tuple(fields["center"])
        buttons.append(ButtonSettings(**fields, style=style))

    return Scenario(title=name, window=window, buttons=tuple(buttons),physics=data.get("physics", {}),)
