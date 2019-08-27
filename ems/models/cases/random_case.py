from datetime import datetime

from geopy import Point

from ems.generators.event.event_generator import EventGenerator
from ems.models.cases.case import Case
from ems.models.events.event_type import EventType



# Implementation of a Case that stochastically generates random events while iterating
# Events are currently defined in this order:
# TO_INCIDENT -> AT_INCIDENT -> TO_HOSPITAL -> AT_HOSPITAL
class RandomCase(Case):

    def __init__(self,
                 identifier: int,
                 date_recorded: datetime,
                 incident_location: Point,
                 event_generator: EventGenerator,
                 priority: int = None):
        super().__init__(identifier, date_recorded, incident_location, priority)
        self.event_generator = event_generator

    def iterator(self, ambulance, current_time):
        hospital_location = None
        for event_type in [EventType.TO_INCIDENT, EventType.AT_INCIDENT, EventType.TO_HOSPITAL, EventType.AT_HOSPITAL,
                           EventType.TO_BASE]:

            event = self.event_generator.generate(ambulance=ambulance,
                                                  incident_location=self.incident_location,
                                                  timestamp=current_time,
                                                  event_type=event_type,
                                                  hospital_location=hospital_location)
            if event_type == EventType.TO_HOSPITAL:
                hospital_location = event.destination

            current_time = current_time + event.duration

            yield event
