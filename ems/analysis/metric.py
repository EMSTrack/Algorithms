from typing import List

from ems.models.ambulance import Ambulance


class Metric:

    def __init__(self, tag: str):
        self.tag = tag

    def __eq__(self, other):
        return self.tag == self.tag

    # TODO -- define more parameters
    def calculate(self, ambulances: List[Ambulance]):
        raise NotImplementedError
