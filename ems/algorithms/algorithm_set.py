from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.algorithms.times.duration_algorithm import DurationAlgorithm


class AlgorithmSet:

    def __init__(self,
                 ambulance_selector: AmbulanceSelectionAlgorithm,
                 travel_duration_estimator: DurationAlgorithm,
                 stay_duration_estimator: DurationAlgorithm):
        self.ambulance_selector = ambulance_selector
        self.travel_duration_estimator = travel_duration_estimator
        self.stay_duration_estimator = stay_duration_estimator
