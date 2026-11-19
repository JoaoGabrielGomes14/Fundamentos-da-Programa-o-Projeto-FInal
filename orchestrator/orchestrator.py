from typing import Callable
from config.loader import all_scenarios
from scenarios.main_menu import run_scenario_main_menu
#for now i will use DI but this should be easy to change in the future if we want (God willing lol)

class Orchestrator():
    """central orchestrator responsible for managing the change of scenarios"""
    def __init__(self,scenes:dict[str,Callable[[],None]],config_path:str = "config/config.json"):
        self.scenarios = all_scenarios(config_path)
        self.menu = self.scenarios[0] ### this is awfull , but willl do for now, in config the menu need to be the first
        self.scenes = scenes

        if self.menu != "menu":
            raise ValueError("menu MUST exist in config or everyhting breaks")
        if len(self.scenarios) - 1 != len(self.scenes):
            raise ValueError("this doesnt make sense, they must be the same lenght ")


    def start_orchestrator(self):
        run_scenario_main_menu("menu", self.run_scenario)


    def run_scenario(self,scenario:str)->None:
        if scenario not in self.scenes:
            raise KeyError("this scenario doesnt exist in the scenes dict provided, must be some problem in the  orchestrator ")
        self.scenes[scenario]()
            
    

    