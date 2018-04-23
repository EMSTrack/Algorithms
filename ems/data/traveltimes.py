from datetime import timedelta


# TODO -- instead of a model, make a travel time set object
class TravelTime:

    def __init__(self, base_id: int, demand_id: int, traveltime: timedelta):
        self.base_id = base_id
        self.demand_id = demand_id
        self.traveltime = traveltime
