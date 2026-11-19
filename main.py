from config.types_config import WindowSettings,ButtonSettings,Scenario
from config.loader import load_scenario
from scenarios.main_menu import run_scenario_main_menu
from orchestrator.orchestrator import Orchestrator

orchestrator = Orchestrator({})  
orchestrator.start_orchestrator()



###testing