from datetime import datetime
from typing import List

from ems.datasets.case.case_set import CaseSet
from ems.scenarios.scenario import Scenario
from ems.scenarios.scenario_controller import ScenarioController


class ScenarioCaseSet(CaseSet):

    def __init__(self,
                 time: datetime,
                 scenarios: List[Scenario],
                 quantity: int = None):
        super().__init__(time)
        self.current_scenario = None
        self.scenario_controller = ScenarioController(scenarios=scenarios)
        self.scenarios = scenarios
        self.scenario_iterators = {scenario.label: scenario.case_set.iterator() for scenario in scenarios}
        self.current_scenario = None
        self.time = time
        self.quantity = quantity

    def __len__(self):
        return self.quantity

    def iterator(self):

        k = 1

        self.current_scenario, self.time = self.scenario_controller.retrieve_next_scenario(self.time)

        while k <= self.quantity:

            # We want to
            # 1. Generate case with current scenario
            # 2. Trigger scenarios with the time of the new case
            # 3. If a new scenario happens, generate a new case with that new scenario
            #    Otherwise, keep the generated case
            # Loop

            # Step 1: Determine scenario
            new_scenario = True
            new_case = None

            while new_scenario:

                # print("Temp Time: {}".format(self.time))
                # print("Temp Current scenario: {}".format(self.current_scenario.label))

                # Step 1: Generate case with the current scenario's iterator
                new_case = next(self.scenario_iterators[self.current_scenario.label])

                # print("Temp next case time: {}".format(new_case.date_recorded))

                self.scenario_controller.flush_inactive()

                # Step 2
                next_scenario, next_time = self.scenario_controller.retrieve_next_scenario(new_case.date_recorded)

                # Step 3
                if next_scenario == self.current_scenario:
                    self.time = new_case.date_recorded
                    new_scenario = False

                else:
                    self.current_scenario = next_scenario
                    self.time = next_time

                # Update times in all case sets
                for s in self.scenarios:
                    s.case_set.set_time(self.time)

                self.scenario_controller.flush_inactive()

            # self.scenario_controller.set_times(time=self.time)

            # TODO These could be useful as logs
            # print("Next Scenario: {}".format(self.current_scenario.label))
            # print("Next case time: {}".format(new_case.date_recorded))

            new_case.id = k
            k += 1

            yield new_case
