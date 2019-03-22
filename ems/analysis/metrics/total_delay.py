from datetime import datetime, timedelta

from ems.analysis.metrics.metric import Metric


class TotalDelay(Metric):

    def __init__(self, tag="total_delay"):
        super().__init__(tag)

    def calculate(self, timestamp: datetime, **kwargs):

        if "pending_cases" not in kwargs:
            return None

        pending_cases = kwargs["pending_cases"]
        total_delay = timedelta(seconds=0)

        for case in pending_cases:
            total_delay += timestamp - case.date_recorded

        return total_delay
