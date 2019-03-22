import datetime
from typing import List

from ems.datasets.case.case_set import CaseSet
from ems.scenarios.scenario import Scenario


class ScenarioCaseSet(CaseSet):

    def __init__(self,
                 time: datetime,
                 scenarios: List[Scenario],
                 num_cases: int = None):
        super().__init__(time)
        self.scenarios = sorted(scenarios, key=lambda s: s.priority)
        self.scenario_iterators = [s.case_set.iterator(s.label + "_") for s in self.scenarios]
        self.current_scenario, self.current_iterator = self.trigger_scenarios(self.time)
        self.num_cases = num_cases

    def __len__(self):
        return self.num_cases

    def iterator(self):

        k = 1

        # Update scenario
        self.current_scenario, self.current_iterator = self.trigger_scenarios(self.time)

        while k <= self.num_cases:
            # Get next case from chosen iterator; update current time
            new_case = next(self.current_iterator)
            self.time = new_case.date_recorded

            # Update times in all case sets
            for s in self.scenarios:
                s.case_set.set_time(self.time)

            k += 1

            yield new_case

    def trigger_scenarios(self, time):

        for i, s in enumerate(self.scenarios):
            if s.trigger.is_active(time):
                return s, self.scenario_iterators[i]

        # No scenario is triggered for this timeframe; Error log?

        # If no initial scenario set:
        return self.scenarios[0], self.scenario_iterators[0]
