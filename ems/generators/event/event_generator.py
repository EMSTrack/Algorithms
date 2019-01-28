from datetime import datetime

from geopy import Point

from ems.algorithms.hospital_selectors.hospital_selector import HospitalSelector
from ems.generators.event.duration.duration import EventDurationGenerator
from ems.models.ambulances.ambulance import Ambulance
from ems.models.events.event import Event
from ems.models.events.event_type import EventType


class EventGenerator:

    def __init__(self,
                 travel_duration_generator: EventDurationGenerator,
                 incident_duration_generator: EventDurationGenerator,
                 hospital_duration_generator: EventDurationGenerator,
                 hospital_selector: HospitalSelector):
        self.hospital_selector = hospital_selector
        self.hospital_duration_generator = hospital_duration_generator
        self.incident_duration_generator = incident_duration_generator
        self.travel_duration_generator = travel_duration_generator

    def generate(self,
                 ambulance: Ambulance,
                 incident_location: Point,
                 timestamp: datetime,
                 event_type: EventType,
                 hospital_location=None):

        destination = None
        duration = 0

        if event_type == EventType.TO_INCIDENT:
            destination = incident_location
            duration = self.travel_duration_generator.generate(ambulance=ambulance,
                                                               destination=incident_location,
                                                               timestamp=timestamp)
        elif event_type == EventType.AT_INCIDENT:
            destination = incident_location
            duration = self.incident_duration_generator.generate(ambulance=ambulance,
                                                                 destination=incident_location,
                                                                 timestamp=timestamp)
        elif event_type == EventType.TO_BASE:
            destination = ambulance.base
            duration = self.travel_duration_generator.generate(ambulance=ambulance,
                                                               destination=incident_location,
                                                               timestamp=timestamp)
        elif event_type == EventType.TO_HOSPITAL or event_type == EventType.AT_HOSPITAL:

            if not hospital_location:
                destination = self.hospital_selector.select(timestamp=timestamp,
                                                            ambulance=ambulance)
            else:
                destination = hospital_location

            if event_type == EventType.TO_HOSPITAL:
                duration = self.travel_duration_generator.generate(ambulance=ambulance,
                                                                   destination=destination,
                                                                   timestamp=timestamp)
            else:
                duration = self.hospital_duration_generator.generate(ambulance=ambulance,
                                                                     destination=destination,
                                                                     timestamp=timestamp)
        else:
            # TODO -- other
            pass
        return Event(destination=destination,
                     duration=duration['duration'],
                     error=duration['error'] if 'error' in duration else None,
                     sim_dest=duration['sim_dest'] if 'sim_dest' in duration else None,
                     event_type=event_type)
