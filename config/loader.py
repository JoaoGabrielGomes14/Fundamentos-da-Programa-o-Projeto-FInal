from config.types_config import WindowSettings, ButtonSettings,Scenario
import json
#make a loader, reads from json and outputs objects corresponding to that window, fro example the "main menu" reads and outputs and object with everything

def load_scenario(name, path="config/config.json")->Scenario:
    with open(path) as f:
        data = json.load(f)[name]

    window = WindowSettings(**data["window"])

    buttons = []
    for button in data["buttons"]:
        button["center"] = tuple(button["center"])
        buttons.append(ButtonSettings(**button))

    return Scenario(title=name, window=window, buttons=tuple(buttons))