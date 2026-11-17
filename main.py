from config.types_config import WindowSettings,ButtonSettings,Scenario
from config.loader import load_scenario

scenario = load_scenario("menu")
win = scenario.window.make_window()
win.getKey()
