import datetime

from ems.generators.duration.random_duration import RandomDurationGenerator
from ems.generators.time.time import CaseTimeGenerator


class RandomCaseTimeGenerator(CaseTimeGenerator):

    def __init__(self,
                 lower_bound: float = 30,
                 upper_bound: float = 45):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.random_duration_generator = RandomDurationGenerator(lower_bound,
                                                          upper_bound)

    def generate(self,
                 time: datetime):
        return time + self.random_duration_generator.generate(None,
                                                              None,
                                                              None)['duration']
