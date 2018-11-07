from datetime import datetime

from ems.datasets.case.case_set import CaseSet

from ems.generators.case.location.location import LocationGenerator
from ems.generators.case.time.time import CaseTimeGenerator

from ems.generators.event.random_duration import RandomDurationGenerator
from ems.models.cases.random_case import RandomCase


# Implementation of a case set that randomly generates cases while iterating
class RandomCaseSet(CaseSet):

    def __init__(self,
                 num_cases: int,
                 initial_time: datetime,
                 case_time_generator: CaseTimeGenerator,
                 location_generator: LocationGenerator):
        self.num_cases = num_cases
        self.initial_time = initial_time
        self.case_time_generator = case_time_generator
        self.location_generator = location_generator

    def iterator(self):
        k = 1
        time = self.initial_time

        while k <= self.num_cases:
            # Compute time and location of next event via generators
            time = self.case_time_generator.generate(time)
            point = self.location_generator.generate()

            # Define event duration generator for the case
            gen = RandomDurationGenerator()

            # Create case
            case = RandomCase(id=k,
                              date_recorded=time,
                              incident_location=point,
                              event_duration_generator=gen)

            k += 1

            yield case
