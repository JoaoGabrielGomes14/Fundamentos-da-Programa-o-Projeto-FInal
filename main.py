from orchestrator.orchestrator import Orchestrator
from scenarios.scenario_2 import run_scenario_2

if __name__ == "__main__":
    orchestrator = Orchestrator({"2": run_scenario_2})
    orchestrator.start_orchestrator()