from datetime import datetime
from typing import List

from ems.datasets.case.case_set import CaseSet
from ems.scenarios.scenario import Scenario


class ScenarioCaseSet(CaseSet):

    def __init__(self,
                 time: datetime,
                 scenarios: List[Scenario],
                 quantity: int = None):
        super().__init__(time)
        self.current_scenario = None
        self.scenarios = sorted(scenarios, key=lambda s: s.priority)
        self.scenario_iterators = [s.case_set.iterator() for s in self.scenarios]
        self.current_scenario, self.current_iterator, self.time = self.trigger_scenarios(self.time)
        self.quantity = quantity

    def __len__(self):
        return self.quantity

    def iterator(self):

        k = 1

        while k <= self.quantity:

            # We want to
            # 1. Generate case with current scenario
            # 2. Trigger scenarios with the time of the new case
            # 3. If a new scenario happens, generate a new case with that new scenario
            #    Otherwise, keep the generated case
            # Loop

            new_scenario = True
            new_case = None

            while new_scenario:
                # Step 1
                new_case = next(self.current_iterator)

                # Step 2
                next_scenario, next_it, next_time = self.trigger_scenarios(new_case.date_recorded)

                # Step 3
                if next_scenario != self.current_scenario:
                    self.current_scenario, self.current_iterator, self.time = next_scenario, next_it, next_time
                    # Problem is that first trigger time is going off when it should be next one
                    # print("Next time: {}".format(next_time))
                else:
                    self.time = new_case.date_recorded
                    new_scenario = False

                # Update times in all case sets
                for s in self.scenarios:
                    s.case_set.set_time(self.time)
                # new_case = next(self.current_iterator)

            print("Next Scenario: {}".format(self.current_scenario.label))
            print("Next case time: {}".format(new_case.date_recorded))

            for s in self.scenarios:
                if s == self.current_scenario:
                    for t in s.triggers:
                        t.was_active = True
                else:
                    for t in s.triggers:
                        t.was_active = False

            # # Step 1
            # new_case = next(self.current_iterator)
            #
            # # Step 2
            # next_scenario, next_it, next_time = self.trigger_scenarios(new_case.date_recorded)
            #
            # # Step 3
            # if next_scenario != self.current_scenario:
            #     self.current_scenario, self.current_iterator, self.time = next_scenario, next_it, next_time
            #     # Update times in all case sets
            #     for s in self.scenarios:
            #         s.case_set.set_time(self.time)
            #     new_case = next(self.current_iterator)
            # else:
            #     # Update times in all case sets
            #     for s in self.scenarios:
            #         s.case_set.set_time(self.time)

            # Update scenario
            # self.current_scenario, self.current_iterator, self.time = self.trigger_scenarios(self.time)
            #
            # # Update times in all case sets
            # for s in self.scenarios:
            #     s.case_set.set_time(self.time)
            #
            # print(self.current_scenario.label)

            # Get next case from chosen iterator; update current time
            # new_case = next(self.current_iterator)
            new_case.id = k
            # self.time = new_case.date_recorded

            k += 1

            yield new_case

    def trigger_scenarios(self, time):

        new_s = None
        new_s_index = None
        new_time = datetime.max

        # Scenarios are sorted by priority
        for i, s in enumerate(self.scenarios):
            for t in s.triggers:

                is_active, start_time = t.is_active(time)

                if is_active:

                    if s.label == "disaster":
                        print(time)
                        print("what the hell")

                    # Scenario does not change if current scenario is still active and highest priority of active ones
                    if new_s is None and self.current_scenario is not None and s == self.current_scenario:
                        return s, self.scenario_iterators[i], time

                    # Otherwise, the earliest scenario with the highest priority will be saved
                    if start_time < new_time:
                        new_s = s
                        new_s_index = i
                        new_time = start_time
                # else:
                #     print("Inactive: {}".format(s.label))

        if new_s is not None:
            return new_s, self.scenario_iterators[new_s_index], new_time

        # No scenario is triggered for this timeframe; Error log?

        # If no initial scenario set:
        return self.current_scenario, self.current_iterator, self.time
