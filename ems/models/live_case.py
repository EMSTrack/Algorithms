from datetime import datetime, timedelta

from geopy import Point

from ems.models.ambulance import Ambulance
from ems.models.case import Case


class LiveCase(Case):

    def __init__(self,
                 id: int,
                 location: Point,
                 time: datetime,
                 weekday: str = None,
                 priority: float = None,
                 start_time: datetime = None,
                 finish_time: datetime = None,
                 delay: timedelta = None,
                 assigned_ambulance: Ambulance = None):
        super().__init__(id,
                         location,
                         time,
                         weekday,
                         priority,
                         start_time,
                         finish_time,
                         delay,
                         assigned_ambulance)

    # def start(self, ambulance, start_time, ambulance_travel_time):
    #
    #     # TODO - Currently assume that each case will take 2x travel time + 20 minutes
    #     # TODO - Algorithm for case duration?
    #     # Compute duration of the trip
    #     duration = ambulance_travel_time * 2 + timedelta(minutes=20)
    #
    #     self.start_time = start_time
    #     self.finish_time = start_time + duration
    #     self.delay = self.start_time - self.time
    #     self.assigned_ambulance = ambulance
    #
    # def get_duration(self):
    #     return self.finish_time - self.start_time
    #
    # def get_finish_time(self):
    #     return self.finish_time


