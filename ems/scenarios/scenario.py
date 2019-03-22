from ems.datasets.case.case_set import CaseSet
from ems.triggers.trigger import Trigger


class Scenario:

    def __init__(self,
                 label: str,
                 priority: int,
                 trigger: Trigger,
                 case_set: CaseSet):
        self.label = label
        self.trigger = trigger
        self.priority = priority
        self.case_set = case_set
