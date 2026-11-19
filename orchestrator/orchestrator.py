from typing import Callable
from config.loader import all_scenarios
from scenarios.main_menu import run_scenario_main_menu

#main will create the dict cointaing scenes(aka scenarios) and pass it, then it will use it to call functions
#tbh, right now this is a bit unnecessary, basically acts as a pretty dictionary lookup
#but this might be usefull for dealing with a bunch of errors as well, alos doesnt hurt , even in this state...


class Orchestrator():
    """central orchestrator responsible for managing the change of scenarios"""
    def __init__(self,scenes:dict[str,Callable[[],None]],config_path:str = "config/config.json"):
        self.scenarios = all_scenarios(config_path)
        self.menu = self.scenarios[0] ### this is awfull , but willl do for now, in config the menu need to be the first
        self.scenes = scenes

        if self.menu != "menu":
            raise ValueError("menu MUST exist in config or everyhting breaks")
        

    def start_orchestrator(self):
        run_scenario_main_menu("menu", self.run_scenario) #again, this bound method is mega unncesessary, but i still think there are good opportunities to implement error handling later


    def run_scenario(self,scenario:str)->None:
        if scenario not in self.scenes:
            raise KeyError("this scenario doesnt exist in the scenes dict provided, must be some problem in the  orchestrator ")
        self.scenes[scenario]()
            
    

    