import math
import random
from datetime import datetime, timedelta

from ems.generators.case.time.time import CaseTimeGenerator


# Implementation for a case time generator, where duration until next incident is drawn from the exponential
# distribution with parameter lambda
# lambda = (total # of cases) / (total # of time units in an interval)
# e.g. For 1,000 cases in 40,000 minutes, lambda = 1/40
class PoissonCaseTimeGenerator(CaseTimeGenerator):

    def __init__(self,
                 quantity: int,
                 duration: float):
        self.quantity = quantity
        self.duration = duration
        self.lmda = quantity / duration

    def generate(self,
                 time: datetime):
        rand = -math.log(1.0 - random.random())
        minutes_until_next = rand / self.lmda
        return time + timedelta(minutes=minutes_until_next)
