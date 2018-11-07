# Implementation of a case set which is instantiated from a list of already known cases
from typing import List

from ems.datasets.case.case_set import CaseSet
from ems.models.cases.case import Case


class DefinedCaseSet(CaseSet):

    def __init__(self,
                 cases: List[Case]=None):
        self.cases = cases

    def iterator(self):
        return iter(self.cases)
