##load scenario and make the main menu logic
from config.loader import load_scenario
from typing import Callable
from graphics import GraphicsError
from config.loader import load_scenario
from graphical_logic.classes import Button

OPTION_IDS: tuple[str, ...] = ("1", "2", "3", "4")


def run_scenario_main_menu(json_name: str, scenes: dict[str, Callable[[], None]]) -> None:
    scenario = load_scenario(json_name)
    window = scenario.window.make_window()

    buttons: dict[str, Button] = {}
    for button_settings in scenario.buttons:
        buttons[button_settings.id] = Button(window, button_settings)

    start = buttons["start"]
    quit_button = buttons["quit"]
    start.deactivate()                  
    selected: str | None = None
    window.update()

    while True:
        try:
            click = window.getMouse()   
        except GraphicsError:           
            return

        if quit_button.clicked(click):
            break

        if start.clicked(click):        
            scenes[selected]()         #if you chose one and then press start clal the function to next scenario like run_scenario_2()
            continue                    #like in the readme maybe add an orchestrator, maybe not needed

        for option_id in OPTION_IDS:
            if buttons[option_id].clicked(click):
                if selected is not None:
                    buttons[selected].deselect()   
                buttons[option_id].select()    #if we choose one it need to deactivate the last and select itself    
                selected = option_id
                start.activate()

        window.update()                 

    window.close()