from datetime import datetime

from ems.analysis.metrics.metric import Metric


class CountPending(Metric):

    def __init__(self, tag="count_pending"):
        super().__init__(tag)

    def calculate(self, timestamp: datetime, **kwargs):
        if "pending_cases" not in kwargs:
            return None

        pending_cases = kwargs["pending_cases"]
        return len(pending_cases)
