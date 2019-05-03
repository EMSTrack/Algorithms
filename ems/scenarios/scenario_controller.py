# Manages the progression of scenarios
from datetime import datetime
from typing import List

from ems.scenarios.scenario import Scenario
from ems.triggers.trigger import Trigger


class TriggerTuple:

    def __init__(self,
                 scenario: Scenario,
                 trigger: Trigger):
        self.scenario = scenario
        self.trigger = trigger

    def __eq__(self, other):
        return self.scenario == other.scenario and self.trigger == other.trigger

    def __str__(self):
        return "Scenario {}; Trigger {}".format(self.scenario.label, self.trigger.id)


class TriggerTimeTuple:

    def __init__(self,
                 tt: TriggerTuple,
                 time: datetime):
        self.tt = tt
        self.time = time

    def __str__(self):
        return "Scenario {}; Trigger {}; Time: {}".format(self.tt.scenario.label, self.tt.trigger.id, self.time)


# Current solution relies on keeping track of all scenario triggers that are active at a given time. Upon call to
# retrieve the next scenario, all active scenarios that have ended should end and all inactive scenarios that have
# started should start. Then the new scenario should be the scenario with the highest priority of the active
# triggers.

# However, the problem is made complex because the caller may not be progressing in a constant tick by tick manner
# but rather, by event based, variable interval time jumps. Inactive scenarios may cause a "rewind" in time back to
# the start of its time. Thus the algorithm is as follows:

# 1. With given time, check all inactive triggers that have started
# 2. Beginning with the earliest started inactive trigger, check to see if any currently active triggers have
#    ended starting at that time. Mark those triggers as inactive.
# 3. Add the started inactive trigger to the active triggers
# 4. Check to see if newly active trigger has a higher priority than all of the still active triggers. If so, it
#    must be the new scenario. If so, return it; current list of active triggers should be correct.
# 5. Repeat from 2 with started inactive triggers in chronological order until no more
# 6. Reaching this step means that no newly activated scenarios (if any) have a higher priority than the existing
#    scenarios. Therefore, return the scenario with the highest priority in the active triggers list
class ScenarioController:

    def __init__(self,
                 scenarios: List[Scenario]):
        self.scenarios = scenarios
        self.active_triggers = []
        self.inactive_trigger_buffer = []

        index = 0
        for scenario in self.scenarios:
            for trigger in scenario.triggers:
                trigger.set_id(index)
                index += 1

    # Returns the next scenario and the new time
    def retrieve_next_scenario(self, time: datetime):

        self.set_times(time)

        fired_triggers = self._check_start_triggers(time)
        fired_triggers = sorted(fired_triggers, key=lambda x: x.time)

        # print("Fired triggers")
        # for p in fired_triggers:
        #     print(p)

        preactive_triggers = []
        for fired in fired_triggers:

            self.active_triggers, inactive_triggers = self._check_end_triggers(fired.time)
            preactive_triggers.append(fired)
            self.inactive_trigger_buffer += inactive_triggers

            # Priority comparison portion
            has_highest_priority = True
            for active_trigger in self.active_triggers:
                if active_trigger.tt.scenario.priority < fired.tt.scenario.priority:
                    has_highest_priority = False

            if has_highest_priority:
                self.active_triggers += preactive_triggers
                return fired.tt.scenario, fired.time

        self.active_triggers, inactive_triggers = self._check_end_triggers(time)
        self.active_triggers += preactive_triggers

        # print("Active triggers")
        # for p in self.active_triggers:
        #     print(p)
        #
        # print("Ended triggers")
        # for p in self.inactive_trigger_buffer:
        #     print(p)

        self.inactive_trigger_buffer += inactive_triggers

        if len(self.active_triggers) == 0:
            raise Exception("No scenario can be chosen")

        # Return scenario with highest priority
        self.active_triggers = sorted(self.active_triggers, key=lambda x: x.tt.scenario.priority)

        return self.active_triggers[0].tt.scenario, self.active_triggers[0].time

    def set_times(self, time):
        for active_trigger in self.active_triggers:
            active_trigger.time = time

    def flush_inactive(self):
        for inactive_trigger in self.inactive_trigger_buffer:
            inactive_trigger.tt.trigger.mark_ended()
        self.inactive_trigger_buffer = []

    # Returns a list of tuples of (start_time, st_pair) for each newly active trigger
    def _check_start_triggers(self, time: datetime):
        fired_triggers = []

        # Loop through each scenario's triggers
        for scenario in self.scenarios:
            for trigger in scenario.triggers:

                # If the trigger is not active but has started, add that to the list to return
                pair = TriggerTuple(scenario, trigger)

                if pair not in [active_trigger.tt for active_trigger in self.active_triggers]:

                    should_start, start_time = trigger.has_started(time=time)

                    if should_start:
                        fired_triggers.append(TriggerTimeTuple(tt=pair,
                                                               time=start_time))

        return fired_triggers

    # Returns two lists of triggers
    # One list of previously active triggers that are still active
    # Another list of previously active triggers that are now inactive
    def _check_end_triggers(self, time):

        actives = []
        inactives = []

        for active_trigger in self.active_triggers:
            if active_trigger.tt.trigger.has_ended(time):
                inactives.append(active_trigger)
            else:
                actives.append(active_trigger)

        return actives, inactives
