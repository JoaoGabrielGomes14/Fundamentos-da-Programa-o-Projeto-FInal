##load scenario and make the main menu logic
from typing import Callable
from graphics import GraphicsError
from config.loader import load_scenario
from graphical_logic.classes import Button


OPTION_IDS: tuple[str, ...] = ("1", "2", "3", "4")


def run_scenario_main_menu(json_name: str, start_scene: Callable[[str], None]) -> None:
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
            start_scene(selected)         #the main menu gets this callable from the orchestrator and uses it. 
            continue                    

        for option_id in OPTION_IDS:
            if buttons[option_id].clicked(click):
                if selected is not None:
                    buttons[selected].deselect()   
                buttons[option_id].select()    #if we choose one it need to deactivate the last and select itself    
                selected = option_id
                start.activate()

        window.update()                 

    window.close()