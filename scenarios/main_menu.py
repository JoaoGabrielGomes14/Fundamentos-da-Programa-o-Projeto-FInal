##load scenario and make the main menu logic
##load scenario and make the main menu logic
from config.loader import load_scenario
from graphical_logic.classes import Button


def run_scenario_main_menu(json_name: str) -> None:
    scenario = load_scenario(json_name)
    window = scenario.window.make_window()

    buttons: dict[str, Button] = {}
    for button_settings in scenario.buttons:
        buttons[button_settings.id] = Button(window, button_settings)

    window.update()
    window.getMouse()