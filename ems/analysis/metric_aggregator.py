from typing import List

from ems.analysis.metric import Metric
from ems.models.ambulance import Ambulance


class MetricAggregator:

    def __init__(self,
                 metrics=None):

        if metrics is None:
            metrics = []

        self.metrics = metrics

    def add_metric(self, metric: Metric):

        if metric in self.metrics:
            # TODO custom exception
            raise Exception("Metric '{}' already exists in aggregator".format(metric.tag))

        self.metrics.append(metric)

    def remove_metric(self, metric: Metric):
        self.metrics.remove(metric)

    def calculate(self, ambulances: List[Ambulance]):

        d = {}
        for metric in self.metrics:
            d[metric.tag] = metric.calculate(ambulances)

        return d
