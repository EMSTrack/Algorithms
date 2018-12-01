from datetime import datetime

from geopy import Point

from ems.algorithms.hospital_selectors.hospital_selector import HospitalSelector
from ems.generators.case.location.random_circle import RandomCircleLocationGenerator
from ems.generators.event.duration import EventDurationGenerator
from ems.models.cases.case import Case
from ems.models.events.event import Event
from ems.models.events.event_type import EventType


# Implementation of a Case that stochastically generates random events while iterating
# Events are currently defined in this order:
# TO_INCIDENT -> AT_INCIDENT -> TO_HOSPITAL -> AT_HOSPITAL
class RandomCase(Case):

    def __init__(self,
                 id: int,
                 date_recorded: datetime,
                 incident_location: Point,
                 event_duration_generator: EventDurationGenerator,
                 hospital_selector: HospitalSelector,
                 priority: float = None):
        super().__init__(id, date_recorded, incident_location, priority)
        self.event_duration_generator = event_duration_generator
        self.hospital_selector = hospital_selector

    def iterator(self, ambulance, current_time):
        # Compute duration of trip
        duration = self.event_duration_generator.generate(ambulance=ambulance,
                                                          destination=self.incident_location,
                                                          current_time=current_time)

        current_time = current_time + duration

        # Produce new event for TO INCIDENT
        yield Event(destination=self.incident_location,
                    event_type=EventType.TO_INCIDENT,
                    duration=duration)

        # Compute duration of stay
        duration = self.event_duration_generator.generate(ambulance=ambulance,
                                                          destination=self.incident_location,
                                                          current_time=current_time)

        current_time = current_time + duration

        # Produce new event for AT INCIDENT
        yield Event(destination=self.incident_location,
                    event_type=EventType.AT_INCIDENT,
                    duration=duration)

        hospital_location = self.hospital_selector.select(timestamp=current_time,
                                                          ambulance=ambulance)

        # Compute duration of trip
        duration = self.event_duration_generator.generate(ambulance=ambulance,
                                                          destination=hospital_location,
                                                          current_time=current_time)

        current_time = current_time + duration

        # Produce new event for TO HOSPITAL
        yield Event(destination=hospital_location,
                    event_type=EventType.TO_HOSPITAL,
                    duration=duration)

        # Compute duration of stay
        duration = self.event_duration_generator.generate(ambulance=ambulance,
                                                          destination=hospital_location,
                                                          current_time=current_time)

        # Produce new event for AT HOSPITAL
        yield Event(destination=hospital_location,
                    event_type=EventType.AT_HOSPITAL,
                    duration=duration)

        # Compute duration of trip back to base
        duration = self.event_duration_generator.generate(ambulance=ambulance,
                                                          destination=ambulance.base,
                                                          current_time=current_time)

        yield Event(destination=ambulance.base,
                    event_type=EventType.TO_BASE,
                    duration=duration)
